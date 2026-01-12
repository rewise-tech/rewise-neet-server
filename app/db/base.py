from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Import models here so Alembic/metadata sees tables
from app.domain.users import models as users_models  # noqa: F401,E402
from app.domain.questions import models as questions_models  # noqa: F401,E402
from app.domain.process_questions import models as process_questions_models  # noqa: F401,E402
from app.domain.subjects import models as subjects_models  # noqa: F401,E402
from app.domain.test import models as test_models  # noqa: F401,E402
