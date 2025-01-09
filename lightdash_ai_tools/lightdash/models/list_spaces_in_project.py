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

from pydantic import BaseModel, ConfigDict, Field, SecretStr


class UserAccess(BaseModel):
    """User access model"""
    model_config = ConfigDict(extra='allow')

    inheritedFrom: Optional[str] = Field(..., description="The source of the user's access")
    inheritedRole: Optional[str] = Field(..., description="The role inherited from the organization")
    projectRole: Optional[str] = Field(..., description="The role assigned for the project")
    hasDirectAccess: Optional[bool] = Field(..., description="Indicates if the user has direct access")
    role: str = Field(..., description="The user's role")
    lastName: Optional[str] = Field(..., description="The user's last name")
    firstName: Optional[str] = Field(..., description="The user's first name")
    userUuid: Optional[str] = Field(..., description="The UUID of the user")
    # NOTE: Hide email for privacy
    email: SecretStr = Field(..., description="The user's email address")

class Space(BaseModel):
    """Space model"""

    model_config = ConfigDict(extra='allow')

    name: str = Field(..., description="The name of the space")
    uuid: str = Field(..., description="The UUID of the space")
    projectUuid: str = Field(..., description="The UUID of the project")
    organizationUuid: str = Field(..., description="The UUID of the organization")
    pinnedListUuid: Optional[str] = Field(..., description="The UUID of the pinned list")
    slug: Optional[str] = Field(..., description="The slug of the space")
    isPrivate: bool = Field(..., description="Indicates if the space is private")
    pinnedListOrder: Optional[float] = Field(..., description="Order of the pinned list")
    dashboardCount: Optional[float] = Field(..., description="Count of dashboards in the space")
    chartCount: Optional[float] = Field(..., description="Count of charts in the space")
    access: List[str] = Field(..., description="List of access types")
    userAccess: UserAccess = Field(..., description="User access details")

class ListSpacesInProjectResponse(BaseModel):
    """Response model for listing spaces in a project"""
    results: List[Space] = Field(..., description='The list of spaces')
    status: str = Field(..., description='The status of the request')
