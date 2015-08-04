from uuiduser import models


class User(models.UUIDUser):

  @classmethod
  def get_by_email(cls, email):
    if email == 'nick@unb.services':
      return User.objects.get(username='nick')
    raise User.DoesNotExist
