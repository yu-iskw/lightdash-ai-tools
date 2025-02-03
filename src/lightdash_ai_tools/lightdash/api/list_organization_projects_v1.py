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
from lightdash_ai_tools.lightdash.models.list_organization_projects_v1 import (
    ListOrganizationProjectsV1Response,
)


class ListOrganizationProjectsV1(BaseLightdashApiCaller[ListOrganizationProjectsV1Response]):
    """Gets all projects of the current user's organization"""
    request_type = RequestType.GET

    def _request(
        self,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        search_query: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Retrieve all projects in the current organization.

        Args:
            page: Page number for pagination
            page_size: Number of results per page
            search_query: Search query to filter projects

        Returns:
            Dict[str, Any]: List of organization projects.
        """
        formatted_path = self._get_endpoint()
        params = {}
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size
        if search_query is not None:
            params["search_query"] = search_query
        return self.lightdash_client.call(request_type=self.request_type, path=formatted_path, parameters=params)

    async def _arequest(
        self,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        search_query: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Asynchronously retrieve all projects in the current organization.

        Args:
            page: Page number for pagination
            page_size: Number of results per page
            search_query: Search query to filter projects

        Returns:
            Dict[str, Any]: List of organization projects.
        """
        formatted_path = self._get_endpoint()
        params = {}
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size
        if search_query is not None:
            params["search_query"] = search_query
        return await self.lightdash_client.acall(request_type=self.request_type, path=formatted_path, parameters=params)

    def _parse_response(self, response_data: Dict[str, Any]) -> ListOrganizationProjectsV1Response:
        return ListOrganizationProjectsV1Response(**response_data)

    def _get_endpoint(self) -> str:
        """
        Build the path for the API request.
        """
        return "/api/v1/org/projects"
