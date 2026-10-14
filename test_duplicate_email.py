from sqlalchemy.exc import IntegrityError

from db_orm import SessionLocal
from user_repository import create_user


def main() -> None:
    try:
        with SessionLocal.begin() as session:
            user = create_user(
                session,
                name="Duplicate Test",
                email="test.user@example.com",
            )
            print(f"Создан пользователь с ID: {user.id}")

    
    
    except IntegrityError as error:
        original_error = error.orig
        sqlstate = getattr(original_error, "sqlstate", None)
        constraint = getattr(original_error, "diag", None)
        constraint_name = (
            getattr(constraint, "constraint_name", None)
            if constraint is not None
            else None
        )

        if (
            sqlstate == "23505"
            and constraint_name == "users_email_key"
        ):
            print("Email уже занят.")
        elif sqlstate == "23505":
            print("Нарушено другое ограничение уникальности.")
        else:
            print("Другая ошибка целостности данных.")

    print("Программа продолжает работу.")




if __name__ == "__main__":
    main()
