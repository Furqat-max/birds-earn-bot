from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import TelegramUser, BirdPackage, UserBird, Transaction, SystemConfig

@admin.register(TelegramUser)
class TelegramUserAdmin(ModelAdmin):
    list_display = ('telegram_id', 'username', 'first_name', 'balance_usdt', 'earn_balance', 'referrer', 'created_at')
    search_fields = ('telegram_id', 'username', 'first_name')
    list_filter = ('created_at',)

@admin.register(BirdPackage)
class BirdPackageAdmin(ModelAdmin):
    list_display = ('name', 'icon_emoji', 'price_usdt', 'daily_roi_percent', 'period_days', 'is_active')
    list_editable = ('is_active',)

@admin.register(UserBird)
class UserBirdAdmin(ModelAdmin):
    list_display = ('user', 'package', 'purchased_at', 'expires_at', 'is_active')
    list_filter = ('is_active', 'package')

@admin.register(Transaction)
class TransactionAdmin(ModelAdmin):
    list_display = ('user', 'tx_type', 'amount', 'status', 'network', 'created_at')
    list_filter = ('tx_type', 'status', 'network')
    search_fields = ('user__telegram_id', 'tx_hash', 'wallet_address')

@admin.register(SystemConfig)
class SystemConfigAdmin(ModelAdmin):
    list_display = ('ref_l1_percent', 'ref_l2_percent', 'ref_l3_percent', 'min_withdraw')
