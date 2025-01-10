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


from typing import Any, Dict

from lightdash_ai_tools.lightdash.api.base import BaseLightdashApiCaller
from lightdash_ai_tools.lightdash.client import RequestType
from lightdash_ai_tools.lightdash.models.list_organization_projects_v1 import (
    ListOrganizationProjectsV1Response,
)


class ListOrganizationProjectsV1(BaseLightdashApiCaller[ListOrganizationProjectsV1Response]):
    """Gets all projects of the current user's organization"""
    request_type = RequestType.GET

    def _request(self) -> Dict[str, Any]:
        """
        Retrieve all projects in the current organization.

        Returns:
            ListOrganizationProjectsResponse: List of organization projects.
        """
        formatted_path = "/api/v1/org/projects"
        return self.lightdash_client.call(self.request_type, formatted_path)

    def _parse_response(self, response_data: Dict[str, Any]) -> ListOrganizationProjectsV1Response:
        return ListOrganizationProjectsV1Response(**response_data)
