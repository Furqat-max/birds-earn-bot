from django.db import models
from django.utils import timezone
from decimal import Decimal

class TelegramUser(models.Model):
    telegram_id = models.BigIntegerField(unique=True, verbose_name="Telegram ID")
    username = models.CharField(max_length=255, null=True, blank=True, verbose_name="Username")
    first_name = models.CharField(max_length=255, null=True, blank=True, verbose_name="Ism")
    balance_usdt = models.DecimalField(max_digits=12, decimal_places=4, default=Decimal('0.0000'), verbose_name="Asosiy balans (USDT)")
    earn_balance = models.DecimalField(max_digits=12, decimal_places=4, default=Decimal('0.0000'), verbose_name="Daromad balansi (USDT)")
    referrer = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='referrals', verbose_name="Taklif qilgan shaxs")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ro'yxatdan o'tgan vaqt")

    class Meta:
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"

    def __str__(self):
        return f"{self.first_name} ({self.telegram_id})"

class BirdPackage(models.Model):
    name = models.CharField(max_length=100, verbose_name="Qush nomi")
    price_usdt = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Narxi (USDT)")
    daily_roi_percent = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Kunlik daromad foizi (%)")
    period_days = models.PositiveIntegerField(default=30, verbose_name="Amal qilish muddati (kun)")
    icon_emoji = models.CharField(max_length=10, default="🦅", verbose_name="Emoji belgisi")
    is_active = models.BooleanField(default=True, verbose_name="Sotuvda faolmi?")

    class Meta:
        verbose_name = "VIP Qush paketi"
        verbose_name_plural = "VIP Qush paketlari"

    def __str__(self):
        return f"{self.name} - {self.price_usdt} USDT"

class UserBird(models.Model):
    user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE, related_name='birds', verbose_name="Foydalanuvchi")
    package = models.ForeignKey(BirdPackage, on_delete=models.CASCADE, verbose_name="Qush paketi")
    purchased_at = models.DateTimeField(auto_now_add=True, verbose_name="Sotib olingan vaqt")
    last_collected_at = models.DateTimeField(default=timezone.now, verbose_name="Oxirgi foyda yig'ilgan vaqt")
    expires_at = models.DateTimeField(verbose_name="Tugash vaqti")
    is_active = models.BooleanField(default=True, verbose_name="Faol holatdami?")

    class Meta:
        verbose_name = "Foydalanuvchi qushi"
        verbose_name_plural = "Foydalanuvchilar qushlari"

class Transaction(models.Model):
    TX_TYPES = (
        ('deposit', 'Hisob to\'ldirish'),
        ('withdraw', 'Pul yechish'),
        ('buy_bird', 'Qush sotib olish'),
        ('earn', 'Qush daromadi'),
        ('referral', 'Referal bonusi'),
    )
    STATUS_CHOICES = (
        ('pending', 'Kutilmoqda'),
        ('completed', 'Muvaffaqiyatli'),
        ('rejected', 'Bekor qilingan'),
    )
    user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE, related_name='transactions', verbose_name="Foydalanuvchi")
    tx_type = models.CharField(max_length=20, choices=TX_TYPES, verbose_name="Tranzaksiya turi")
    amount = models.DecimalField(max_digits=12, decimal_places=4, verbose_name="Miqdor (USDT)")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Holati")
    network = models.CharField(max_length=20, null=True, blank=True, verbose_name="Tarmoq (TRC20, BEP20, TON)")
    wallet_address = models.CharField(max_length=255, null=True, blank=True, verbose_name="Hamyon manzili")
    tx_hash = models.CharField(max_length=255, null=True, blank=True, unique=True, verbose_name="Tranzaksiya Hashi")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Vaqti")

    class Meta:
        verbose_name = "Tranzaksiya"
        verbose_name_plural = "Tranzaksiyalar"

class SystemConfig(models.Model):
    ref_l1_percent = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('5.00'), verbose_name="1-daraja referal foizi (%)")
    ref_l2_percent = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('2.00'), verbose_name="2-daraja referal foizi (%)")
    ref_l3_percent = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('1.00'), verbose_name="3-daraja referal foizi (%)")
    min_withdraw = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('5.00'), verbose_name="Minimal yechish summasi (USDT)")

    class Meta:
        verbose_name = "Tizim sozlamasi"
        verbose_name_plural = "Tizim sozlamalari"
