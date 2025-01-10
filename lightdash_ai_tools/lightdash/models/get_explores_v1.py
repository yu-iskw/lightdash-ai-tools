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
