from django.contrib.auth.forms import PasswordResetForm


# Just use the django.contrib.auth PasswordResetForm.  Technically we don't
# have to reassign it to itself...
PasswordResetForm = PasswordResetForm
