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

from typing import List, Optional, Type

from pydantic import BaseModel, Field

from lightdash_ai_tools.lightdash.api.get_explore_v1 import GetExploreV1
from lightdash_ai_tools.lightdash.client import LightdashClient
from lightdash_ai_tools.lightdash.models.compile_query_v1 import (
    Filters,
    SortField,
)
from lightdash_ai_tools.lightdash.models.get_explore_v1 import GetExploreV1Results


class CompileQueryInput(BaseModel):
    """Input for the CompileQuery tool."""
    projectUuid: str = Field(..., description="UUID of the Lightdash project")
    exploreId: str = Field(..., description="ID of the explore to compile the query for")
    exploreName: str = Field(..., description="Name of the explore")
    dimensions: Optional[List[str]] = Field(default_factory=list, description="List of dimension field IDs")
    metrics: Optional[List[str]] = Field(default_factory=list, description="List of metric field IDs")
    filters: Optional[Filters] = Field(default=None, description="Query filters")
    sorts: Optional[List[SortField]] = Field(default=None, description="Sorting configuration")
    limit: Optional[int] = Field(default=500, description="Limit of results")


from lightdash_ai_tools.lightdash.api.compile_query_v1 import CompileQueryV1
from lightdash_ai_tools.lightdash.models.compile_query_v1 import CompileQueryRequestV1


class CompileQuery:
    """Controller for compiling Lightdash queries."""

    name: str = "compile_query"
    description: str = "Compile a query in a Lightdash project."
    input_schema: Type[BaseModel] = CompileQueryInput

    def __init__(self, lightdash_client: LightdashClient):
        """Initialize the controller with a Lightdash client."""
        self.lightdash_client = lightdash_client

    def call(
        self,
        project_uuid: str,
        explore_id: str,
        explore_name: str,
        dimensions: Optional[List[str]] = None,
        metrics: Optional[List[str]] = None,
        filters: Optional[Filters] = None,
        sorts: Optional[List[SortField]] = None,
        limit: Optional[int] = 500,
    ) -> str:
        """Compile a Lightdash query."""
        request_body = CompileQueryRequestV1(
            projectUuid=project_uuid,
            exploreId=explore_id,
            exploreName=explore_name,
            dimensions=dimensions or [],
            metrics=metrics or [],
            filters=filters,
            sorts=sorts or [],
            limit=limit or 500,
        )
        service = CompileQueryV1(lightdash_client=self.lightdash_client)
        response = service.call(project_uuid, explore_id, request_body)
        return response.results

    async def acall(
        self,
        project_uuid: str,
        explore_id: str,
        explore_name: str,
        dimensions: Optional[List[str]] = None,
        metrics: Optional[List[str]] = None,
        filters: Optional[Filters] = None,
        sorts: Optional[List[SortField]] = None,
        limit: Optional[int] = 500,
    ) -> str:
        """Asynchronously compile a Lightdash query."""
        request_body = CompileQueryRequestV1(
            projectUuid=project_uuid,
            exploreId=explore_id,
            exploreName=explore_name,
            dimensions=dimensions or [],
            metrics=metrics or [],
            filters=filters,
            sorts=sorts or [],
            limit=limit or 500,
        )
        service = CompileQueryV1(lightdash_client=self.lightdash_client)
        response = await service.acall(project_uuid, explore_id, request_body)
        return response.results
