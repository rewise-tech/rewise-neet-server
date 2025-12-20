from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Import models here so Alembic/metadata sees tables
from app.domain.users import models as users_models  # noqa: F401,E402
