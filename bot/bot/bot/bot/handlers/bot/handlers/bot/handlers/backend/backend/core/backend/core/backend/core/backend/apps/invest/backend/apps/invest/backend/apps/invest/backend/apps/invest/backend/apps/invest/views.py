from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from decimal import Decimal
import json
from .models import TelegramUser, BirdPackage, UserBird, Transaction

def webapp_view(request):
    tg_id = request.GET.get('tg_id', 0)
    user = TelegramUser.objects.filter(telegram_id=tg_id).first()
    packages = BirdPackage.objects.filter(is_active=True).order_by('price_usdt')
    user_birds = UserBird.objects.filter(user=user, is_active=True) if user else []

    context = {
        'user': user,
        'packages': packages,
        'user_birds': user_birds,
    }
    return render(request, 'webapp/index.html', context)

@csrf_exempt
def collect_earnings(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Faqat POST so‘rovi qabul qilinadi'}, status=405)

    try:
        data = json.loads(request.body)
        tg_id = data.get('tg_id')
        user = TelegramUser.objects.filter(telegram_id=tg_id).first()
        if not user:
            return JsonResponse({'error': 'Foydalanuvchi topilmadi'}, status=404)

        now = timezone.now()
        total_collected = Decimal('0.0000')

        active_birds = UserBird.objects.filter(user=user, is_active=True)
        for bird in active_birds:
            if bird.expires_at <= now:
                bird.is_active = False
                bird.save()
                continue

            elapsed_seconds = (now - bird.last_collected_at).total_seconds()
            if elapsed_seconds > 0:
                daily_profit = (bird.package.price_usdt * bird.package.daily_roi_percent) / Decimal('100.0')
                profit = (daily_profit / Decimal('86400.0')) * Decimal(str(elapsed_seconds))
                total_collected += profit
                bird.last_collected_at = now
                bird.save()

        user.earn_balance += total_collected
        user.save()

        return JsonResponse({
            'success': True,
            'collected': round(float(total_collected), 4),
            'new_balance': round(float(user.earn_balance), 4)
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def buy_bird(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Faqat POST so‘rovi qabul qilinadi'}, status=405)

    try:
        data = json.loads(request.body)
        tg_id = data.get('tg_id')
        package_id = data.get('package_id')

        user = TelegramUser.objects.filter(telegram_id=tg_id).first()
        package = BirdPackage.objects.filter(id=package_id, is_active=True).first()

        if not user or not package:
            return JsonResponse({'error': 'Ma’lumotlar topilmadi'}, status=404)

        if user.balance_usdt < package.price_usdt:
            return JsonResponse({'error': 'Balansda mablag‘ yetarli emas!'}, status=400)

        user.balance_usdt -= package.price_usdt
        user.save()

        expires = timezone.now() + timezone.timedelta(days=package.period_days)
        UserBird.objects.create(
            user=user,
            package=package,
            expires_at=expires
        )

        Transaction.objects.create(
            user=user,
            tx_type='buy_bird',
            amount=package.price_usdt,
            status='completed'
        )

        return JsonResponse({'success': True, 'new_balance': float(user.balance_usdt)})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
