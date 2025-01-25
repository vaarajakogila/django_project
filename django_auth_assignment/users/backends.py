from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend

class CustomAuthenticationBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # Attempt to authenticate using email
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            # Attempt to authenticate using username if email doesn't match
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return None  # Return None if no matching user is found

        # Check if the password matches
        if user.check_password(password):
            return user
        return None
