from pyramid.config import Configurator
from pyramid.interfaces import IAuthorizationPolicy
from zope.interface import implementer
import logging

logger = logging.getLogger('jwtlogin')


@implementer(IAuthorizationPolicy)
class CustomAuthorizationPolicy(object):

    def permits(self, context, principals, permission):
        """ Return ``True`` if any of the ``principals`` is allowed the
        ``permission`` in the current ``context``, else return ``False``
        """
        if 'system.Authenticated' in principals:
            logger.info("Hello %r", principals)
            return True

    def principals_allowed_by_permission(self, context, permission):
        """ Return a set of principal identifiers allowed by the
        ``permission`` in ``context``.  This behavior is optional; if you
        choose to not implement it you should define this method as
        something which raises a ``NotImplementedError``.  This method
        will only be called when the
        ``pyramid.security.principals_allowed_by_permission`` API is
        used."""
        raise NotImplementedError


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)

    # Pyramid requires an authorization policy to be active.
    config.set_authorization_policy(CustomAuthorizationPolicy())
    config.include('pyramid_jwt')       # Enable JWT authentication.
    config.set_jwt_authentication_policy('secret')

    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('check-token', '/check_token')
    config.add_route('something-protected', '/something-protected')
    config.scan()
    return config.make_wsgi_app()
