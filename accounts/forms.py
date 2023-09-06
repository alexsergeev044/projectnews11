from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from django.core.mail import EmailMultiAlternatives, mail_managers, mail_admins


# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User

# class SignUpForm(UserCreationForm):
#     email = forms.EmailField(label="Email")
#     first_name = forms.CharField(label="Имя")
#     last_name = forms.CharField(label="Фамилия")
#
#     class Meta:
#         model = User
#         fields = (
#             "username",
#             "first_name",
#             "last_name",
#             "email",
#             "password1",
#             "password2",
#         )


class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)

        try:
            common_users = Group.objects.get(name="Обычные пользователи")
            user.groups.add(common_users)

            subject = 'Добро пожаловать в новостной портал!'
            text = f'{user.username}, вы успешно зарегистрировались на сайте!'
            html = (
                f'<b>{user.username}</b>, вы успешно зарегистрировались на '
                f'<a href="http://127.0.0.1:8000">сайте</a>!'
            )
            msg = EmailMultiAlternatives(
                subject=subject, body=text, from_email=None, to=[user.email]
            )
            msg.attach_alternative(html, "text/html")
            msg.send()

            mail_managers(
                subject=f'Новый пользователь {user.username}!',
                message=f'Пользователь {user.username} зарегистрировался на сайте.'
            )

            mail_admins(
                subject=f'Новый пользователь {user.username}!',
                message=f'Пользователь {user.username} зарегистрировался на сайте.'
            )
        except AttributeError:
            pass

        return user