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
from typing import List, Type

from crewai.tools import BaseTool
from pydantic import BaseModel

from lightdash_ai_tools.common.tools.get_projects import GetProjects
from lightdash_ai_tools.lightdash.client import LightdashClient
from lightdash_ai_tools.lightdash.models.list_organization_projects_v1 import (
    ListOrganizationProjectsV1Results,
)


class GetProjectsTool(BaseTool):
    """Get all projects in the organization"""

    name: str = GetProjects.name
    description: str = GetProjects.description
    args_schema: Type[BaseModel] = GetProjects.input_schema

    lightdash_client: LightdashClient

    def _run(self) -> List[ListOrganizationProjectsV1Results]:
        """
        Run method for getting all projects in the organization.

        Returns:
            List of projects in the organization
        """
        try:
            tool = GetProjects(lightdash_client=self.lightdash_client)
            return tool.call()
        except Exception as e:
            error_message = textwrap.dedent(f"""\
              Error retrieving projects in organization.
              Exception: {type(e).__name__}: {e}
            """).strip()
            raise RuntimeError(error_message) from e
