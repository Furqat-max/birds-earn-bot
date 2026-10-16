import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR / 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

import django
django.setup()

from asgiref.sync import sync_to_async
from apps.invest.models import TelegramUser, BirdPackage, UserBird, Transaction, SystemConfig

@sync_to_async
def get_or_create_user(tg_id: int, username: str, first_name: str, referrer_id: int = None):
    referrer = None
    if referrer_id and referrer_id != tg_id:
        referrer = TelegramUser.objects.filter(telegram_id=referrer_id).first()

    user, created = TelegramUser.objects.get_or_create(
        telegram_id=tg_id,
        defaults={
            'username': username or '',
            'first_name': first_name or '',
            'referrer': referrer
        }
    )
    return user, created

@sync_to_async
def get_user_profile(tg_id: int):
    return TelegramUser.objects.filter(telegram_id=tg_id).first()

@sync_to_async
def get_birds_market():
    return list(BirdPackage.objects.filter(is_active=True).order_by('price_usdt'))
