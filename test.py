from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=['bcrypt']
)

hashed_pass = pwd_context.hash("My name is Kartek")

print("Hashed password - ", hashed_pass)

is_valid = pwd_context.verify("My name is Kartek", hashed_pass)

print("is valid? - ", is_valid)