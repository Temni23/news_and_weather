from typing import List

from users.models import User


def get_emails() -> List[str]:
    """Получить электронные почты пользователей с ролью 'reader'."""
    users = User.objects.filter(role='reader')
    result = [user.email for user in users if isinstance(user.email, str)]
    return result
