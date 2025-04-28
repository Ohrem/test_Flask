from flask_restx import Namespace, Resource

from flask import request, jsonify
from marshmallow import ValidationError
from schema.toast import (
    CreateToastSchema,
    MarkReadToastSchema,
    GetUserToastSchema,
    ToastResponseSchema
)
from service.toast_service import ToastService

# Namespace для всех маршрутов toast
api = Namespace("toasts", description="Toast Messages Management")

@api.route("/")
class ToastsResource(Resource):
    def get(self):
        """Получить системные toast-сообщения"""
        toasts = ToastService.get_system_toasts()
        schema = ToastResponseSchema(many=True)
        return jsonify(schema.dump(toasts))

    def post(self):
        """Создание нового toast-сообщения"""
        data = request.json
        try:
            valid_data = CreateToastSchema().load(data)
        except ValidationError as exc:
            return {"error": exc.messages}, 400

        toast = ToastService.create_toast(valid_data['text'], valid_data.get('user_id'))
        schema = ToastResponseSchema()
        return jsonify(schema.dump(toast))

@api.route("/mark-read")
class MarkReadResource(Resource):
    def post(self):
        """Отметить toast как прочитанные"""
        data = request.json
        try:
            valid_data = MarkReadToastSchema().load(data)
        except ValidationError as exc:
            return {"error": exc.messages}, 400

        ToastService.mark_toasts_read(valid_data['id'])
        return {"message": "Toasts marked as read"}, 200

@api.route("/user")
class UserToastResource(Resource):
    def post(self):
        """Получить toast-сообщения для конкретного пользователя"""
        data = request.json
        try:
            valid_data = GetUserToastSchema().load(data)
        except ValidationError as exc:
            return {"error": exc.messages}, 400

        user_toasts = ToastService.get_user_toasts(valid_data['user_id'])
        schema = ToastResponseSchema(many=True)
        return jsonify(schema.dump(user_toasts))

@api.route("/user/mark-read")
class UserMarkReadResource(Resource):
    def post(self):
        """Отметить пользовательские toast-сообщения как прочитанные"""
        data = request.json
        user_id = data.get("user_id")
        toast_ids = data.get("id")
        if not user_id or not toast_ids:
            return {"error": "user_id and id are required fields"}, 400

        ToastService.mark_user_toasts_read(user_id, toast_ids)
        return {"message": "User's toasts marked as read"}, 200