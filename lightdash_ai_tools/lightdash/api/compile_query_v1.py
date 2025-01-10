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
from lightdash_ai_tools.lightdash.models.compile_query_v1 import (
    CompileQueryRequestV1,
    CompileQueryResponseV1,
)


class CompileQueryV1(BaseLightdashApiCaller[CompileQueryResponseV1]):
    """Compile a query in a Lightdash project"""
    request_type = RequestType.POST

    def _request(
        self,
        project_uuid: str,
        explore_id: str,
        body: CompileQueryRequestV1
    ) -> Dict[str, Any]:
        """
        Compile a query for a specific explore in a project.

        Args:
            project_uuid (str): The UUID of the project
            explore_id (str): The ID of the explore
            body (Dict[str, Any]): Query compilation parameters

        Returns:
            Dict[str, Any]: Compiled query results
        """
        formatted_path = f"/api/v1/projects/{project_uuid}/explores/{explore_id}/compileQuery"
        response_data = self.lightdash_client.call(
          self.request_type, formatted_path, data=body.model_dump(exclude=["projectUuid", "exploreId"]))
        return response_data

    def _parse_response(self, response_data: Dict[str, Any]) -> CompileQueryResponseV1:
        return CompileQueryResponseV1(**response_data)
