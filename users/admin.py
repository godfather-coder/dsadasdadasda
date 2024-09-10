
from django.contrib import admin
from .models import (User, UserActionLog)

admin.site.register(User)
admin.site.register(UserActionLog)

