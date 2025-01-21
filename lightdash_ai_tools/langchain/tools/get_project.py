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
from typing import Optional, Type

from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool, ToolException
from pydantic import BaseModel

from lightdash_ai_tools.common.tools.get_project import GetProject
from lightdash_ai_tools.lightdash.client import LightdashClient
from lightdash_ai_tools.lightdash.models.get_project_v1 import GetProjectResults


class GetProjectTool(BaseTool):
    """Get a project by uuid"""

    name: str = GetProject.name
    description: str = GetProject.description
    args_schema: Type[BaseModel] = GetProject.input_schema
    return_direct: bool = False
    handle_tool_error: bool = True
    handle_validation_error: bool = True

    lightdash_client: LightdashClient

    def _run(
        self,
        project_uuid: str,
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> GetProjectResults:
        """
        Run method for getting a project by uuid.

        Returns:
            Project
        """
        try:
            tool = GetProject(lightdash_client=self.lightdash_client)
            return tool.call(project_uuid=project_uuid)
        except Exception as e:
            error_message = textwrap.dedent(f"""\
              Error retrieving project with project_uuid: {project_uuid}.
              Exception: {type(e).__name__}: {e}
            """).strip()
            raise ToolException(error_message) from e

    async def _arun(
        self,
        project_uuid: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> GetProjectResults:
        """
        Asynchronously retrieve a project by uuid.

        :param project_uuid: UUID of the project
        :param run_manager: Optional async callback manager
        :return: Project
        """
        try:
            tool = GetProject(lightdash_client=self.lightdash_client)
            return await tool.acall(project_uuid=project_uuid)
        except Exception as e:
            error_message = textwrap.dedent(f"""\
              Error retrieving project asynchronously with project_uuid: {project_uuid}.
              Exception: {type(e).__name__}: {e}
            """).strip()
            raise ToolException(error_message) from e
