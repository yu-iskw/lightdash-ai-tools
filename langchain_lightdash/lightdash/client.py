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

from enum import Enum
from typing import Any, Dict, Optional

import requests


class RequestType(str, Enum):
    """HTTP request type enumeration"""
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    PATCH = 'PATCH'
    DELETE = 'DELETE'


class LightdashClient:
    """A client for the Lightdash API"""

    def __init__(self, base_url: str, token: str, timeout: int = 30):
        """
        Initialize the Lightdash client.

        Args:
            base_url (str): Base URL for the Lightdash API
            token (str): API authentication token
            timeout (int, optional): Request timeout in seconds. Defaults to 30.
        """
        self.base_url = base_url.rstrip('/')
        self.token = token
        self.timeout = timeout

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
        url = f'{self.base_url}{path}'

        headers = {
            'Authorization': f'ApiKey {self.token}',
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
            raise RuntimeError(f"API call failed: {e}") from e
