import textwrap
from typing import List, Optional, Type

from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool, ToolException
from pydantic import BaseModel, Field

from lightdash_ai_tools.lightdash.api.get_explores_v1 import GetExploresV1
from lightdash_ai_tools.lightdash.client import LightdashClient
from lightdash_ai_tools.lightdash.models.get_explores_v1 import ExploreModel


class GetExploresInput(BaseModel):
    """Input for the GetExplores tool."""
    project_uuid: str = Field(description="The UUID of the project to get explores for")


class GetExplores(BaseTool):
    """Get explores in a project"""

    name: str = "get_explores"
    description: str = "Get explores (tables) in a project."
    args_schema: Type[BaseModel] = GetExploresInput
    return_direct: bool = False
    handle_tool_error: bool = True

    lightdash_client: LightdashClient

    def _run(self, project_uuid: str, run_manager: Optional[CallbackManagerForToolRun] = None) -> List[ExploreModel]:
        try:
            response = GetExploresV1(client=self.lightdash_client).call(project_uuid)
            return response.results
        except Exception as e:
            error_message = textwrap.dedent(f"""\
              Error retrieving explores with project_uuid: {project_uuid}.
              Exception: {type(e).__name__}: {e}
            """).strip()
            raise ToolException(error_message) from e

    async def _arun(
      self,
      project_uuid: str,
      run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> List[ExploreModel]:
        try:
            if run_manager is not None:
                return self._run(project_uuid, run_manager=run_manager.get_sync())
            return self._run(project_uuid)
        except Exception as e:
            error_message = textwrap.dedent(f"""\
              Error retrieving explores asynchronously with project_uuid: {project_uuid}.
              Exception: {type(e).__name__}: {e}
            """).strip()
            raise ToolException(error_message) from e
