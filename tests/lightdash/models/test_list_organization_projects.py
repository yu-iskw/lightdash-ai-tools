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

import unittest

from langchain_lightdash.lightdash.models.list_organization_projects_v1 import (
    ListOrganizationProjectsResponse,
    OrganizationProject,
)


class TestOrganizationProjectModel(unittest.TestCase):
    """Test the OrganizationProject model"""

    def test_organization_project_model(self):
        # Create a sample project data
        project_data = {
            "warehouseType": "bigquery",
            "upstreamProjectUuid": "uuid-1",
            "createdByUserUuid": "user-1",
            "type": "data",
            "name": "Project A",
            "projectUuid": "uuid-1"
        }

        # Create an instance of OrganizationProject
        project = OrganizationProject(**project_data)

        # Assert the attributes
        self.assertEqual(project.warehouseType, "bigquery")
        self.assertEqual(project.upstreamProjectUuid, "uuid-1")
        self.assertEqual(project.createdByUserUuid, "user-1")
        self.assertEqual(project.type, "data")
        self.assertEqual(project.name, "Project A")
        self.assertEqual(project.projectUuid, "uuid-1")


class TestListOrganizationProjectsResponseModel(unittest.TestCase):
    """Test the ListOrganizationProjectsResponse model"""

    def test_list_organization_projects_response_model(self):
        # Create a sample response data
        response_data = {
            "results": [
                {
                    "warehouseType": "bigquery",
                    "upstreamProjectUuid": "uuid-1",
                    "createdByUserUuid": "user-1",
                    "type": "data",
                    "name": "Project A",
                    "projectUuid": "uuid-1"
                },
                {
                    "warehouseType": "snowflake",
                    "upstreamProjectUuid": "uuid-2",
                    "createdByUserUuid": "user-2",
                    "type": "data",
                    "name": "Project B",
                    "projectUuid": "uuid-2"
                }
            ],
            "status": "success"
        }

        # Create an instance of ListOrganizationProjectsResponse
        response = ListOrganizationProjectsResponse(**response_data)

        # Assert the attributes
        self.assertEqual(response.status, "success")
        self.assertEqual(len(response.results), 2)
        self.assertIsInstance(response.results[0], OrganizationProject)
        self.assertIsInstance(response.results[1], OrganizationProject)
