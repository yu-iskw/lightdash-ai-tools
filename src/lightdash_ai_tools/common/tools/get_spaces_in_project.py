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

from lightdash_ai_tools.lightdash.api.list_spaces_in_project_v1 import (
    ListSpacesInProjectV1,
)
from lightdash_ai_tools.lightdash.client import LightdashClient
from lightdash_ai_tools.lightdash.models.list_spaces_in_project_v1 import (
    ListSpacesInProjectV1Results,
)


class GetSpacesInProjectInput(BaseModel):
    project_uuid: str


class GetSpacesInProject:
    name: str = "get_spaces_in_project"
    description: str = "Get spaces in a project"
    input_schema = GetSpacesInProjectInput

    def __init__(self, lightdash_client: LightdashClient):
        self.lightdash_client = lightdash_client

    def call(self, project_uuid: str) -> List[ListSpacesInProjectV1Results]:
        service = ListSpacesInProjectV1 (client=self.lightdash_client)
        return service.call(project_uuid=project_uuid)

    async def acall(self, project_uuid: str) -> List[ListSpacesInProjectV1Results]:
        service = ListSpacesInProjectV1(client=self.lightdash_client)
        return await service.acall(project_uuid=project_uuid)
