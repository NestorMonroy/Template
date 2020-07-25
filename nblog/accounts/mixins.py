

class ErrorsSerializerMixin(object):
    """ Used primary by service layer to validate business rules.

        Requirements:
        - self.errors

        Example::

            class MyService(ValidationMixin):

                def __init__(self, repository, errors, locale):
                    # ...

                def authenticate(self, credential):
                    if not self.factory.membership.authenticate(credentials):
                        self.error('The username or password provided '
                                   'is incorrect.')
                        return False
                    # ...
                    return True
    """

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     error = str(item.errors[name])

    def error(self, message, name='__ERROR__'):
        """ Add `message` to errors.
        """
        self.errors.setdefault(name, []).append(message)
