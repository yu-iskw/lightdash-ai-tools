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

from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class GetExploresV1Results(BaseModel):
    """Model representing an explore in Lightdash"""
    model_config = ConfigDict(extra="allow")

    name: str = Field(..., description="Name of the explore")
    label: Optional[str] = Field(default=None, description="Label of the explore")
    groupLabel: Optional[str] = Field(default=None, description="Group label of the explore")
    type: str = Field(..., description="Type of the explore")
    tags: List[str] = Field(default_factory=list, description="Tags associated with the explore")
    databaseName: Optional[str] = Field(default=None, description="Database name of the explore")
    schemaName: Optional[str] = Field(default=None, description="Schema name of the explore")
    description: Optional[str] = Field(default=None, description="Description of the explore")

class GetExploresV1Response(BaseModel):
    """Response model for GetExplores API"""
    results: List[GetExploresV1Results] = Field(..., description="List of explores")
    status: str = Field(..., description="Status of the API response")
