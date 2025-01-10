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


from typing import Any, Dict, Optional

from lightdash_ai_tools.lightdash.api.base import BaseLightdashApiCaller
from lightdash_ai_tools.lightdash.client import RequestType
from lightdash_ai_tools.lightdash.models.get_group_v1 import GetGroupV1Response


class GetGroupV1(BaseLightdashApiCaller[GetGroupV1Response]):
    """Get group details"""
    request_type = RequestType.GET

    def _request(self,
                 group_uuid: str,
                 include_members: Optional[int] = None,
                 offset: Optional[int] = None
                 ) -> Dict[str, Any]:
        """
        Retrieve a specific group.

        Args:
            group_uuid (str): The UUID of the group to retrieve.
            include_members (Optional[int]): Number of members to include.
            offset (Optional[int]): Offset of members to include.

        Returns:
            GetGroupV1Response: Details of the group.
        """
        formatted_path = f"/api/v1/groups/{group_uuid}"
        params = {}
        if include_members is not None:
            params['includeMembers'] = include_members
        if offset is not None:
            params['offset'] = offset
        return self.lightdash_client.call(self.request_type, formatted_path, parameters=params)

    def _parse_response(self, response_data: Dict[str, Any]) -> GetGroupV1Response:
        return GetGroupV1Response(**response_data)
