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

from typing import Optional, Type

from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

from lightdash_ai_tools.lightdash.api.get_project_v1 import GetProjectV1
from lightdash_ai_tools.lightdash.client import LightdashClient


class GetProjectInput(BaseModel):
    """Input for the GetProject tool."""
    project_uuid: str = Field(description="The UUID of the project to fetch.")

class GetProject(BaseTool):
    """Get project details"""

    name: str = "get_project"
    description: str = "Fetches the project associated with the given UUID."
    args_schema: Type[BaseModel] = GetProjectInput
    return_direct: bool = False

    lightdash_client: LightdashClient

    def _run(self, project_uuid: str, run_manager: Optional[CallbackManagerForToolRun] = None) -> str:
        response = GetProjectV1(client=self.lightdash_client).call(project_uuid)
        return response.results.model_dump_json()

    async def _arun(
      self,
      project_uuid: str,
      run_manager: Optional[AsyncCallbackManagerForToolRun] = None) -> str:
        return self._run(project_uuid, run_manager=run_manager.get_sync())
