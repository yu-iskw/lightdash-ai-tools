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
from typing import List, Optional, Type

from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool, ToolException
from pydantic import BaseModel

from lightdash_ai_tools.common.tools.get_organization_members import (
    GetOrganizationMembers,
)
from lightdash_ai_tools.lightdash.client import LightdashClient
from lightdash_ai_tools.lightdash.models.list_organization_members_v1 import (
    ListOrganizationMembersV1Results,
)


class GetOrganizationMembersTool(BaseTool):
    """Get members of the organization"""

    name: str = GetOrganizationMembers.name
    description: str = GetOrganizationMembers.description
    args_schema: Type[BaseModel] = GetOrganizationMembers.input_schema
    return_direct: bool = False
    handle_tool_error: bool = True
    handle_validation_error: bool = True

    lightdash_client: LightdashClient

    def _run(
        self,
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> List[ListOrganizationMembersV1Results]:
        """
        Run method for getting members of the organization.

        Returns:
            List of members in the organization
        """
        try:
            tool = GetOrganizationMembers(lightdash_client=self.lightdash_client)
            return tool.call()
        except Exception as e:
            error_message = textwrap.dedent(f"""\
              Error retrieving organization members.
              Exception: {type(e).__name__}: {e}
            """).strip()
            raise ToolException(error_message) from e

    async def _arun(
        self,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> List[ListOrganizationMembersV1Results]:
        """
        Asynchronously retrieve members of the organization.

        :param run_manager: Optional async callback manager
        :return: List of members in the organization
        """
        try:
            tool = GetOrganizationMembers(lightdash_client=self.lightdash_client)
            return await tool.acall()
        except Exception as e:
            error_message = textwrap.dedent(f"""\
              Error retrieving organization members asynchronously.
              Exception: {type(e).__name__}: {e}
            """).strip()
            raise ToolException(error_message) from e
