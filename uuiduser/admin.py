from django.contrib.auth.admin import UserAdmin


class UUIDUserAdmin(UserAdmin):
  """Handle a UUIDUser-based User model properly in the admin."""

  fieldsets = (
    (None, {'fields': ('username', 'password')}),
    ('Personal info', {'fields': ('name', 'short_name')}),
    ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                'groups', 'user_permissions')}),
    ('Important dates', {'fields': ('last_login', 'date_joined')}),
  )
  list_display = ('username', 'name', 'short_name', 'is_staff')
  search_fields = ('username', 'name', 'short_name')
