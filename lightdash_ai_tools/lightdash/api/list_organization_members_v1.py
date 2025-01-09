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
from lightdash_ai_tools.lightdash.models.list_organization_members_v1 import (
    ListOrganizationMembersV1Response,
)


class ListOrganizationMembersV1(BaseLightdashApiCaller[ListOrganizationMembersV1Response]):
    """API call to list organization members."""

    request_type = RequestType.GET

    def _request(
        self,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        search_query: Optional[str] = None,
        project_uuid: Optional[str] = None,
        include_groups: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        List organization members.

        Args:
            page: Page number for pagination
            page_size: Number of results per page
            search_query: Search query to filter members
            project_uuid: Filter users who can view this project
            include_groups: Optional parameter for groups

        Returns:
            Dict[str, Any]
        """
        if page_size is None:
            page_size = 100
        parameters = {
            k: str(v) for k, v in {
                'page': page,
                'pageSize': page_size,
                'searchQuery': search_query,
                'projectUuid': project_uuid,
                'includeGroups': include_groups
            }.items() if v is not None
        }

        formatted_path = "/api/v1/org/users"
        response_data = self.client.call(self.request_type, formatted_path, parameters=parameters)
        return response_data

    def _parse_response(self, response_data: Dict[str, Any]) -> ListOrganizationMembersV1Response:
        return ListOrganizationMembersV1Response(**response_data)
