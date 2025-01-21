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

from typing import List, Optional, Type

from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

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

    lightdash_client: LightdashClient = Field(..., description="Lightdash API client")

    def _run(
        self,
        page_size: Optional[float] = 100,
        include_members: Optional[float] = None,
        search_query: Optional[str] = None
    ) -> List[Group]:
        """
        Run method to list groups

        :return: Formatted string of groups
        """
        tool = GetGroupsInOrganization(lightdash_client=self.lightdash_client)
        return tool(
            page_size=page_size,
            include_members=include_members,
            search_query=search_query
        )

    async def _arun(self, *args, **kwargs):
        """
        Async run method (not implemented)

        :raises NotImplementedError: This method is not implemented
        """
        raise NotImplementedError("get_groups_in_organization does not support async")
