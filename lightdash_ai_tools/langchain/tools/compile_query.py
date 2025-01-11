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
from typing import Optional

from langchain_core.callbacks import AsyncCallbackManagerForToolRun
from langchain_core.tools import BaseTool, ToolException
from pydantic import BaseModel

from lightdash_ai_tools.lightdash.api.compile_query_v1 import CompileQueryV1
from lightdash_ai_tools.lightdash.client import LightdashClient
from lightdash_ai_tools.lightdash.models.compile_query_v1 import (
    CompileQueryRequestV1,
    Filters,
    SortField,
)

# class CompileQueryInput(BaseModel):
#     """Input for the CompileQuery tool."""
#     project_uuid: str = Field(..., description="UUID of the Lightdash project")
#     explore_id: str = Field(..., description="ID of the explore to compile the query for")
#     explore_name: str = Field(..., description="Name of the explore")
#     dimensions: Optional[list[str]] = Field(default=None, description="List of dimension field IDs")
#     metrics: Optional[list[str]] = Field(default=None, description="List of metric field IDs")
#     filters: Optional[Dict[str, Any]] = Field(default=None, description="Query filters")
#     sorts: Optional[list[Dict[str, Any]]] = Field(default=None, description="Sorting configuration")
#     limit: Optional[int] = Field(default=None, description="Limit of results")
#     timezone: Optional[str] = Field(default=None, description="Timezone for the query")
#     table_calculations: Optional[list[Dict[str, Any]]] = Field(default=None, description="Table calculations")
#     custom_dimensions: Optional[list[Dict[str, Any]]] = Field(default=None, description="Custom dimensions")
#     additional_metrics: Optional[list[Dict[str, Any]]] = Field(default=None, description="Additional metrics")
#     metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata")


class CompileQueryTool(BaseTool):
    """Tool to compile a Lightdash query."""
    name: str = "compile_lightdash_query"
    description: str = (
        "Compiles a query in a Lightdash project. "
        "Useful for preparing and validating queries before execution. "
        "Requires project UUID, explore ID, and explore name. "
        "Optional parameters allow detailed query configuration."
    )
    args_schema: type[BaseModel] = CompileQueryRequestV1
    return_direct: bool = False
    handle_tool_error: bool = True
    handle_validation_error: bool = True

    lightdash_client: LightdashClient

    def _run(
        self,
        projectUuid: Optional[str] = None,
        exploreId: Optional[str] = None,
        exploreName: Optional[str] = None,
        dimensions: Optional[list[str]] = None,
        metrics: Optional[list[str]] = None,
        filters: Optional[Filters] = None,
        sorts: Optional[list[SortField]] = None,
        limit: Optional[int] = None,
        # timezone: Optional[str] = None,
        # table_calculations: Optional[list[Dict[str, Any]]] = None,
        # custom_dimensions: Optional[list[Dict[str, Any]]] = None,
        # additional_metrics: Optional[list[Dict[str, Any]]] = None,
        # metadata: Optional[Dict[str, Any]] = None,
        # run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """
        Compile a Lightdash query.

        :return: Compiled query results
        """
        # Construct the request body using the CompileQueryRequestV1 model
        request_body = CompileQueryRequestV1(
            projectUuid=projectUuid ,
            exploreId=exploreId,
            exploreName=exploreName,
            dimensions=dimensions or [],
            metrics=metrics or [],
            # filters=Filters(
            #     dimensions=filters["dimensions"] if filters and "dimensions" in filters else {},
            #     metrics=filters["metrics"] if filters and "metrics" in filters else {},
            # ),
            # sorts=[SortField(fieldId=sort["fieldId"], descending=sort.get("descending", False)) for sort in (sorts or [])],
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
        project_uuid: str,
        explore_id: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None) -> str:
        """Async version of the run method."""
        try:
            if run_manager:
                return await self._run(project_uuid, explore_id, run_manager=run_manager)
            else:
                return await self._run(project_uuid, explore_id)
        except Exception as e:
            error_message = textwrap.dedent(f"""\
              Error compiling Lightdash query with project_uuid: {project_uuid} and explore_id: {explore_id}.
              Exception: {type(e).__name__}: {e}
            """).strip()
            raise ToolException(error_message) from e
