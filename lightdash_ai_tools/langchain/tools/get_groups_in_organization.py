from typing import List, Optional, Type

from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

from lightdash_ai_tools.lightdash.client import LightdashClient
from lightdash_ai_tools.lightdash.models.list_groups_in_organization_v1 import Group
from lightdash_ai_tools.lightdash.services.list_groups_in_organization import (
    ListGroupsInOrganizationService,
)


class GetGroupsInOrganizationToolInput(BaseModel):
    """Input for the GetGroupsInOrganizationTool tool."""
    # page_size: Optional[float] = Field(
    #     default=100,
    #     description="Number of results per page. Defaults to 100."
    # )
    # include_members: Optional[float] = Field(
    #     default=None,
    #     description="Number of members to include in the group details"
    # )
    # search_query: Optional[str] = Field(
    #     default=None,
    #     description="Optional search query to filter groups"
    # )


class GetGroupsInOrganizationTool(BaseTool):
    """Tool to list groups in the current user's organization."""

    name: str = "get_groups_in_organization"
    description: str = "Retrieve all groups in the current user's organization"
    args_schema: Type[BaseModel] = GetGroupsInOrganizationToolInput

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
        service = ListGroupsInOrganizationService(lightdash_client=self.lightdash_client)
        return service.get_all_groups(
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
