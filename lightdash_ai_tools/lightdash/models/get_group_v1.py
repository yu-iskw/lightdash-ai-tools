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

from datetime import datetime
from typing import List  # Import List to fix the undefined variable error
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class GroupMember(BaseModel):
    """Model for a member of the group."""
    model_config = ConfigDict(extra='ignore')

    userUuid: str = Field(..., description="Unique identifier for the user")
    firstName: str = Field(..., description="User's first name")
    lastName: str = Field(..., description="User's last name")
    role: Optional[str] = Field(None, description="User's role in the group")
    isActive: Optional[bool] = Field(None, description="Whether the user is active")

class GetGroupV1Result(BaseModel):
    """Model for the get group API response result."""
    model_config = ConfigDict(extra='ignore')

    organizationUuid: str = Field(..., description="Unique identifier of the organization")
    updatedByUserUuid: Optional[str] = Field(None, description="UUID of the user who last updated the group")
    updatedAt: Optional[datetime] = Field(None, description="Timestamp of the last update")
    createdByUserUuid: Optional[str] = Field(None, description="UUID of the user who created the group")
    createdAt: Optional[datetime] = Field(None, description="Timestamp of group creation")
    name: str = Field(..., description="Name of the group")
    uuid: str = Field(..., description="Unique identifier of the group")
    memberUuids: Optional[List[str]] = Field(..., default_factory=list, description="List of member UUIDs in the group")
    members: Optional[List[GroupMember]] = Field(..., default_factory=list, description="List of members in the group")

class GetGroupV1Response(BaseModel):
    """Model for the complete get group API response."""
    results: GetGroupV1Result
    status: str = Field(..., description="Status of the API response")
