from social.exceptions import AuthMissingParameter


class AuthMissingParameterExtension(AuthMissingParameter):
    """Extend exception to provide a more meaningful message"""
    def __str__(self):
        msg = super(AuthMissingParameterExtension, self).__str__()
        ext_msg = "You either need to be admin or provide access to your {0} to use this site".format(self.parameter)
        return msg + ". " + ext_msg


# Use the following method in social_pipeline to authenticate
def auth_allowed(backend, details, response, *args, **kwargs):
    if not backend.auth_allowed(response, details):
        raise AuthMissingParameterExtension(backend, parameter='pages')