from django.contrib import admin

from .models import Pos, AvailableFuel, AvailableService

admin.site.register(Pos)
admin.site.register(AvailableFuel)
admin.site.register(AvailableService)
