import importlib.metadata

packages = [
    "fastapi",
    "pydantic-settings",
    "sqlmodel",
    "asyncpg",
    "alembic",
    "passlib",
    "bcrypt"
]


for pkg in packages:
    print(f"{pkg} - version {importlib.metadata.version(pkg)}")