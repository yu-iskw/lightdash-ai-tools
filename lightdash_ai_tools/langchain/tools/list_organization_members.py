from typing import List, Optional, Type

from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool
from pydantic import BaseModel

from lightdash_ai_tools.lightdash.client import LightdashClient
from lightdash_ai_tools.lightdash.services.list_organization_members_v1 import (
    ListOrganizationMembersV1Service,
)


class ListOrganizationMembersInput(BaseModel):
    """Input for the ListOrganizationMembers tool."""


class ListOrganizationMembersTool(BaseTool):
    """List organization members"""

    name: str = "list_organization_members"
    description: str = "List all members of the current user's organization"
    args_schema: Type[BaseModel] = ListOrganizationMembersInput
    return_direct: bool = False

    lightdash_client: LightdashClient

    def _run(self, run_manager: Optional[CallbackManagerForToolRun] = None) -> List[str]:
        """
        Run method for listing organization members.

        Returns:
            JSON string of organization members
        """
        service = ListOrganizationMembersV1Service(client=self.lightdash_client)
        organization_members = service.get_all_members()
        return [organization_member.model_dump_json() for organization_member in organization_members]

    async def _arun(
      self,
      run_manager: Optional[AsyncCallbackManagerForToolRun] = None) -> List[str]:
        return self._run(run_manager=run_manager.get_sync())
