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

from lightdash_ai_tools.common.tools.get_groups_in_organization import (
    GetGroupsInOrganization,
)
from lightdash_ai_tools.lightdash.client import LightdashClient
from lightdash_ai_tools.lightdash.models.list_groups_in_organization_v1 import Group


class GetGroupsInOrganizationTool(BaseTool):
    """Tool to list groups in the current user's organization."""

    name: str = GetGroupsInOrganization.name
    description: str = GetGroupsInOrganization.description
    args_schema: Type[BaseModel] = GetGroupsInOrganization.input_schema
    handle_tool_error: bool = True
    handle_validation_error: bool = True

    lightdash_client: LightdashClient

    def _run(
        self,
        page_size: Optional[float] = 100,
        include_members: Optional[float] = None,
        search_query: Optional[str] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> List[Group]:
        """
        Run method to list groups

        :return: Formatted string of groups
        """
        try:
            tool = GetGroupsInOrganization(lightdash_client=self.lightdash_client)
            return tool.call(
                page_size=page_size,
                include_members=include_members,
                search_query=search_query
            )
        except Exception as e:
            error_message = textwrap.dedent(f"""\
              Error retrieving groups in organization.
              Exception: {type(e).__name__}: {e}
            """).strip()
            raise ToolException(error_message) from e

    async def _arun(
        self,
        page_size: Optional[float] = 100,
        include_members: Optional[float] = None,
        search_query: Optional[str] = None,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> List[Group]:
        """
        Asynchronously retrieve groups in the organization.

        :param page_size: Number of results per page
        :param include_members: Number of members to include
        :param search_query: Search query to filter groups
        :param run_manager: Optional async callback manager
        :return: List of groups
        """
        try:
            tool = GetGroupsInOrganization(lightdash_client=self.lightdash_client)
            return await tool.acall(
                page_size=page_size,
                include_members=include_members,
                search_query=search_query
            )
        except Exception as e:
            error_message = textwrap.dedent(f"""\
              Error retrieving groups in organization asynchronously.
              Exception: {type(e).__name__}: {e}
            """).strip()
            raise ToolException(error_message) from e
