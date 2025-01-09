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

from lightdash_ai_tools.lightdash.api.base import BaseLightdashApiCaller
from lightdash_ai_tools.lightdash.client import RequestType
from lightdash_ai_tools.lightdash.models.get_explore_v1 import GetExploreV1Response


class GetExploreV1(BaseLightdashApiCaller[GetExploreV1Response]):
    """Get a specific explore for a project"""
    request_type = RequestType.GET
    response_model = GetExploreV1Response

    def call(self, project_uuid: str, explore_id: str) -> GetExploreV1Response:
        """
        Retrieve a specific explore for a project.

        Args:
            project_uuid (str): The UUID of the project.
            explore_id (str): The ID of the explore to retrieve.

        Returns:
            GetExploreV1Response: Details of the explore.
        """
        formatted_path = f"/api/v1/projects/{project_uuid}/explores/{explore_id}"
        return super()._call(path=formatted_path)
