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

from langchain_core.callbacks import AsyncCallbackManagerForToolRun
from langchain_core.tools import BaseTool
from pydantic import BaseModel

from langchain_lightdash.lightdash.api.list_organization_projects_v1 import (
    ListOrganizationProjects,
)
from langchain_lightdash.lightdash.client import LightdashClient


class GetProjectsInput(BaseModel):
    """Input for the GetProjects tool."""


class GetProjects(BaseTool):
    """Get project details by UUID."""

    name: str = "get_project"
    description: str = "Fetches the project associated with the given UUID."
    args_schema: Type[BaseModel] = GetProjectsInput
    return_direct: bool = False

    lightdash_client: LightdashClient

    def _run(self) -> str:
        response = ListOrganizationProjects(client=self.lightdash_client).call()
        return response.results.model_dump_json()

    async def _arun(
      self,
      run_manager: Optional[AsyncCallbackManagerForToolRun] = None) -> str:
        return self._run(run_manager=run_manager.get_sync())
