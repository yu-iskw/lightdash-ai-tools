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

import textwrap
from typing import Any, Dict, List, Optional

from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool, ToolException
from pydantic import BaseModel, Field

from lightdash_ai_tools.lightdash.api.compile_query_v1 import CompileQueryV1
from lightdash_ai_tools.lightdash.client import LightdashClient
from lightdash_ai_tools.lightdash.models.compile_query_v1 import (
    CompileQueryRequestV1,
    Filters,
    SortField,
)


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

class CompileQueryTool(BaseTool):
    """Tool to compile a Lightdash query."""
    name: str = "compile_lightdash_query"
    description: str = (
        "Compiles a query in a Lightdash project. "
        "Useful for preparing and validating queries before execution. "
        "Requires project UUID, explore ID, and explore name. "
        "Optional parameters allow detailed query configuration."
    )
    args_schema: type[BaseModel] = CompileQueryInput
    return_direct: bool = False
    handle_tool_error: bool = True
    handle_validation_error: bool = True

    lightdash_client: LightdashClient

    def _run(
        self,
        projectUuid: str,
        exploreId: str,
        exploreName: str,
        dimensions: Optional[List[str]] = None,
        metrics: Optional[List[str]] = None,
        filters: Optional[Filters] = None,
        sorts: Optional[List[SortField]] = None,
        limit: Optional[int] = 500,
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> Dict[str, Any]:
        """
        Compile a Lightdash query.

        :return: Compiled query results
        """
        # Construct the request body using the CompileQueryRequestV1 model
        request_body = CompileQueryRequestV1(
            projectUuid=projectUuid,
            exploreId=exploreId,
            exploreName=exploreName,
            dimensions=dimensions or [],
            metrics=metrics or [],
            filters=filters,
            sorts=sorts,
            limit=limit or 500,
        )

        # Call the Lightdash API to compile the query
        try:
            response_data = CompileQueryV1(lightdash_client=self.lightdash_client).call(projectUuid, exploreId, request_body)
            return response_data.results
        except Exception as e:
            error_message = textwrap.dedent(f"""\
              Error compiling Lightdash query with project_uuid: {projectUuid} and explore_id: {exploreId}.
              Exception: {type(e).__name__}: {e}
            """).strip()
            raise ToolException(error_message) from e

    async def _arun(
        self,
        projectUuid: str,
        exploreId: str,
        exploreName: str,
        dimensions: Optional[List[str]] = None,
        metrics: Optional[List[str]] = None,
        filters: Optional[Filters] = None,
        sorts: Optional[List[SortField]] = None,
        limit: Optional[int] = 500,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> Dict[str, Any]:
        """Async version of the run method."""
        try:
            return self._run(
                projectUuid,
                exploreId,
                exploreName,
                dimensions,
                metrics,
                filters,
                sorts,
                limit
            )
        except Exception as e:
            error_message = textwrap.dedent(f"""\
              Error compiling Lightdash query with project_uuid: {projectUuid} and explore_id: {exploreId}.
              Exception: {type(e).__name__}: {e}
            """).strip()
            raise ToolException(error_message) from e
