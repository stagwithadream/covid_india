from django.contrib import admin

from .models import state_table, count_table

admin.site.register(state_table)
admin.site.register(count_table)
