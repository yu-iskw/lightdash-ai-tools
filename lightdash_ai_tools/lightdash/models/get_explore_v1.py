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


class DefaultTimeDimension(BaseModel):
    """Default time dimension"""
    model_config = ConfigDict(extra='allow')

    interval: Optional[str] = Field(None, description="Time interval for the default time dimension")
    field: Optional[str] = Field(None, description="Field name for the default time dimension")


class Target(BaseModel):
    """Target"""
    model_config = ConfigDict(extra='allow')

    fieldRef: Optional[str] = Field(None, description="Reference to the target field")


class RequiredFilter(BaseModel):
    """Required filter"""
    model_config = ConfigDict(extra='allow')

    values: Optional[List[Optional[str]]] = Field(None, description="List of filter values")
    operator: Optional[str] = Field(None, description="Filtering operator (e.g., 'isNull')")
    id: Optional[str] = Field(None, description="Unique identifier for the filter")
    target: Optional[Target] = Field(None, description="Target of the filter")
    settings: Optional[Dict[str, Any]] = Field(None, description="Additional filter settings")
    disabled: Optional[bool] = Field(None, description="Whether the filter is disabled")
    required: Optional[bool] = Field(None, description="Whether the filter is required")


class HighlightPosition(BaseModel):
    """Highlight position"""
    model_config = ConfigDict(extra='allow')

    character: Optional[float] = Field(None, description="Character position")
    line: Optional[float] = Field(None, description="Line number")


class SourceHighlight(BaseModel):
    """Source highlight"""
    model_config = ConfigDict(extra='allow')

    end: Optional[HighlightPosition] = Field(None, description="End position of the highlight")
    start: Optional[HighlightPosition] = Field(None, description="Start position of the highlight")


class SourceDetails(BaseModel):
    """Source details"""
    model_config = ConfigDict(extra='allow')

    content: Optional[str] = Field(None, description="Source content")
    highlight: Optional[SourceHighlight] = Field(None, description="Highlight details")
    range: Optional[Dict[str, HighlightPosition]] = Field(None, description="Range of the source")
    path: Optional[str] = Field(None, description="Path to the source")


class TableDetails(BaseModel):
    """Table details"""
    model_config = ConfigDict(extra='allow')

    defaultTimeDimension: Optional[DefaultTimeDimension] = Field(None, description="Default time dimension for the table")
    groupDetails: Optional[Dict[str, Any]] = Field(None, description="Details about grouping")
    requiredAttributes: Optional[Dict[str, Any]] = Field(None, description="Required attributes for the table")
    hidden: Optional[bool] = Field(None, description="Whether the table is hidden")
    requiredFilters: Optional[List[RequiredFilter]] = Field(None, description="List of required filters")
    sqlWhere: Optional[str] = Field(None, description="SQL WHERE clause")
    groupLabel: Optional[str] = Field(None, description="Label for grouping")
    orderFieldsBy: Optional[str] = Field(None, description="Ordering of fields")
    sqlTable: Optional[str] = Field(None, description="SQL table name")
    schema: Optional[str] = Field(None, description="Database schema")
    database: Optional[str] = Field(None, description="Database name")
    description: Optional[str] = Field(None, description="Table description")
    originalName: Optional[str] = Field(None, description="Original name of the table")
    label: Optional[str] = Field(None, description="Display label")
    name: Optional[str] = Field(None, description="Table name")
    uncompiledSqlWhere: Optional[str] = Field(None, description="Uncompiled SQL WHERE clause")
    source: Optional[SourceDetails] = Field(None, description="Source details")
    groupBy: Optional[List[str]] = Field(None, description="Fields to group by")
    sqlGroup: Optional[str] = Field(None, description="SQL grouping configuration")
    type: Optional[str] = Field(None, description="Type of the table")
    timeframes: Optional[List[str]] = Field(None, description="Available timeframes")
    suggestFilter: Optional[bool] = Field(None, description="Suggestion to apply a filter")
    suggestDimension: Optional[str] = Field(None, description="Suggested dimension")


class JoinedTable(BaseModel):
    """Joined table"""
    model_config = ConfigDict(extra='allow')

    table: Optional[str] = Field(None, description="Name of the joined table")
    sqlOn: Optional[str] = Field(None, description="SQL join condition")
    type: Optional[str] = Field(None, description="Type of join (e.g., 'inner')")
    hidden: Optional[bool] = Field(None, description="Whether the joined table is hidden")
    always: Optional[bool] = Field(None, description="Whether the join is always applied")
    compiledSqlOn: Optional[str] = Field(None, description="Compiled SQL join condition")


class Dimension(BaseModel):
    """Dimension"""
    model_config = ConfigDict(extra='allow')

    sql: Optional[str] = Field(None, description="SQL expression for the dimension")
    name: Optional[str] = Field(None, description="Name of the dimension")
    type: Optional[str] = Field(None, description="Data type of the dimension")
    index: Optional[int] = Field(None, description="Index of the dimension")
    label: Optional[str] = Field(None, description="Label of the dimension")
    table: Optional[str] = Field(None, description="Table name the dimension belongs to")
    groups: Optional[List[str]] = Field(None, description="Groups the dimension is part of")
    hidden: Optional[bool] = Field(None, description="Whether the dimension is hidden")
    fieldType: Optional[str] = Field(None, description="Field type of the dimension")
    tableLabel: Optional[str] = Field(None, description="Label of the table")
    compiledSql: Optional[str] = Field(None, description="Compiled SQL for the dimension")
    description: Optional[str] = Field(None, description="Description of the dimension")
    isIntervalBase: Optional[bool] = Field(None, description="Whether the dimension is interval-based")
    tablesReferences: Optional[List[str]] = Field(None, description="Tables referenced by the dimension")
    timeInterval: Optional[str] = Field(None, description="Time interval for date dimensions")
    timeIntervalBaseDimensionName: Optional[str] = Field(None, description="Base dimension name for time intervals")


class Metric(BaseModel):
    """Metric"""
    model_config = ConfigDict(extra='allow')

    sql: Optional[str] = Field(None, description="SQL expression for the metric")
    name: Optional[str] = Field(None, description="Name of the metric")
    type: Optional[str] = Field(None, description="Type of the metric (e.g., 'sum', 'count_distinct')")
    index: Optional[int] = Field(None, description="Index of the metric")
    label: Optional[str] = Field(None, description="Label of the metric")
    table: Optional[str] = Field(None, description="Table name the metric belongs to")
    groups: Optional[List[str]] = Field(None, description="Groups the metric is part of")
    hidden: Optional[bool] = Field(None, description="Whether the metric is hidden")
    filters: Optional[List[Any]] = Field(None, description="Filters applied to the metric")
    fieldType: Optional[str] = Field(None, description="Field type of the metric")
    tableLabel: Optional[str] = Field(None, description="Label of the table")
    compiledSql: Optional[str] = Field(None, description="Compiled SQL for the metric")
    description: Optional[str] = Field(None, description="Description of the metric")
    isAutoGenerated: Optional[bool] = Field(None, description="Whether the metric is auto-generated")
    tablesReferences: Optional[List[str]] = Field(None, description="Tables referenced by the metric")
    dimensionReference: Optional[str] = Field(None, description="Reference to the related dimension")


class GetExploreV1Results(BaseModel):
    """Explore results"""
    model_config = ConfigDict(extra='allow')

    type: Optional[str] = Field(None, description="Type of explore")
    sqlPath: Optional[str] = Field(None, description="Path to SQL file")
    ymlPath: Optional[str] = Field(None, description="Path to YAML file")
    warehouse: Optional[str] = Field(None, description="Warehouse name")
    targetDatabase: Optional[str] = Field(None, description="Target database")
    tables: Optional[Dict[str, TableDetails]] = Field(None, description="Dictionary of tables")
    joinedTables: Optional[List[JoinedTable]] = Field(None, description="List of joined tables")
    baseTable: Optional[str] = Field(None, description="Base table name")
    groupLabel: Optional[str] = Field(None, description="Group label")
    tags: Optional[List[str]] = Field(None, description="List of tags")
    label: Optional[str] = Field(None, description="Display label")
    name: Optional[str] = Field(None, description="Explore name")
    lineageGraph: Optional[Dict[str, Any]] = Field(None, description="Lineage graph information")
    metrics: Optional[Dict[str, Metric]] = Field(None, description="Metrics information")
    dimensions: Optional[Dict[str, Dimension]] = Field(None, description="Dimensions information")
    explores: Optional[Dict[str, Dict[str, Any]]] = Field(None, description="Additional explores")
    compiledSql: Optional[str] = Field(None, description="Compiled SQL query")
    sqlTable: Optional[str] = Field(None, description="SQL table name")
    sqlWhere: Optional[str] = Field(None, description="SQL WHERE clause")
    uncompiledSqlWhere: Optional[str] = Field(None, description="Uncompiled SQL WHERE clause")
    databaseName: Optional[str] = Field(None, description="Database name")
    schemaName: Optional[str] = Field(None, description="Schema name")
    description: Optional[str] = Field(None, description="Explore description")
    timeframes: Optional[List[str]] = Field(None, description="Available timeframes")


class GetExploreV1Response(BaseModel):
    results: GetExploreV1Results = Field(None, description="Explore results")
    status: str = Field(None, description="Status of the API response")
