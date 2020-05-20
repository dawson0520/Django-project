import time
from functools import wraps

from flask import g, request

import jwt
from loguru import logger
from src import settings
from src.db import CashierModel


def encode_jwt(data):
    return jwt.encode(data, settings.JWT_SECRET, algorithm="HS256").decode()


def decode_jwt(data):
    return jwt.decode(data, settings.JWT_SECRET, algorithms=["HS256"])


def timestamp():
    return int(time.time())


def login_required(fn):
    @wraps(fn)
    def deco(*args, **kwargs):
        try:
            authorization = request.headers["Authorization"]
            token_type, token = authorization.split(" ")
            assert token_type == "Bearer"
            username = decode_jwt(token)["username"]
            user = CashierModel.objects.get(username=username)
            assert user
            g.user = user.username
            g.uid = user.id
        except Exception as e:
            logger.warning(f"Unauthorized request [{e}]")
            return {"code": 401, "msg": "Unauthorized"}
        return fn(*args, **kwargs)

    return deco

