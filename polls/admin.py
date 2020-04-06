from django.contrib import admin

from .models import state_table, count_table,place_table,contact

admin.site.register(state_table)
admin.site.register(count_table)
admin.site.register(place_table)