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


class OrganizationProject(BaseModel):
    """Organization project model"""
    model_config = ConfigDict(extra='allow')

    warehouseType: str = Field(..., description='The type of warehouse to use')
    upstreamProjectUuid: Optional[str] = Field(..., description='The UUID of the upstream project')
    createdByUserUuid: Optional[str] = Field(..., description='The UUID of the user who created the project')
    type: str = Field(..., description='The type of project')
    name: str = Field(..., description='The name of the project')
    projectUuid: str = Field(..., description='The UUID of the project')


class ListOrganizationProjectsResponse(BaseModel):
    """Response model for listing organization projects"""
    results: List[OrganizationProject] = Field(..., description='The list of projects')
    status: str = Field(..., description='The status of the request')
