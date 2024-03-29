from accounts.models import User
from django.core.exceptions import ObjectDoesNotExist
import re
import logging

logger = logging.getLogger('common')


def get_user(key):
    '''
    fetch User object based on 3 Keys (id, username, email)

    return -> User | ObjectDoesNotExist | None
    '''
    key = key.strip()
    is_key_id = isinstance(key, int)
    is_key_email = re.match(r'^.+@.+\..+$', str(key))

    try:
        if is_key_id:
            user = User.objects.get(id=key)
        elif is_key_email is not None:
            user = User.objects.get(email=key)
        else:
            user = User.objects.get(username=key)
        return user
    except ObjectDoesNotExist as e:
        return e
    except Exception as e:
        logger.error(f'Found Error in Getting User Object : {e}')
        return None
