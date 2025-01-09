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

from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, ConfigDict, Field


class DefaultTimeDimension(BaseModel):
    interval: Optional[str] = Field(None, description="Time interval for the default time dimension")
    field: Optional[str] = Field(None, description="Field name for the default time dimension")

class Target(BaseModel):
    fieldRef: Optional[str] = Field(None, description="Reference to the target field")

class RequiredFilter(BaseModel):
    values: Optional[List[Optional[str]]] = Field(None, description="List of filter values")
    operator: Optional[str] = Field(None, description="Filtering operator (e.g., 'isNull')")
    id: Optional[str] = Field(None, description="Unique identifier for the filter")
    target: Optional[Target] = Field(None, description="Target of the filter")
    settings: Optional[Dict] = Field(None, description="Additional filter settings")
    disabled: Optional[bool] = Field(None, description="Whether the filter is disabled")
    required: Optional[bool] = Field(None, description="Whether the filter is required")

class HighlightPosition(BaseModel):
    character: Optional[float] = Field(None, description="Character position")
    line: Optional[float] = Field(None, description="Line number")

class SourceHighlight(BaseModel):
    end: Optional[HighlightPosition] = Field(None, description="End position of the highlight")
    start: Optional[HighlightPosition] = Field(None, description="Start position of the highlight")

class SourceDetails(BaseModel):
    content: Optional[str] = Field(None, description="Source content")
    highlight: Optional[SourceHighlight] = Field(None, description="Highlight details")
    range: Optional[Dict[str, HighlightPosition]] = Field(None, description="Range of the source")
    path: Optional[str] = Field(None, description="Path to the source")

class TableDetails(BaseModel):
    defaultTimeDimension: Optional[DefaultTimeDimension] = Field(None, description="Default time dimension for the table")
    groupDetails: Optional[Dict] = Field(None, description="Details about grouping")
    requiredAttributes: Optional[Dict] = Field(None, description="Required attributes for the table")
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
    table: Optional[str] = Field(None, description="Name of the joined table")
    sqlOn: Optional[str] = Field(None, description="SQL join condition")
    type: Optional[str] = Field(None, description="Type of join (e.g., 'inner')")
    hidden: Optional[bool] = Field(None, description="Whether the joined table is hidden")
    always: Optional[bool] = Field(None, description="Whether the join is always applied")
    compiledSqlOn: Optional[str] = Field(None, description="Compiled SQL join condition")

class ExploreResults(BaseModel):
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
    lineageGraph: Optional[Dict] = Field(None, description="Lineage graph information")
    metrics: Optional[Dict] = Field(None, description="Metrics information")
    dimensions: Optional[Dict] = Field(None, description="Dimensions information")
    explores: Optional[Dict[str, Dict]] = Field(None, description="Additional explores")
    compiledSql: Optional[str] = Field(None, description="Compiled SQL query")
    sqlTable: Optional[str] = Field(None, description="SQL table name")
    sqlWhere: Optional[str] = Field(None, description="SQL WHERE clause")
    uncompiledSqlWhere: Optional[str] = Field(None, description="Uncompiled SQL WHERE clause")
    databaseName: Optional[str] = Field(None, description="Database name")
    schemaName: Optional[str] = Field(None, description="Schema name")
    description: Optional[str] = Field(None, description="Explore description")

class GetExploreV1Response(BaseModel):
    results: Optional[Union[ExploreResults, Dict[str, Any]]] = Field(None, description="Explore results")
    status: Optional[str] = Field(None, description="Status of the API response")

    model_config = ConfigDict(extra='allow')
