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

from typing import Optional

from lightdash_ai_tools.lightdash.api.get_group_v1 import GetGroupV1
from lightdash_ai_tools.lightdash.client import LightdashClient
from lightdash_ai_tools.lightdash.models.get_group_v1 import GetGroupV1Response


class GetGroupV1Controller:
    """Controller for getting group details."""

    def __init__(self, lightdash_client: LightdashClient):
        """
        Initialize the get group controller.

        :param lightdash_client: Lightdash client for making API calls
        """
        self.lightdash_client = lightdash_client

    def __call__(
        self,
        group_uuid: str,
        include_members: Optional[int] = None,
        offset: Optional[int] = None
    ) -> GetGroupV1Response:
        """
        Get details of a specific group.

        :param group_uuid: Unique identifier of the group
        :param include_members: Number of members to include
        :param offset: Offset of members to include
        :return: Group details response
        """
        api = GetGroupV1(lightdash_client=self.lightdash_client)
        return api.call(group_uuid=group_uuid, include_members=include_members, offset=offset)
