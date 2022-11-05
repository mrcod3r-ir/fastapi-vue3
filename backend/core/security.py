#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# @Time : 2021/10/19 19:49
# @Author : zxiaosi
# @desc :Security configuration  https://fastapi.tiangolo.com/zh/advanced/security/oauth2-scopes/#global-view
from typing import Any, Union, Optional
from datetime import datetime, timedelta
from fastapi import Header
from jose import jwt
from passlib.context import CryptContext

from core import settings
from utils import AccessTokenFail

ALGORITHM = "HS256"  # Encryption Algorithm

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")  # encrypted password


def get_password_hash(password: str) -> str:
    """ Encrypted plaintext password """
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """ Verify that the plaintext password is the same as the encrypted password """
    return pwd_context.verify(password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    generate token

    :param data: store data
    :param expires_delta: expiration time
    :return: encrypted token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})  # eg: {'sub': '1', scopes: ['items'] 'exp': '123'}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# https://www.cnblogs.com/CharmCode/p/14191112.html?ivk_sa=1024320u
async def check_jwt_token(token: Optional[str] = Header(...)) -> Union[str, Any]:
    """ decrypt token """
    try:
        payload = jwt.decode(token=token, key=settings.SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except Exception as e:  # jwt.JWTError, jwt.ExpiredSignatureError, AttributeError
        raise AccessTokenFail(f'token expired!  -- {e}')


if __name__ == '__main__':
    # The value obtained after encrypting '123456' is not the same
    print(get_password_hash('123456'))

    # But the verification before encryption and after encryption is the same
    print(verify_password('123456', '$2b$12$I5lfn4eO8M0oH4yYQWjSQ.t4VJz9cGKXA.ht6syIG6tAXmbnQywqa'))  # True
    print(verify_password('123456', '$2b$12$h58wHhABGgNSRfQCqYFod.0mycfuLZIWQmtvKgP9s0VyYs78In6b.'))  # True
