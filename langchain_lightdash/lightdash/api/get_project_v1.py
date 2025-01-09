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



from langchain_lightdash.lightdash.api.base import BaseLightdashApiCaller
from langchain_lightdash.lightdash.client import RequestType
from langchain_lightdash.lightdash.models.get_project_v1 import GetProjectResponse


class GetProjectV1(BaseLightdashApiCaller[GetProjectResponse]):
    """Get a Lightdash Project"""
    request_type = RequestType.GET
    path = "/api/v1/projects/{project_uuid}"
    response_model = GetProjectResponse

    def call(self, project_uuid: str) -> GetProjectResponse:
        """
        Retrieve a specific project by its UUID.

        Args:
            project_uuid (str): The UUID of the project to retrieve.

        Returns:
            GetProjectResponse: Details of the retrieved project.
        """
        formatted_path = self.path.format(project_uuid=project_uuid)
        self.path = formatted_path
        return super()._call()