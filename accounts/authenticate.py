from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
class EmailOrPhoneModelBackend(BaseBackend):
    def authenticate(self, request, email_or_phone=None, password=None, **kwargs):
        User = get_user_model()
        try:
            user = User.objects.filter(Q(email=email_or_phone) | Q(phone=email_or_phone)).first()
            if user and user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
