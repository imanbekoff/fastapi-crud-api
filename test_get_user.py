from sqlalchemy import select

from db_orm import SessionLocal
from models import User


def main() -> None:
    statement = select(User).where(
        User.email == "test.user@example.com"
    )

    with SessionLocal() as session:
        user = session.scalars(statement).first()

        if user is None:
            print("Пользователь не найден.")
            return

        print(f"ID: {user.id}")
        print(f"Имя: {user.name}")
        print(f"Email: {user.email}")


if __name__ == "__main__":
    main()
