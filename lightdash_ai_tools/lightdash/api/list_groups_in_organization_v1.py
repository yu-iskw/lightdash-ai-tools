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

from typing import Any, Dict, Optional

from lightdash_ai_tools.lightdash.api.base import BaseLightdashApiCaller
from lightdash_ai_tools.lightdash.client import RequestType
from lightdash_ai_tools.lightdash.models.list_groups_in_organization_v1 import (
    ListGroupsInOrganizationV1Response,
)


class ListGroupsInOrganizationV1(BaseLightdashApiCaller[ListGroupsInOrganizationV1Response]):
    """API call to list groups in the organization."""

    request_type = RequestType.GET

    def _request(
        self,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        search_query: Optional[str] = None,
        include_members: Optional[float] = None,
    ) -> Dict[str, Any]:
        """
        List groups in the organization.

        Args:
            page: Page number for pagination
            page_size: Number of results per page
            search_query: Search query to filter groups
            include_members: Optional parameter to include members in the group details

        Returns:
            Dict[str, Any]
        """
        formatted_path = self._get_endpoint()
        params = {}
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["pageSize"] = page_size
        if search_query is not None:
            params["searchQuery"] = search_query
        if include_members is not None:
            params["includeMembers"] = include_members

        response_data = self.lightdash_client.call(
            request_type=self.request_type, path=formatted_path, parameters=params
        )
        return response_data

    async def _arequest(
        self,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        search_query: Optional[str] = None,
        include_members: Optional[float] = None,
    ) -> Dict[str, Any]:
        """
        Async version: List groups in the organization.

        Args:
            page: Page number for pagination
            page_size: Number of results per page
            search_query: Search query to filter groups
            include_members: Optional parameter to include members in the group details

        Returns:
            Dict[str, Any]
        """
        formatted_path = self._get_endpoint()
        params = {}
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size
        if search_query is not None:
            params["search_query"] = search_query
        if include_members is not None:
            params["include_members"] = include_members
        return await self.lightdash_client.acall(
            request_type=self.request_type,
            path=formatted_path,
            parameters=params,
        )

    def _parse_response(self, response_data: Dict[str, Any]) -> ListGroupsInOrganizationV1Response:
        return ListGroupsInOrganizationV1Response(**response_data)

    def _get_endpoint(self) -> str:
        """
        Build the path for the API request.
        """
        return "/api/v1/org/groups"
