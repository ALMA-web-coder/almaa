from django.contrib.admin import AdminSite
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import User, Group


class MyAdminSite(AdminSite):
    site_header = "ALMA ADMIN"
    site_title = "ALMA ADMIN"
    index_title = "Welcome to the ALMA ADMIN Panel"

# Create a single admin site instance
custom_admin_site = MyAdminSite(name='myadmin')

# Register default Django auth models
custom_admin_site.register(User, UserAdmin)
custom_admin_site.register(Group, GroupAdmin)