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

from lightdash_ai_tools.common.tools.get_group import GetGroup
from lightdash_ai_tools.lightdash.client import LightdashClient
from lightdash_ai_tools.lightdash.models.get_group_v1 import GetGroupV1Response


class GetGroupTool(BaseTool):
    """Tool for getting group details."""

    name: str = GetGroup.name
    description: str = GetGroup.description
    args_schema: Type[BaseModel] = GetGroup.input_schema
    return_direct: bool = False
    handle_tool_error: bool = True
    handle_validation_error: bool = True

    lightdash_client: LightdashClient

    def _run(
        self,
        group_uuid: str,
        include_members: Optional[int] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> GetGroupV1Response:
        """
        Run the get group tool.

        :param group_uuid: Unique identifier of the group
        :param include_members: Number of members to include
        :param run_manager: Optional callback manager
        :return: Group details response
        """
        try:
            tool = GetGroup(lightdash_client=self.lightdash_client)
            return tool.call(
                group_uuid=group_uuid,
                include_members=include_members,
            )
        except Exception as e:
            error_message = textwrap.dedent(f"""\
              Error retrieving group details with group_uuid: {group_uuid}.
              Exception: {type(e).__name__}: {e}
            """).strip()
            raise ToolException(error_message) from e

    async def _arun(
        self,
        group_uuid: str,
        include_members: Optional[int] = None,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> GetGroupV1Response:
        """
        Asynchronously retrieve group details.

        :param group_uuid: Unique identifier of the group
        :param include_members: Number of members to include
        :param run_manager: Optional async callback manager
        :return: Group details
        """
        try:
            tool = GetGroup(lightdash_client=self.lightdash_client)
            return await tool.acall(
                group_uuid=group_uuid,
                include_members=include_members
            )
        except Exception as e:
            error_message = textwrap.dedent(f"""\
              Error retrieving group details asynchronously with group_uuid: {group_uuid}.
              Exception: {type(e).__name__}: {e}
            """).strip()
            raise ToolException(error_message) from e
