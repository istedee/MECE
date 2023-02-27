import secrets, datetime, string

# from db import SessionLocal


def generate_token() -> str:
    return secrets.token_hex(16)


def generate_timestamp() -> str:
    return datetime.datetime.now()


def generate_chatroom_uuid() -> str:
    link = "".join(
        secrets.choice(string.digits + string.ascii_lowercase + string.ascii_uppercase)
        for _ in range(8)
    )
    return link
