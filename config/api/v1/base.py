from rest_framework.response import Response
from rest_framework.views import APIView


class HealthCheckView(APIView):
    """
    Basic API health-check endpoint.
    """

    authentication_classes = []
    permission_classes = []

    def get(self, request):
        return Response(
            {
                "success": True,
                "message": "Shades of Brown API is running.",
                "data": {
                    "version": "v1",
                    "status": "healthy",
                },
            }
        )
    