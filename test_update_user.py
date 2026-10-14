
from sqlalchemy import select

from db_orm import SessionLocal
from models import User


def main() -> None:
    with SessionLocal.begin() as session:
        statement = select(User).where(
            User.email == "test.user@example.com"
        )
        user = session.scalars(statement).first()

        if user is None:
            print("Пользователь не найден.")
            return

        user.name = "Yersultan Updated"

    print("Пользователь успешно обновлён.")


if __name__ == "__main__":
    main()
