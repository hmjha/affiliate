from requests import request, ConnectionError
from social.backends.facebook import FacebookOAuth2
from social.exceptions import AuthUnreachableProvider


class FacebookOauth2Extension(FacebookOAuth2):
    """Extending FacebookOauth2 auth functionality to check response for accounts data."""
    def auth_allowed(self, response, details):
        allowed = super(FacebookOauth2Extension, self).auth_allowed(response, details)
        _id_ = response.get('id')
        access_token = response.get('access_token')
        url = 'https://graph.facebook.com/{0}/accounts?access_token={1}'.format(_id_, access_token)

        try:
            url_response = request('GET', url)
        except ConnectionError:
            raise AuthUnreachableProvider(FacebookOauth2Extension)

        if url_response.json().get('data') and allowed:
            return True
        else:
            return False

    # Extending FacebookOauth2 functionality to get extra scope as required
    def get_scope(self):
        scope = super(FacebookOauth2Extension, self).get_scope()
        if self.data.get('read-insights'):
            scope.append('read-insights')
        return scope


# TODO
            # Extend Facebook oauth functionality to ask for permissions as required
            # Do as above for Twitter and Google+