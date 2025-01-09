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

from typing import List

from langchain_core.tools import BaseTool

from lightdash_ai_tools.langchain.tools.get_project import GetProject
from lightdash_ai_tools.langchain.tools.get_projects import GetProjects
from lightdash_ai_tools.langchain.tools.get_spaces_in_project import GetSpacesInProject
from lightdash_ai_tools.langchain.tools.list_organization_members import (
    ListOrganizationMembersTool,
)
from lightdash_ai_tools.lightdash.client import LightdashClient


def get_all_readable_tools(lightdash_client: LightdashClient) -> List[BaseTool]:
    """Get the read-only tools."""
    return [
        GetProject(lightdash_client=lightdash_client),
        GetProjects(lightdash_client=lightdash_client),
        GetSpacesInProject(lightdash_client=lightdash_client),
        ListOrganizationMembersTool(lightdash_client=lightdash_client),
    ]


# def get_all_writable_tools(lightdash_client: LightdashClient) -> List[BaseTool]:
#     """Get the write tools."""
#     return []

__all__ = [
    "GetProject",
    "GetProjects",
    "GetSpacesInProject",
    "ListOrganizationMembersTool",
]
