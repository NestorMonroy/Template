from django.utils.translation import ugettext_lazy as _

from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from allauth.account.views import PasswordResetView
from dj_rest_auth.views import PasswordResetView
from django.contrib.auth.forms import PasswordResetForm

from ..serializers import (
    UserDetailsSerializer,
    CustomPasswordResetSerializer,
    PasswordResetSerializer
)

class CustomPasswordResetView(PasswordResetView):
    swagger_tags = ["User"]

    @swagger_auto_schema(
        responses={200: "Password reset e-mail has been sent."},
        request_body=CustomPasswordResetSerializer,
    )

    def post(self, *args, **kwargs):
        """Password reset

        Sends an email to the user with instructions on how to reset the password
        """
        return super().post(*args, **kwargs)

    # def get_context_data(self, **kwargs):
    #     ret = super(CustomPasswordResetView, self).get_context_data(**kwargs)
    #     login_url = passthrough_next_redirect_url(self.request,
    #                                               reverse("account_login"),
    #                                               self.redirect_field_name)
    #     # NOTE: For backwards compatibility
    #     ret['password_reset_form'] = ret.get('form')
    #     # (end NOTE)
    #     ret.update({"login_url": login_url})
    #     return ret

class PasswordResetView(generics.GenericAPIView):
    """
    Calls Django Auth PasswordResetForm save method.

    Accepts the following POST parameters: email
    Returns the success/fail message.
    """
    serializer_class = PasswordResetSerializer
    permission_classes = (permissions.AllowAny,)


    def post(self, request, *args, **kwargs):
        # Create a serializer with request.data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        # Return the success message with OK HTTP status
        return Response(
            {"detail": _("Password reset e-mail has been sent.")},
            status=status.HTTP_200_OK
        )

