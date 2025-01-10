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

from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, TypeVar

from lightdash_ai_tools.lightdash.client import LightdashClient, RequestType

T = TypeVar("T")

class BaseLightdashApiCaller(Generic[T], ABC):
    """Base class for Lightdash API callers"""

    request_type: RequestType

    def __init__(self, lightdash_client: LightdashClient):
        """
        Initialize the Lightdash API caller.

        Args:
            lightdash_client (LightdashClient): The Lightdash client to use for API calls.
        """
        self.lightdash_client = lightdash_client

    def call(self, *args: Any, **kwargs: Any) -> T:
        """
        Abstract method to be implemented by subclasses.

        Raises:
            NotImplementedError: If not implemented by a subclass.
        """
        response_data = self._request(*args, **kwargs)
        return self._parse_response(response_data)

    @abstractmethod
    def _request(
        self,
        *args: Any,
        **kwargs: Any
    ) -> Dict[str, Any]:
        """
        Makes a request to the Lightdash API and returns the raw response.

        Args:
            *args: Any positional arguments.
            **kwargs: Any keyword arguments.

        Returns:
            Dict[str, Any]: The raw response data from the API.
        """
        raise NotImplementedError("Subclasses must implement this method")

    @abstractmethod
    def _parse_response(self, response_data: Dict[str, Any]) -> T:
        """
        Parse the API response into the expected model.

        Args:
            response_data (Dict[str, Any]): Raw response data from the API.

        Returns:
            T: Parsed response model.
        """
        raise NotImplementedError("Subclasses must implement this method")
