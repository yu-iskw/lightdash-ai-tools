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
from lightdash_ai_tools.lightdash.models.get_project_access_list_v1 import (
    GetProjectAccessListV1Response,
)


class GetProjectAccessListV1(BaseLightdashApiCaller[GetProjectAccessListV1Response]):
    """Get project access list"""
    request_type = RequestType.GET

    def _request(self, project_uuid: str) -> Dict[str, Any]:
        """
        Retrieve the access list for a specific project.

        Args:
            project_uuid (str): The UUID of the project to retrieve access list for.

        Returns:
            Dict[str, Any]: The raw response data from the API.
        """
        formatted_path = self._get_endpoint(project_uuid=project_uuid)
        response_data = self.lightdash_client.call(self.request_type, formatted_path)
        return response_data

    async def _arequest(self, project_uuid: str) -> Dict[str, Any]:
        """
        Retrieve the access list for a specific project asynchronously.

        Args:
            project_uuid (str): The UUID of the project to retrieve access list for.

        Returns:
            Dict[str, Any]: The raw response data from the API.
        """
        formatted_path = self._get_endpoint(project_uuid=project_uuid)
        response_data = await self.lightdash_client.acall(self.request_type, formatted_path)
        return response_data

    def _parse_response(self, response_data: Dict[str, Any]) -> GetProjectAccessListV1Response:
        return GetProjectAccessListV1Response(**response_data)

    def _get_endpoint(self, project_uuid: str) -> str:
        """
        Build the path for the API request.
        """
        return f"/api/v1/projects/{project_uuid}/access"
