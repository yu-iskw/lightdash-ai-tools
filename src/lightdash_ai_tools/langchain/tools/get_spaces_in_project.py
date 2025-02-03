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

from lightdash_ai_tools.common.tools.get_spaces_in_project import GetSpacesInProject
from lightdash_ai_tools.lightdash.client import LightdashClient
from lightdash_ai_tools.lightdash.models.list_spaces_in_project_v1 import (
    ListSpacesInProjectV1Results,
)


class GetSpacesInProjectTool(BaseTool):
    """Get spaces in a project"""

    name: str = GetSpacesInProject.name
    description: str = GetSpacesInProject.description
    args_schema: Type[BaseModel] = GetSpacesInProject.input_schema
    return_direct: bool = False
    handle_tool_error: bool = True
    handle_validation_error: bool = True

    lightdash_client: LightdashClient

    def _run(
        self,
        project_uuid: str,
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> List[ListSpacesInProjectV1Results]:
        """
        Run method for getting spaces in a project.

        Returns:
            List of spaces in the project
        """
        try:
            tool = GetSpacesInProject(lightdash_client=self.lightdash_client)
            return tool.call(project_uuid=project_uuid)
        except Exception as e:
            error_message = textwrap.dedent(f"""\
              Error retrieving spaces in project.
              Exception: {type(e).__name__}: {e}
            """).strip()
            raise ToolException(error_message) from e

    async def _arun(
        self,
        project_uuid: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> List[ListSpacesInProjectV1Results]:
        """
        Asynchronously retrieve spaces in a project.

        :param project_uuid: UUID of the project
        :param run_manager: Optional async callback manager
        :return: List of spaces in the project
        """
        try:
            tool = GetSpacesInProject(lightdash_client=self.lightdash_client)
            return await tool.acall(project_uuid=project_uuid)
        except Exception as e:
            error_message = textwrap.dedent(f"""\
              Error retrieving spaces in project asynchronously with project_uuid: {project_uuid}.
              Exception: {type(e).__name__}: {e}
            """).strip()
            raise ToolException(error_message) from e
