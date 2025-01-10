from typing import List, Optional

from lightdash_ai_tools.lightdash.api.list_groups_in_organization_v1 import (
    ListGroupsInOrganizationV1,
)
from lightdash_ai_tools.lightdash.client import LightdashClient
from lightdash_ai_tools.lightdash.models.list_groups_in_organization_v1 import Group


class ListGroupsInOrganizationService:
    def __init__(self, lightdash_client: LightdashClient):
        self.lightdash_client = lightdash_client

    def get_all_groups(
        self,
        page_size: Optional[float] = 100,
        include_members: Optional[float] = None,
        search_query: Optional[str] = None,
    ) -> List[Group]:
        """
        Retrieve all groups across all pages

        :param page_size: Number of results per page
        :param include_members: Number of members to include
        :param search_query: Search query to filter groups
        :return: ListGroupsResponse or list of groups
        """
        all_groups: List[Group] = []
        current_page = 1

        while True:
            response = ListGroupsInOrganizationV1(lightdash_client=self.lightdash_client).call(
                page=current_page,
                page_size=page_size,
                include_members=include_members,
                search_query=search_query
            )

            # Extract groups from the response
            current_groups = response.results.data
            all_groups.extend(current_groups)

            # Check if we've retrieved all pages
            pagination = response.results.pagination
            total_pages = pagination.totalPageCount

            if current_page >= total_pages:
                break

            current_page += 1
        return all_groups
