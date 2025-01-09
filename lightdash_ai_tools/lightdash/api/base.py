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

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, Optional, Type, TypeVar

from pydantic import BaseModel

from lightdash_ai_tools.lightdash.client import LightdashClient, RequestType

T = TypeVar("T", bound=BaseModel)

class BaseLightdashApiCaller(Generic[T], ABC):
    """Base class for Lightdash API callers"""

    request_type: RequestType
    response_model: Type[T]

    def __init__(self, client: LightdashClient):
        """
        Initialize the Lightdash API caller.

        Args:
            client (LightdashClient): The Lightdash client to use for API calls.
        """
        self.client = client

    @abstractmethod
    def call(self, *args: Any, **kwargs: Any) -> T:
        """
        Abstract method to be implemented by subclasses.

        Raises:
            NotImplementedError: If not implemented by a subclass.
        """
        raise NotImplementedError("Subclasses must implement this method")

    def _call(
        self,
        path: str,
        parameters: Optional[Dict[str, str]] = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> T:
        """
        Internal method to call the Lightdash API.

        Args:
            parameters (Optional[Dict[str, str]], optional): Query parameters. Defaults to None.
            data (Optional[Dict[str, Any]], optional): Request body data. Defaults to None.

        Returns:
            T: The response from the API call.
        """
        response_data = self.client.call(self.request_type, path, parameters, data)
        return self._parse_response(response_data)

    def _parse_response(self, response_data: Dict[str, Any]) -> T:
        """
        Parse the API response into the expected model.

        Args:
            response_data (Dict[str, Any]): Raw response data from the API.

        Returns:
            T: Parsed response model.
        """
        # Use the type of the current instance to instantiate the expected model
        return self.response_model(**response_data)  # type: ignore
