from lightdash_ai_tools.lightdash.api.base import BaseLightdashApiCaller
from lightdash_ai_tools.lightdash.client import RequestType
from lightdash_ai_tools.lightdash.models.get_explores_v1 import GetExploresV1Response


class GetExploresV1(BaseLightdashApiCaller[GetExploresV1Response]):
    """Get explores for a project"""
    request_type = RequestType.GET
    response_model = GetExploresV1Response

    def call(self, project_uuid: str) -> GetExploresV1Response:
        """
        Retrieve explores for a specific project.

        Args:
            project_uuid (str): The UUID of the project to retrieve explores for.

        Returns:
            GetExploresV1Response: Details of the project's explores.
        """
        formatted_path = "/api/v1/projects/{project_uuid}/explores".format(project_uuid=project_uuid)
        return super()._call(path=formatted_path)
