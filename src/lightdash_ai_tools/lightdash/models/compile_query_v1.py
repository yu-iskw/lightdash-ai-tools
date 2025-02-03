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

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class CustomDimensionRange(BaseModel):
    """Range for custom dimension binning."""
    model_config = ConfigDict(extra="ignore")

    from_: float = Field(alias="from", description="Start of the range")
    to: float = Field(description="End of the range")


class CustomDimension(BaseModel):
    """Custom dimension configuration."""
    model_config = ConfigDict(extra="ignore")

    id: Optional[str] = Field(default=None, description="ID of the custom dimension")
    name: Optional[str] = Field(default=None, description="Name of the custom dimension")
    table: Optional[str] = Field(default=None, description="Table associated with the custom dimension")
    type: Optional[str] = Field(default="bin", alias="type", description="Type of the custom dimension")
    dimension_id: Optional[str] = Field(default=None, alias="dimensionId", description="ID of the dimension")
    bin_type: Optional[str] = Field(default=None, alias="binType", description="Type of binning")
    bin_number: Optional[float] = Field(default=None, alias="binNumber", description="Number of bins")
    bin_width: Optional[float] = Field(default=None, alias="binWidth", description="Width of each bin")
    custom_range: Optional[List[CustomDimensionRange]] = Field(default=None, alias="customRange", description="Custom range for binning")


class AdditionalMetricFilter(BaseModel):
    """Filter for additional metrics."""
    model_config = ConfigDict(extra="ignore")

    values: Optional[List[Any]] = Field(default=None, description="Values for the filter")
    operator: Optional[str] = Field(default=None, description="Operator for the filter")
    id: Optional[str] = Field(default=None, description="ID of the filter")
    target: Optional[Dict[str, str]] = Field(default=None, description="Target for the filter")
    settings: Optional[Any] = Field(default=None, description="Settings for the filter")
    disabled: Optional[bool] = Field(default=None, description="Whether the filter is disabled")
    required: Optional[bool] = Field(default=None, description="Whether the filter is required")


class AdditionalMetric(BaseModel):
    """Additional metric configuration."""
    model_config = ConfigDict(extra="ignore")

    label: Optional[str] = Field(default=None, description="Label for the additional metric")
    type: Optional[str] = Field(default=None, description="Type of the additional metric")
    description: Optional[str] = Field(default=None, description="Description of the additional metric")
    sql: Optional[str] = Field(default=None, description="SQL expression for the additional metric")
    hidden: Optional[bool] = Field(default=None, description="Whether the metric is hidden")
    round: Optional[float] = Field(default=None, description="Round value for the metric")
    compact: Optional[str] = Field(default=None, description="Compact representation of the metric")
    format: Optional[str] = Field(default=None, description="Format for the metric")
    table: Optional[str] = Field(default=None, description="Table associated with the metric")
    name: Optional[str] = Field(default=None, description="Name of the additional metric")
    index: Optional[float] = Field(default=None, description="Index of the additional metric")
    filters: Optional[List[AdditionalMetricFilter]] = Field(default=None, description="Filters for the additional metric")
    base_dimension_name: Optional[str] = Field(default=None, alias="baseDimensionName", description="Base dimension name for the metric")
    uuid: Optional[str] = Field(default=None, description="UUID of the additional metric")
    percentile: Optional[float] = Field(default=None, description="Percentile for the additional metric")
    format_options: Optional[Dict[str, Any]] = Field(default=None, alias="formatOptions", description="Format options for the additional metric")


class TableCalculation(BaseModel):
    """Table calculation configuration."""
    model_config = ConfigDict(extra="ignore")

    type: Optional[str] = Field(default=None, description="Type of the table calculation")
    format: Optional[Dict[str, Any]] = Field(default=None, description="Format for the table calculation")
    sql: Optional[str] = Field(default=None, description="SQL expression for the table calculation")
    display_name: Optional[str] = Field(default=None, alias="displayName", description="Display name for the table calculation")
    name: Optional[str] = Field(default=None, description="Name of the table calculation")
    index: Optional[float] = Field(default=None, description="Index of the table calculation")


class SortField(BaseModel):
    """Sort field configuration."""
    model_config = ConfigDict(extra="ignore")

    descending: bool = Field(..., description="Sort order, descending if True")
    field_id: str = Field(..., alias="fieldId", description="ID of the field to sort by")

# class FilterRule(BaseModel):
#     """Filter rule configuration."""
#     model_config = ConfigDict(extra="ignore")

#     values: Optional[List[Any]] = Field(default=None, description="Values for the filter")
#     operator: Optional[str] = Field(default=None, description="Operator for the filter")
#     id: Optional[str] = Field(default=None, description="ID of the filter")
#     target: Optional[Dict[str, str]] = Field(default=None, description="Target for the filter")
#     settings: Optional[Any] = Field(default=None, description="Settings for the filter")
#     disabled: Optional[bool] = Field(default=None, description="Whether the filter is disabled")
#     required: Optional[bool] = Field(default=None, description="Whether the filter is required")

# class FilterGroup(BaseModel):
#     """Filter group configuration."""
#     model_config = ConfigDict(extra="ignore")

#     or_: Optional[Union[List[Union["FilterGroup"]], FilterRule]] = Field(alias="or", default=None, description="List of filters in the group (for OR conditions)")
#     and_: Optional[Union[List[Union["FilterGroup"]], FilterRule]] = Field(alias="and", default=None, description="List of filters in the group (for AND conditions)")
#     id: str = Field(..., description="ID of the filter group")

class Filters(BaseModel):
    """Query filters configuration."""
    model_config = ConfigDict(extra="ignore")

    # table_calculations: Optional[Dict[str, Any]] = Field(default=None, alias="tableCalculations", description="Table calculations for the filters")
    # metrics: Optional[Union[FilterGroup, FilterRule]] = Field(default=None, description="Metrics for the filters")
    # dimensions: Optional[Union[FilterGroup, FilterRule]] = Field(default=None, description="Dimensions for the filters")
    metrics: Dict[str, Any] = Field(default_factory=dict, description="Metrics for the filters")
    dimensions: Dict[str, Any] = Field(default_factory=dict, description="Dimensions for the filters")


class CompileQueryRequestV1(BaseModel):
    """Request model for CompileQuery operation."""
    model_config = ConfigDict(extra="ignore")

    projectUuid: str = Field(alias="projectUuid", description="UUID of the project to compile")
    exploreId: str = Field(alias="exploreId", description="ID of the explore to compile")

    exploreName: str = Field(alias="exploreName", description="Name of the explore to compile")
    dimensions: List[str] = Field(default_factory=list, description="List of dimensions for the query")
    metrics: List[str] = Field(default_factory=list, description="List of metrics for the query")
    filters: Filters = Field(default_factory=Filters, description="Filters to apply to the query")
    sorts: List[SortField] = Field(default_factory=list, description="Sorting configuration for the query")
    limit: int = Field(default=500, description="Limit of results returned")
    # table_calculations: List[TableCalculation] = Field(alias="tableCalculations", description="Table calculations for the query")
    # timezone: Optional[str] = Field(default=None, description="Timezone for the query")
    # custom_dimensions: Optional[List[CustomDimension]] = Field(default=None, alias="customDimensions", description="Custom dimensions for the query")
    # additional_metrics: Optional[List[AdditionalMetric]] = Field(default=None, alias="additionalMetrics", description="Additional metrics for the query")
    # metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata for the query")


class CompileQueryResponseV1(BaseModel):
    """Response model for CompileQuery operation."""
    results: str = Field(description="Results of the compiled query")
    status: str = Field(default="ok", description="Status of the response")
