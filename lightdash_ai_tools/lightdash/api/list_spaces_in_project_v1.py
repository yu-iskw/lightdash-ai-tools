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
from lightdash_ai_tools.lightdash.models.list_spaces_in_project_v1 import (
    ListSpacesInProjectV1Response,
)


class ListSpacesInProject(BaseLightdashApiCaller[ListSpacesInProjectV1Response]):
    """Gets all spaces in a project"""
    request_type = RequestType.GET

    def _request(self, project_uuid: str) -> Dict[str, Any]:
        """
        Retrieve all spaces in the current project.

        Returns:
            ListSpacesInProjectResponse: List of spaces in the project.
        """
        formatted_path = "/api/v1/projects/{projectUuid}/spaces".format(projectUuid=project_uuid)
        response_data = self.lightdash_client.call(self.request_type, formatted_path)
        return response_data

    def _parse_response(self, response_data: Dict[str, Any]) -> ListSpacesInProjectV1Response:
        return ListSpacesInProjectV1Response(**response_data)
