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
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class GroupPagination(BaseModel):
    model_config = ConfigDict(extra="ignore")

    page: float = Field(..., alias="page")
    pageSize: float = Field(..., alias="pageSize")
    totalResults: float = Field(..., alias="totalResults")
    totalPageCount: float = Field(..., alias="totalPageCount")


class Group(BaseModel):
    model_config = ConfigDict(extra="ignore")

    organizationUuid: str = Field(..., alias="organizationUuid")
    updatedByUserUuid: Optional[str] = Field(None, alias="updatedByUserUuid")
    updatedAt: Optional[datetime] = Field(None, alias="updatedAt")
    createdByUserUuid: Optional[str] = Field(None, alias="createdByUserUuid")
    createdAt: Optional[datetime] = Field(None, alias="createdAt")
    name: str = Field(..., alias="name")
    uuid: str = Field(..., alias="uuid")


class ListGroupsInOrganizationV1Results(BaseModel):
    model_config = ConfigDict(extra="ignore")

    pagination: GroupPagination = Field(..., alias="pagination")
    data: List[Group] = Field(..., alias="data")


class ListGroupsInOrganizationV1Response(BaseModel):
    results: ListGroupsInOrganizationV1Results = Field(..., alias="results")
    status: str = Field(..., alias="status")
