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

from pydantic import BaseModel

from lightdash_ai_tools.lightdash.api.list_organization_projects_v1 import (
    ListOrganizationProjectsV1,
)
from lightdash_ai_tools.lightdash.client import LightdashClient
from lightdash_ai_tools.lightdash.models.list_organization_projects_v1 import (
    ListOrganizationProjectsV1Results,
)


class GetProjectsInput(BaseModel):
    pass


class GetProjects:
    """Controller for the GetProjects tool"""

    name: str = "get_projects"
    description: str = "Get all projects in the organization"
    input_schema = GetProjectsInput

    def __init__(self, lightdash_client: LightdashClient):
        """Initialize the controller"""
        self.lightdash_client = lightdash_client

    def call(self) -> List[ListOrganizationProjectsV1Results]:
        """Call the controller"""
        service = ListOrganizationProjectsV1(lightdash_client=self.lightdash_client)
        return service.call().results

    async def acall(self) -> List[ListOrganizationProjectsV1Results]:
        """Async call the controller"""
        service = ListOrganizationProjectsV1(lightdash_client=self.lightdash_client)
        return (await service.acall()).results
