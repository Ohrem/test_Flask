from app import create_app
from model import db, User

def setup_database():

    app = create_app()

    with app.app_context():

        db.create_all()
        if User.query.count() == 0:
            print("Добавляем пользователей в таблицу 'users'...")

            user1 = User(username="user1")
            user2 = User(username="user2")
            db.session.add_all([user1, user2])
            db.session.commit()

            print("Пользователи успешно добавлены!")
        else:
            print("Пользователи уже существуют в таблице.")

if __name__ == "__main__":
    setup_database()