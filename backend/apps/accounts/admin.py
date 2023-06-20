from django.contrib import admin
from accounts.models import Account, VerificationCode


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['email', 'full_name', 'is_active']


@admin.register(VerificationCode)
class VerificationCodeAdmin(admin.ModelAdmin):
    list_display = ['account', 'code', 'expire_at']
