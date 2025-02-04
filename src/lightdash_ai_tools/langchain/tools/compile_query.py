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
from typing import List, Optional

from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool, ToolException
from pydantic import BaseModel

from lightdash_ai_tools.common.tools.compile_query import (
    CompileQuery,
    CompileQueryInput,
)
from lightdash_ai_tools.lightdash.client import LightdashClient
from lightdash_ai_tools.lightdash.models.compile_query_v1 import (
    Filters,
    SortField,
)


class CompileQueryTool(BaseTool):
    """Tool to compile a Lightdash query."""
    name: str = CompileQuery.name
    description: str = CompileQuery.description
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
    ) -> str:
        """
        Compile a Lightdash query.

        :return: Compiled query results
        """
        try:
            tool = CompileQuery(lightdash_client=self.lightdash_client)
            return tool.call(
                project_uuid=projectUuid,
                explore_id=exploreId,
                explore_name=exploreName,
                dimensions=dimensions,
                metrics=metrics,
                filters=filters,
                sorts=sorts,
                limit=limit
            )
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
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        """
        Asynchronously compile a Lightdash query.

        :return: Compiled query results
        """
        try:
            tool = CompileQuery(lightdash_client=self.lightdash_client)
            return await tool.acall(
                project_uuid=projectUuid,
                explore_id=exploreId,
                explore_name=exploreName,
                dimensions=dimensions,
                metrics=metrics,
                filters=filters,
                sorts=sorts,
                limit=limit
            )
        except Exception as e:
            error_message = textwrap.dedent(f"""\
              Error compiling Lightdash query asynchronously with project_uuid: {projectUuid} and explore_id: {exploreId}.
              Exception: {type(e).__name__}: {e}
            """).strip()
            raise ToolException(error_message) from e
