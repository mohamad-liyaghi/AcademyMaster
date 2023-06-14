from django.contrib import admin
from managers.models import Manager


@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ['user', 'promoted_by', 'promotion_date', 'can_promote']
