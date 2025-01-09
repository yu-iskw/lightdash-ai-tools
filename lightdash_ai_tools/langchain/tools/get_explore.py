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

from lightdash_ai_tools.lightdash.api.get_explore_v1 import GetExploreV1
from lightdash_ai_tools.lightdash.client import LightdashClient
from lightdash_ai_tools.lightdash.models.get_explore_v1 import GetExploreV1Response


class GetExploreInput(BaseModel):
    """Input for the GetExplore tool."""
    project_uuid: str = Field(description="The UUID of the project.")
    explore_id: str = Field(description="The ID of the explore to retrieve.")

class GetExplore(BaseTool):
    """Get a specific explore in a project"""

    name: str = "get_explore"
    description: str = "Get a specific explore (table) in a project."
    args_schema: Type[BaseModel] = GetExploreInput
    return_direct: bool = False

    lightdash_client: LightdashClient

    def _run(self, project_uuid: str, explore_id: str, run_manager: Optional[CallbackManagerForToolRun] = None) -> GetExploreV1Response:
        response = GetExploreV1(client=self.lightdash_client).call(project_uuid, explore_id)
        return response

    async def _arun(
        self,
        project_uuid: str,
        explore_id: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> GetExploreV1Response:
        if run_manager is not None:
            return self._run(project_uuid, explore_id, run_manager=run_manager.get_sync())
        return self._run(project_uuid, explore_id)
