# -*- coding: utf-8 -*-
'''
    flask_login.mixins
    ------------------
    This module provides mixin objects.
'''


from ._compat import PY2, text_type


class UserMixin(object):
    '''
    This provides default implementations for the methods that Flask-Login
    expects user objects to have.
    '''

    if not PY2:  # pragma: no cover
        # Python 3 implicitly set __hash__ to None if we override __eq__
        # We set it back to its default implementation
        __hash__ = object.__hash__

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return text_type(self.id)
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')

    def __eq__(self, other):
        '''
        Checks the equality of two `UserMixin` objects using `get_id`.
        '''
        if isinstance(other, UserMixin):
            return self.get_id() == other.get_id()
        return NotImplemented

    def __ne__(self, other):
        '''
        Checks the inequality of two `UserMixin` objects using `get_id`.
        '''
        equal = self.__eq__(other)
        if equal is NotImplemented:
            return NotImplemented
        return not equal


class AnonymousUserMixin(object):
    '''
    This is the default object for representing an anonymous user.
    '''
    @property
    def is_authenticated(self):
        return False

    @property
    def is_active(self):
        return False

    @property
    def is_anonymous(self):
        return True

    def get_id(self):
        return
root@c2d964580d7d:/usr/local/lib/python3.7/site-packages/flask_login# cd ../
root@c2d964580d7d:/usr/local/lib/python3.7/site-packages# cat __init__.py
cat: __init__.py: No such file or directory
root@c2d964580d7d:/usr/local/lib/python3.7/site-packages# cd flask_login/
root@c2d964580d7d:/usr/local/lib/python3.7/site-packages/flask_login# cat __init__.py
# -*- coding: utf-8 -*-
'''
    flask_login
    -----------
    This module provides user session management for Flask. It lets you log
    your users in and out in a database-independent manner.
    :copyright: (c) 2011 by Matthew Frazier.
    :license: MIT/X11, see LICENSE for more details.
'''

from .__about__ import __version__
from .config import (COOKIE_NAME, COOKIE_DURATION, COOKIE_SECURE,
                     COOKIE_HTTPONLY, LOGIN_MESSAGE, LOGIN_MESSAGE_CATEGORY,
                     REFRESH_MESSAGE, REFRESH_MESSAGE_CATEGORY, ID_ATTRIBUTE,
                     AUTH_HEADER_NAME)
from .login_manager import LoginManager
from .mixins import UserMixin, AnonymousUserMixin
from .signals import (user_logged_in, user_logged_out, user_loaded_from_cookie,
                      user_loaded_from_header, user_loaded_from_request,
                      user_login_confirmed, user_unauthorized,
                      user_needs_refresh, user_accessed, session_protected)
from .utils import (current_user, login_url, login_fresh, login_user,
                    logout_user, confirm_login, login_required,
                    fresh_login_required, set_login_view, encode_cookie,
                    decode_cookie, make_next_param)


__all__ = [
    LoginManager.__name__,
    UserMixin.__name__,
    AnonymousUserMixin.__name__,
    __version__,
    'COOKIE_NAME',
    'COOKIE_DURATION',
    'COOKIE_SECURE',
    'COOKIE_HTTPONLY',
    'LOGIN_MESSAGE',
    'LOGIN_MESSAGE_CATEGORY',
    'REFRESH_MESSAGE',
    'REFRESH_MESSAGE_CATEGORY',
    'ID_ATTRIBUTE',
    'AUTH_HEADER_NAME',
    'user_logged_in',
    'user_logged_out',
    'user_loaded_from_cookie',
    'user_loaded_from_header',
    'user_loaded_from_request',
    'user_login_confirmed',
    'user_unauthorized',
    'user_needs_refresh',
    'user_accessed',
    'session_protected',
    'current_user',
    'login_url',
    'login_fresh',
    'login_user',
    'logout_user',
    'confirm_login',
    'login_required',
    'fresh_login_required',
    'set_login_view',
    'encode_cookie',
    'decode_cookie',
    'make_next_param',
]