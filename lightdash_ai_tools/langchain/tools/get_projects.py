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

import textwrap
from typing import List, Optional, Type

from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool, ToolException
from pydantic import BaseModel

from lightdash_ai_tools.lightdash.client import LightdashClient
from lightdash_ai_tools.lightdash.controller.get_projects import GetProjectsController
from lightdash_ai_tools.lightdash.models.list_organization_projects_v1 import (
    ListOrganizationProjectsV1Results,
)


class GetProjectsToolInput(BaseModel):
    """Input for the GetProjectsTool tool."""


class GetProjectsTool(BaseTool):
    """Get project details by UUID."""

    name: str = "get_projects"
    description: str = "Get all projects in the organization."
    args_schema: Type[BaseModel] = GetProjectsToolInput
    return_direct: bool = False
    handle_tool_error: bool = True
    handle_validation_error: bool = True

    lightdash_client: LightdashClient

    def _run(self, run_manager: Optional[CallbackManagerForToolRun] = None) -> List[ListOrganizationProjectsV1Results]:
        try:
            controller = GetProjectsController(lightdash_client=self.lightdash_client)
            results = controller()
            return results
        except Exception as e:
            error_message = textwrap.dedent(f"""\
              Error retrieving organization projects.
              Exception: {type(e).__name__}: {e}
            """).strip()
            raise ToolException(error_message) from e

    async def _arun(
      self,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None) -> List[ListOrganizationProjectsV1Results]:
        try:
            if run_manager is not None:
                return self._run(run_manager=run_manager.get_sync())
            return self._run()
        except Exception as e:
            error_message = textwrap.dedent(f"""\
              Error retrieving organization projects asynchronously.
              Exception: {type(e).__name__}: {e}
            """).strip()
            raise ToolException(error_message) from e
