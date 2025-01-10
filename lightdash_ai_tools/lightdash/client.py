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

import textwrap
from enum import Enum
from typing import Any, Dict, Optional

import requests
from pydantic import BaseModel, Field, SecretStr


class RequestType(str, Enum):
    """HTTP request type enumeration"""
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    PATCH = 'PATCH'
    DELETE = 'DELETE'


class LightdashClient(BaseModel):
    """A client for the Lightdash API"""

    base_url: str = Field(alias="base_url", description="Base URL for the Lightdash API")
    token: SecretStr = Field(alias="token", description="API authentication token")
    timeout: int = Field(alias="timeout", description="Request timeout in seconds", default=30)

    def call(
        self,
        request_type: RequestType,
        path: str,
        parameters: Optional[Dict[str, str]] = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Make an API call to Lightdash.

        Args:
            request_type (RequestType): HTTP method to use
            path (str): API endpoint path
            parameters (Optional[Dict[str, str]], optional): Query parameters
            data (Optional[Dict[str, Any]], optional): Request body data

        Returns:
            Dict[str, Any]: Parsed JSON response
        """
        base_url = self.base_url.rstrip("/")
        url = f'{base_url}{path}'

        headers = {
            'Authorization': f'ApiKey {self.token.get_secret_value()}',
            'Content-Type': 'application/json'
        }

        try:
            response = requests.request(
                request_type.value,
                url,
                params=parameters,
                json=data,
                headers=headers,
                timeout=self.timeout,
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            error_message = textwrap.dedent(f"""\
              API call failed: {e}

              URL: {url}
              Headers: {headers}
              Parameters: {parameters}
              Data: {data}
            """).strip()
            raise RuntimeError(error_message) from e
