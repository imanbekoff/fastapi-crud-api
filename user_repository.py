from sqlalchemy import select
from sqlalchemy.orm import Session

from models import User


def get_user_by_email(session: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    return session.scalars(statement).first()

def get_user_by_id(session: Session, user_id: int) -> User | None:
    return session.get(User, user_id)

def create_user(session: Session, name: str, email: str) -> User:
    user = User(name=name, email=email)
    session.add(user)
    session.flush()
    return user


def update_user_name(
    session: Session,
    email: str,
    new_name: str,
) -> User | None:
    user = get_user_by_email(session, email)

    if user is None:
        return None

    user.name = new_name
    session.flush()
    return user


def delete_user(session: Session, email: str) -> bool:
    user = get_user_by_email(session, email)

    if user is None:
        return False

    session.delete(user)
    session.flush()
    return True

def update_user_by_id(
    session: Session,
    user_id: int,
    name: str,
    email: str,
) -> User | None:
    user = session.get(User, user_id)

    if user is None:
        return None

    user.name = name
    user.email = email
    session.flush()

    return user

def delete_user_by_id(
    session: Session,
    user_id: int,
) -> bool:
    user = session.get(User, user_id)

    if user is None:
        return False

    session.delete(user)
    session.flush()

    return True
