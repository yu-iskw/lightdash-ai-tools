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

from typing import List

from lightdash_ai_tools.lightdash.api.list_spaces_in_project_v1 import (
    ListSpacesInProject,
)
from lightdash_ai_tools.lightdash.client import LightdashClient
from lightdash_ai_tools.lightdash.models.list_spaces_in_project_v1 import (
    ListSpacesInProjectV1Results,
)


class GetSpacesInProjectController:
    """Controller for the GetSpacesInProject tool"""

    def __init__(self, lightdash_client: LightdashClient):
        """Initialize the controller"""
        self.lightdash_client = lightdash_client

    def __call__(self, project_uuid: str) -> List[ListSpacesInProjectV1Results]:
        """Call the controller"""
        response = ListSpacesInProject(lightdash_client=self.lightdash_client).call(project_uuid)
        results = response.results
        return results
