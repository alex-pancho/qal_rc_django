import logging
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Логування інформації про запит ДО view
        logger.info(
            f"Запит: {request.method} {request.path} | "
            f"IP: {request.META.get('REMOTE_ADDR')}"
        )
        return None  # Продовжити обробку
    
    def process_response(self, request, response):
        # Логування інформації після view
        logger.info(
            f"Відповідь: {request.path} | "
            f"Статус: {response.status_code}"
        )
        return response 