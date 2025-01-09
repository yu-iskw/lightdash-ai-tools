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


from typing import Optional

from pydantic import BaseModel, Field


class GetProjectResults(BaseModel):
    """A Lightdash Project"""

    createdByUserUuid: Optional[str] = Field(None, description="The UUID of the user who created the project")
    schedulerTimezone: Optional[str] = Field(None, description="The timezone for the scheduler")
    dbtVersion: Optional[str] = Field(None, description="The version of DBT being used")
    upstreamProjectUuid: Optional[str] = Field(None, description="The UUID of the upstream project")
    pinnedListUuid: Optional[str] = Field(None, description="The UUID of the pinned list")
    type: str = Field(default="DEFAULT", description="The type of the project")
    name: str = Field(..., description="The name of the project")
    projectUuid: str = Field(..., description="The UUID of the project")
    organizationUuid: str = Field(..., description="The UUID of the organization")


class GetProjectResponse(BaseModel):
    """Response model for retrieving a project"""
    results: GetProjectResults = Field(..., description="The project details")
    status: str = Field(..., description="The status of the request")
