from db_orm import SessionLocal
from user_repository import (
    create_user,
    delete_user,
    get_user_by_email,
    update_user_name,
    get_user_by_id
)

def main() -> None:
    email = "repository.test@example.com"

    # CREATE
    with SessionLocal.begin() as session:
        user = get_user_by_email(session, email)

        if user is None:
            user = create_user(
                session,
                name="Repository Test",
                email=email,
            )

        print(f"Создан или найден пользователь: {user.id}")

        # READ BY ID
    found_user = get_user_by_id(session, user.id)

    if found_user is None:
        print("Пользователь не найден.")
    else:
        print(f"Найден по ID: {found_user.name}")

    # READ
    with SessionLocal() as session:
        user = get_user_by_email(session, email)

        if user is not None:
            print(f"Прочитан пользователь: {user.name}")

    # UPDATE
    with SessionLocal.begin() as session:
        user = update_user_name(
            session,
            email,
            "Repository Updated",
        )

        if user is not None:
            print(f"Новое имя: {user.name}")

    # DELETE
    with SessionLocal.begin() as session:
        deleted = delete_user(session, email)
        print(f"Удаление выполнено: {deleted}")


if __name__ == "__main__":
    main()
