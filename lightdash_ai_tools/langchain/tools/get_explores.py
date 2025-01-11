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
from pydantic import BaseModel, Field

from lightdash_ai_tools.lightdash.client import LightdashClient
from lightdash_ai_tools.lightdash.controller.get_explores import GetExploresController
from lightdash_ai_tools.lightdash.models.get_explores_v1 import GetExploresV1Results


class GetExploresToolInput(BaseModel):
    """Input for the GetExploresTool tool."""
    project_uuid: str = Field(description="The UUID of the project to get explores for. That isn't the project name.")


class GetExploresTool(BaseTool):
    """Get explores in a project"""

    name: str = "get_explores"
    description: str = "Get explores (tables) in a project."
    args_schema: Type[BaseModel] = GetExploresToolInput
    return_direct: bool = False
    handle_tool_error: bool = True
    handle_validation_error: bool = True

    lightdash_client: LightdashClient

    def _run(self, project_uuid: str, run_manager: Optional[CallbackManagerForToolRun] = None) -> List[GetExploresV1Results]:
        try:
            controller = GetExploresController(lightdash_client=self.lightdash_client)
            return controller(project_uuid)
        except Exception as e:
            error_message = textwrap.dedent(f"""\
              Error retrieving explores with project_uuid: {project_uuid}.
              Exception: {type(e).__name__}: {e}
            """).strip()
            raise ToolException(error_message) from e

    async def _arun(
      self,
      project_uuid: str,
      run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> List[GetExploresV1Results]:
        try:
            if run_manager is not None:
                return self._run(project_uuid, run_manager=run_manager.get_sync())
            return self._run(project_uuid)
        except Exception as e:
            error_message = textwrap.dedent(f"""\
              Error retrieving explores asynchronously with project_uuid: {project_uuid}.
              Exception: {type(e).__name__}: {e}
            """).strip()
            raise ToolException(error_message) from e
