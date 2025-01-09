# Copyright 2025 yu-iskw
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import List, Optional, Type

from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool
from pydantic import BaseModel

from lightdash_ai_tools.lightdash.api.list_spaces_in_project import ListSpacesInProject
from lightdash_ai_tools.lightdash.client import LightdashClient


class GetSpacesInProjectInput(BaseModel):
    """Input for the GetSpacesInProject tool."""
    project_uuid: str

class GetSpacesInProject(BaseTool):
    """Get spaces in a project"""

    name: str = "get_spaces_in_project"
    description: str = "Get spaces in a project"
    args_schema: Type[BaseModel] = GetSpacesInProjectInput
    return_direct: bool = False

    lightdash_client: LightdashClient

    def _run(self, project_uuid: str, run_manager: Optional[CallbackManagerForToolRun] = None) -> List[str]:
        response = ListSpacesInProject(client=self.lightdash_client).call(project_uuid)
        spaces = response.results
        return [space.model_dump_json() for space in spaces]

    async def _arun(
      self,
      project_uuid: str,
      run_manager: Optional[AsyncCallbackManagerForToolRun] = None) -> List[str]:
        return self._run(project_uuid, run_manager=run_manager.get_sync())
