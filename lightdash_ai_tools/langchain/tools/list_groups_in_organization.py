from typing import Optional, Type

from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

from lightdash_ai_tools.lightdash.client import LightdashClient
from lightdash_ai_tools.lightdash.services.list_groups_in_organization import (
    ListGroupsInOrganizationService,
)


class ListGroupsToolSchema(BaseModel):
    page_size: Optional[float] = Field(
        default=100,
        description="Number of results per page. Defaults to 100."
    )
    include_members: Optional[float] = Field(
        default=None,
        description="Number of members to include in the group details"
    )
    search_query: Optional[str] = Field(
        default=None,
        description="Optional search query to filter groups"
    )

class ListGroupsInOrganizationTool(BaseTool):
    """Tool to list groups in the current user's organization."""

    name = "list_groups_in_organization"
    description = "Retrieve all groups in the current user's organization"
    args_schema: Type[BaseModel] = ListGroupsToolSchema

    def __init__(self, lightdash_client: LightdashClient):
        """
        Initialize the tool with a Lightdash API client

        :param lightdash_client: Authenticated Lightdash API client
        """
        super().__init__()
        self.lightdash_client = lightdash_client

    def _run(
        self,
        page_size: Optional[float] = 100,
        include_members: Optional[float] = None,
        search_query: Optional[str] = None
    ) -> str:
        """
        Run method to list groups

        :return: Formatted string of groups
        """
        service = ListGroupsInOrganizationService(self.lightdash_client)
        groups = service.get_all_groups(
            page_size=page_size,
            include_members=include_members,
            search_query=search_query
        )

        if not groups:
            return "No groups found in the organization."

        # Format groups into a readable string
        group_list = "\n".join([
            f"Group Name: {group.name}, UUID: {group.uuid}"
            for group in groups
        ])

        return f"Found {len(groups)} groups:\n{group_list}"

    async def _arun(self, *args, **kwargs):
        """
        Async run method (not implemented)

        :raises NotImplementedError: This method is not implemented
        """
        raise NotImplementedError("list_groups_in_organization does not support async")
