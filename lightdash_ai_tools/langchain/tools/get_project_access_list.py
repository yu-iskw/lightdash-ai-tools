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

from lightdash_ai_tools.lightdash.api.get_project_access_list_v1 import (
    GetProjectAccessListV1,
)
from lightdash_ai_tools.lightdash.client import LightdashClient


class GetProjectAccessListToolInput(BaseModel):
    """Input for the GetProjectAccessListTool tool."""
    project_uuid: str = Field(description="The UUID of the project to get access list for")


class GetProjectAccessListTool(BaseTool):
    """Get project access list"""

    name: str = "get_project_access_list"
    description: str = "Get the list of users with access to a specific project"
    args_schema: Type[BaseModel] = GetProjectAccessListToolInput
    return_direct: bool = False
    handle_tool_error: bool = True

    lightdash_client: LightdashClient

    def _run(
        self,
        project_uuid: str,
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> List[str]:
        """
        Run method for getting project access list.

        Returns:
            List of project access members as JSON strings
        """
        try:
            api_call = GetProjectAccessListV1(client=self.lightdash_client)
            response = api_call.call(project_uuid)
            return [member.model_dump_json() for member in response.results]
        except Exception as e:
            error_message = textwrap.dedent(f"""\
              Error retrieving project access list.
              Exception: {type(e).__name__}: {e}
            """).strip()
            raise ToolException(error_message) from e

    async def _arun(
        self,
        project_uuid: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> List[str]:
        """
        Async run method for getting project access list.

        Returns:
            List of project access members as JSON strings
        """
        try:
            if run_manager is not None:
                return self._run(project_uuid, run_manager=run_manager.get_sync())
            return self._run(project_uuid)
        except Exception as e:
            error_message = textwrap.dedent(f"""\
              Error retrieving project access list asynchronously with project_uuid: {project_uuid}.
              Exception: {type(e).__name__}: {e}
            """).strip()
            raise ToolException(error_message) from e
