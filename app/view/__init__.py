from flask_restx import Namespace
from .toast_api import api as toast_api

# Здесь можно зарегистрировать дополнительные namespaces (при их наличии)
api = Namespace("toasts", description="Toast API Management")

# Регистрируем код из toast_api.py
api.add_namespace(toast_api)