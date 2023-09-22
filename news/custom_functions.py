from typing import List

from users.models import User


def get_emails() -> List:
    users = User.objects.filter(role='reader')
    result = [user.email for user in users]
    return result
