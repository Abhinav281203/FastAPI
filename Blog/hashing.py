from passlib.context import CryptContext

# Context to hash password
pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash:
    def bcrypt(password: str):
        return pwd_cxt.hash(password)

    def verify(pass_from_frontend, pass_from_db):
        return pwd_cxt.verify(pass_from_frontend, pass_from_db)
