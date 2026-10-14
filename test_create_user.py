from db_orm import SessionLocal
from models import User


def main() -> None:
    with SessionLocal.begin() as session:
        user = User(
            name="Test User",
            email="test.user@example.com",
        )
        session.add(user)

    print("Пользователь успешно создан.")


if __name__ == "__main__":
    main()
