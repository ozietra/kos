from app.database import Base

# Tüm modeller burada import edilmeli ki Alembic görebilsin
from app.models import (  # noqa: F401
    User, Business, EligibilityCheck, Application,
    ApplicationInput, KosgebProgram, Payment, NotificationSubscription
)
