from db_orm import SessionLocal
from models import User


def main() -> None:
    with SessionLocal() as session:
        user = session.get(User, 2)

        if user is None:
            print("Пользователь не найден.")
            return

        print(f"ID: {user.id}")
        print(f"Имя: {user.name}")
        print(f"Email: {user.email}")


if __name__ == "__main__":
    main()
