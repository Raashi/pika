from django.contrib.auth import get_user_model

UserModel = get_user_model()


class DjangoAdminAuthBackend:
    def authenticate(self, request, username, password):
        try:
            user = UserModel.objects.get(username=username, is_admin=True)
        except UserModel.DoesNotExist:
            # According to django.contrib.token.backends.ModelBackend
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            UserModel().set_password(password)
        else:
            if user.check_password(password):
                return user

    @staticmethod
    def get_user(user_id):
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
