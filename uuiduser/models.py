import re
import uuid

from django.contrib import admin
from django.contrib.auth import models as auth_models
from django.contrib.auth.tokens import default_token_generator
from django.core import validators
from django.db import models
from django.utils import timezone

from .fields import NullCharField


# TODO(nick): We'll have to include migrations in the UUIDUser app as well,
#   since it's not entirely straight-forward to migrate.


class DefaultUserManager(auth_models.BaseUserManager):
  use_in_migrations = True

  def create(self, password=None, username=None, **extra):
    # Don't let the uuid field be specified in create calls.
    try:
      del extra['uuid']
    except KeyError:
      pass

    user = self.model(**extra)

    if password:
      user.set_password(password)
    else:
      user.set_unusable_password()

    if username:
      user.set_username(username)

    user.save(using=self._db)

    return user

  def create_user(self, email=None, password=None, username=None, **extra):
    """Provide an auth.User compliant create_user api."""
    return self.create(password=password, username=username, **extra)

  def create_superuser(self, email=None, password=None, username=None,
                       **extra):
    """Provide an auth.User compliant create_superuser api."""
    return self.create(password=password, username=username, is_staff=True,
                       is_superuser=True, **extra)


class DefaultUserQuerySet(models.QuerySet):
  def _filter_or_exclude(self, mapper, *args, **kwargs):
    """Make username lookups case-insensitive by default.

    Usernames are stored as case-sensitive strings so they may be displayed as
    the user entered them.

    Note: This does not work for more complex queries, like: related__username.
    """
    if 'username' in kwargs:
      kwargs['username__iexact'] = kwargs['username']
      del kwargs['username']
    return super(DefaultUserQuerySet, self)._filter_or_exclude(
      mapper, *args, **kwargs)

  def username(self, username):
    return self.get(username__iexact=username)

  def active(self):
    return self.filter(is_active=True)

  def staff(self):
    return self.filter(is_staff=True)

  def admin(self):
    return self.filter(is_superuser=True)


DefaultUserManager = DefaultUserManager.from_queryset(DefaultUserQuerySet)


class UUIDUser(auth_models.PermissionsMixin, auth_models.AbstractBaseUser):
  """Representation of a user (account) identified by a UUID.

  Attrs:
    username: Users should be able to set a (unique) username which they can
      use for login, display name, @ mentions, etc.
      Usernames are stored, and should be displayed, as they are entered
      (case-sensitive).  However, username queries should **always** be
      case-insensitive!

    uuid: Since usernames are optional and email is handled by another app, the
      uuid field simply provides a unique identifier for users.  It is
      auto-generated at user account creation time.  This puts the onus of
      preventing duplicate accounts on some undefined external process.

  Django auth.User Differences:

    first_name & last_name
      The `django.contrib.auth.User` model provides `first_name` and
      `last_name` fields.


      The standard contrib.auth.User first_name, last_name and email fields are
      deprecated, but can't be removed since there is, or may be, 3rd party
      code that depends on thier existence.

  """

  class Meta:
    abstract = True
    verbose_name = 'user'
    verbose_name_plural = 'users'

  # Constants
  # =========

  UNIQUE_IDENTIFIER_FIELD = 'uuid'

  # NOTE: A username is required for admin access!
  #
  # Django requires a unique username field for much of their admin
  # functionality.  Unfortunately setting this to our unique field (``uuid``)
  # breaks most of the default Django functionality (unless you want to type in
  # UUIDs all over the place).
  USERNAME_FIELD = 'username'

  # Additional fields required in createsuperuser command.
  REQUIRED_FIELDS = []

  USERNAME_VALIDATOR = validators.RegexValidator(
    re.compile(
      # Match 2 character usernames
      "("
      "[a-zA-Z]"       # First char must be a letter
      "[a-zA-Z0-9]"    # Last char must be a letter or number
      ")"

      "|"              # or

      # Match 3+ character usernames
      "("
      "[a-zA-Z]"       # First char must be a letter
      "(?![-_'.]{2})"  # Username must not contain repeated punctuation
      "[\\w.'-]+"      # First char may be followed by any alpha-numberic
                       # character (including - . ' _)
      "[a-zA-Z0-9]"    # Last char must be a letter or number
      ")"
    ),
    code='invalid')

  # Model Fields
  # ============

  uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)

  username = NullCharField(max_length=255,
                           unique=True,
                           blank=True,
                           null=True,
                           validators=[USERNAME_VALIDATOR])

  name = models.CharField(max_length=255, default='', blank=True)

  short_name = models.CharField(max_length=255, default='', blank=True)

  first_name = models.CharField(max_length=255, default='', blank=True)

  last_name = models.CharField(max_length=255, default='', blank=True)

  is_staff = models.BooleanField(default=False,
                                 help_text='Can log in to admin.')
  is_active = models.BooleanField(default=True)

  date_joined = models.DateTimeField(default=timezone.now)

  created_at = models.DateTimeField(auto_now_add=True)

  # Fields provided by contrib.auth.models.AbstractBaseUser
  # -------------------------------------------------------

  # password = models.CharField(_('password'), max_length=128)
  # last_login = models.DateTimeField(_('last login'), blank=True, null=True)

  # Fields provided by contrib.auth.models.PermissionsMixin
  # -------------------------------------------------------

  # is_superuser = models.BooleanField(
  #   default=False,
  #   verbose_name='superuser status',
  #   help_text=('Designates that this user has all permissions without '
  #              'explicitly assigning them.'))
  # groups = models.ManyToManyField(
  #   Group,
  #   blank=True,
  #   related_name="user_set",
  #   related_query_name="user",
  #   verbose_name='groups',
  #   help_text=('The groups this user belongs to. A user will get all '
  #              'permissions granted to each of their groups.'))
  # user_permissions = models.ManyToManyField(
  #   Permission,
  #   blank=True,
  #   related_name="user_set",
  #   related_query_name="user",
  #   verbose_name='user permissions',
  #   help_text='Specific permissions for this user.')

  # Model Managers/QuerySets
  # ========================

  objects = DefaultUserManager()

  def __str__(self):
    return str(self.get_username())

  @property
  def email(self):
    """A psudo-field representing the User's primary email as a string.

    This psudo-field is provided to mimic the api exposed by the
    contrib.auth.User model.

    NOTE: It is not required that sub-classes implement this.  However, 3rd
    party code (and even possibly parts of Django) may assume that a settable
    field named ``email`` exists on the User model.

    Returns the primary email for the User as a string, or the empty string if
    a primary email does not exist.
    """
    return ''

  @email.setter
  def email(self, address):
    """Provide a setter for the ``email`` psudo-field.

    This setter should add a "primary" email address to the User.  It is left
    up to the implementation to determine what "primary" means in its context.

    NOTE: It is not required that sub-classes implement this.  However, 3rd
    party code (and even possibly parts of Django) may assume that a settable
    field named ``email`` exists on the User model.

    Args:

      address(str): Email address as a string.
    """
    pass

  def set_username(self, username):
    """Set the username, taking care to normalize it first.

    TODO(nick): Ultimately we should store usernames as case-sensitive strings
      and simply use case-insensitive logic when dealing with them.  This
      provides a better UX, as we are able to display a user's username to them
      exactly as they have entered it.
      However, making this transparent and ubiquitous is non-trivial.
      Therefore, this functionality will be reserved for a future version of
      UUIDUser.  For now, just set usernames with this ``set_username`` method
      and query for them using ``User.objects.username('username')``.
    """
    username = username.lower()
    self.username = username

  def get_full_name(self):
    return self.name

  def get_short_name(self):
    return self.short_name

  def email_user(self, subject, message, from_email=None, **kwargs):
    return False

  def get_password_reset_token(self):
    return default_token_generator.make_token(self)

  def check_password_reset_token(self, token):
    return default_token_generator.check_token(self, token)

  @classmethod
  def get_by_email(cls, email, primary_only=False):
    """Return a single User instance, given an email address.

    Args:

      email(str): An email address belonging to the user.
      primary_only(bool): Whether to include matches of non-primary addresses.

    Raises:

      User.DoesNotExist: If the User was not found.

    Returns an instance of User if the User was found.
    """
    raise User.DoesNotExist
