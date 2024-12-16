import os
import time
from typing import Dict

import jwt
from dotenv import load_dotenv

import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta


try:
    load_dotenv()
except Exception as e:
    SystemExit(f"Error loading .env file: {e}")
    

JWT_SECRET = os.getenv("SECRET")
JWT_ALGORITHM = os.getenv("ALGORITHM")


class AuthHandler():
	security = HTTPBearer()
	pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


	def get_password_hash(self, password):
		return self.pwd_context.hash(password)

	def verify_password(self, plain_password, hashed_password):
		return self.pwd_context.verify(plain_password, hashed_password)

	def encode_token(self, email, type):
		payload = dict(
			iss = email,
			sub = type
		)
		to_encode = payload.copy()
		if type == "access_token":
			to_encode.update({"exp": datetime.now() + timedelta(minutes=1)})
		else:
			to_encode.update({"exp": datetime.now() + timedelta(hours=720)})

		return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)

	def encode_login_token(self, email):
		access_token = self.encode_token(email, "access_token")
		refresh_token = self.encode_token(email, "refresh_token")

		login_token = dict(
			access_token=f"{access_token}",
			refresh_token=f"{refresh_token}"
		) 
		return login_token

	def encode_update_token(self, email):
		access_token = self.encode_token(email, "access_token")

		update_token = dict(
			access_token=f"{access_token}"
		) 
		return update_token


	def decode_access_token(self, token):
		try:
			payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
			if payload['sub'] != "access_token":
				raise HTTPException(status_code=401, detail='Invalid token')
			return payload['iss']
		except jwt.ExpiredSignatureError:
			raise HTTPException(status_code=401, detail='Signature has expired')
		except jwt.InvalidTokenError as e:
			raise HTTPException(status_code=401, detail='Invalid token')


	def decode_refresh_token(self, token):
		try:
			payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
			if payload['sub'] != "refresh_token":
				raise HTTPException(status_code=401, detail='Invalid token')
			return payload['iss']
		except jwt.ExpiredSignatureError:
			raise HTTPException(status_code=401, detail='Signature has expired')
		except jwt.InvalidTokenError as e:
			raise HTTPException(status_code=401, detail='Invalid token')


	def auth_access_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
		return self.decode_access_token(auth.credentials)


	def auth_refresh_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
		return self.decode_refresh_token(auth.credentials)