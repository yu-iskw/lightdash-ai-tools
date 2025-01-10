from typing import Any, Dict

from lightdash_ai_tools.lightdash.api.base import BaseLightdashApiCaller
from lightdash_ai_tools.lightdash.client import RequestType
from lightdash_ai_tools.lightdash.models.get_explores_v1 import GetExploresV1Response


class GetExploresV1(BaseLightdashApiCaller[GetExploresV1Response]):
    """Get explores for a project"""
    request_type = RequestType.GET

    def _request(self, project_uuid: str) -> Dict[str, Any]:
        """
        Retrieve explores for a specific project.

        Args:
            project_uuid (str): The UUID of the project to retrieve explores for.

        Returns:
            GetExploresV1Response: Details of the project's explores.
        """
        formatted_path = "/api/v1/projects/{project_uuid}/explores".format(project_uuid=project_uuid)
        response_data = self.lightdash_client.call(self.request_type, formatted_path)
        return response_data

    def _parse_response(self, response_data: Dict[str, Any]) -> GetExploresV1Response:
        return GetExploresV1Response(**response_data)
