from model import db, ToastMessage, User
from flask_sqlalchemy import or_

class ToastService:
    @staticmethod
    def create_toast(text, user_id=None):
        toast = ToastMessage(text=text, user_id=user_id)
        db.session.add(toast)
        db.session.commit()
        return toast

    @staticmethod
    def mark_toasts_read(toast_ids):
        ToastMessage.query.filter(ToastMessage.id.in_(toast_ids)).update({"is_read": True}, synchronize_session=False)
        db.session.commit()

    @staticmethod
    def get_system_toasts():
        return ToastMessage.query.filter(ToastMessage.user_id == None).all()

    @staticmethod
    def get_user_toasts(user_id):
        return ToastMessage.query.filter(ToastMessage.user_id == user_id).all()

    @staticmethod
    def mark_user_toasts_read(user_id, toast_ids):
        ToastMessage.query.filter(
            ToastMessage.user_id == user_id,
            ToastMessage.id.in_(toast_ids)
        ).update({"is_read": True}, synchronize_session=False)
        db.session.commit()