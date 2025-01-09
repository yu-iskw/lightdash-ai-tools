import textwrap
from typing import List, Optional, Type

from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool, ToolException
from pydantic import BaseModel

from lightdash_ai_tools.lightdash.client import LightdashClient
from lightdash_ai_tools.lightdash.models.list_organization_members_v1 import (
    OrganizationMemberModel,
)
from lightdash_ai_tools.lightdash.services.list_organization_members_v1 import (
    ListOrganizationMembersV1Service,
)


class GetOrganizationMembersToolInput(BaseModel):
    """Input for the GetOrganizationMembersTool tool."""


class GetOrganizationMembersTool(BaseTool):
    """Get organization members"""

    name: str = "get_organization_members"
    description: str = "Get all members of the current user's organization"
    args_schema: Type[BaseModel] = GetOrganizationMembersToolInput
    return_direct: bool = False
    handle_tool_error: bool = True

    lightdash_client: LightdashClient

    def _run(self, run_manager: Optional[CallbackManagerForToolRun] = None) -> List[OrganizationMemberModel]:
        """
        Run method for getting organization members.

        Returns:
            List of organization members
        """
        try:
            service = ListOrganizationMembersV1Service(client=self.lightdash_client)
            return service.get_all_members()
        except Exception as e:
            error_message = textwrap.dedent(f"""\
              Error retrieving organization members.
              Exception: {type(e).__name__}: {e}
            """).strip()
            raise ToolException(error_message) from e

    async def _arun(
      self,
      run_manager: Optional[AsyncCallbackManagerForToolRun] = None) -> List[OrganizationMemberModel]:
        try:
            if run_manager is not None:
                return self._run(run_manager=run_manager.get_sync())
            return self._run()
        except Exception as e:
            error_message = textwrap.dedent(f"""\
              Error retrieving organization members asynchronously.
              Exception: {type(e).__name__}: {e}
            """).strip()
            raise ToolException(error_message) from e
