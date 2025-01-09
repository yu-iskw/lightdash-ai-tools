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

from langchain_lightdash.langchain.tools.get_project import GetProject
from langchain_lightdash.lightdash.client import LightdashClient


def get_all_readable_tools(lightdash_client: LightdashClient) -> List[BaseTool]:
    """Get the read-only tools."""
    return [
        GetProject(lightdash_client=lightdash_client)
    ]


# def get_all_writable_tools(lightdash_client: LightdashClient) -> List[BaseTool]:
#     """Get the write tools."""
#     return []
