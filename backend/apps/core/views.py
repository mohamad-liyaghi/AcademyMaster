from django.http import JsonResponse
from rest_framework import status
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def handler_404(request, *args, **kwargs):
    return JsonResponse(
        {"not found": "page does not found"}, status=status.HTTP_404_NOT_FOUND
    )


def handler_500(request, *args, **kwargs):
    current_url = request.get_full_path()
    logger.critical(f"URL: {current_url} Status: 500 ")
    return JsonResponse(
        {"server error": "Sth went wrong, please contact site admins."},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
