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


from lightdash_ai_tools.lightdash.api.get_explore_v1 import GetExploreV1
from lightdash_ai_tools.lightdash.client import LightdashClient
from lightdash_ai_tools.lightdash.models.get_explore_v1 import GetExploreV1Results


class GetExploreController:
    """Controller for the GetExplore tool"""

    def __init__(self, client: LightdashClient):
        """Initialize the controller"""
        self.client = client

    def __call__(self, project_uuid: str, explore_uuid: str) -> GetExploreV1Results:
        """Get a specific explore in a project"""
        response = GetExploreV1(client=self.client).call(project_uuid, explore_uuid)
        return response.results
