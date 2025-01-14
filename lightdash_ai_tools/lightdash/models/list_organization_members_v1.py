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


class OrganizationMemberModel(BaseModel):
    """Response model for an organization member."""

    model_config = ConfigDict(extra="ignore")

    userUuid: str = Field(..., description="Unique identifier for the user")
    userCreatedAt: str = Field(..., description="Timestamp when the user was created")
    userUpdatedAt: str = Field(..., description="Timestamp when the user was last updated")
    firstName: str = Field(..., description="User's first name")
    lastName: str = Field(..., description="User's last name")
    organizationUuid: str = Field(..., description="Unique identifier for the organization")
    role: str = Field(..., description="User's role in the organization")
    isActive: bool = Field(default=True, description="Whether the user is active")
    isPending: Optional[bool] = Field(default=True, description="Whether the user's invitation is pending")
    isInviteExpired: Optional[bool] = Field(default=True, description="Whether the user's invitation has expired")
    # NOTE: Hide email for privacy
    email: SecretStr = Field(..., description="User's email address")


class PaginationModel(BaseModel):
    """Model for pagination information."""
    model_config = ConfigDict(extra="ignore")

    page: int = Field(..., description="Current page number")
    pageSize: int = Field(..., description="Number of results per page")
    totalResults: int = Field(..., description="Total number of results available")
    totalPageCount: int = Field(..., description="Total number of pages available")

class ListOrganizationMembersV1Results(BaseModel):
    """Results model for ListOrganizationMembers API call."""
    model_config = ConfigDict(extra="ignore")

    pagination: PaginationModel = Field(..., description="Pagination information")
    data: List[OrganizationMemberModel] = Field(..., description="List of organization members")

class ListOrganizationMembersV1Response(BaseModel):
    """Response model for ListOrganizationMembers API call."""
    results: ListOrganizationMembersV1Results = Field(..., description="List of organization members")
    status: str = Field(..., description="Status of the API response")
