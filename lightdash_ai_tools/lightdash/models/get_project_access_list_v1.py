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


class ProjectAccessMemberModel(BaseModel):
    """Model representing a member's access to a project."""
    model_config = ConfigDict(extra="allow")

    lastName: Optional[str] = Field(default=None, description="Last name of the user")
    firstName: Optional[str] = Field(default=None, description="First name of the user")
    role: str = Field(description="User's role in the project", examples=["viewer", "editor", "admin"])
    projectUuid: str = Field(description="UUID of the project")
    userUuid: str = Field(description="UUID of the user")
    email: SecretStr = Field(description="Email of the user")


class GetProjectAccessListV1Response(BaseModel):
    """Response model for GetProjectAccessList API."""
    results: List[ProjectAccessMemberModel] = Field(default_factory=list, description="List of project access members")
    status: str = Field(description="Status of the API response", default="ok")
