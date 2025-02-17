from passlib.context import CryptContext

pwt_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")

def hashed(password: str):
    return pwt_context.hash(password)

def verify(plain_password, hashed_password):
    return pwt_context.verify(plain_password, hashed_password)

def validate(password): 
    # mật khẩu trên 8 ký tự
    return len(password) >= 8