from django.core import exceptions
from django.db import models


# TODO(nick): This needs to be pulled out into its own package.
class NullCharField(models.CharField):
  description = "CharField that transparently stores NULL for empty strings."
  __metaclass__ = models.SubfieldBase  # this ensures to_python will be called

  def to_python(self, value):
    # Is this the value right out of the db, or an instance? If an instance,
    # just return the instance.
    if isinstance(value, models.CharField):
      return value
    return value or ''  # Transform NULLs to empty strings.

  def get_prep_value(self, value):
    return value or None  # Transform empty strings to NULLs.
