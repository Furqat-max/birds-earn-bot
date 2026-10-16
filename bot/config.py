import os
import environ
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

BOT_TOKEN = env('BOT_TOKEN')
ADMIN_IDS = [int(i.strip()) for i in env('ADMIN_IDS', default='').split(',') if i.strip()]

TRC20_WALLET = env('TRC20_WALLET', default='')
BEP20_WALLET = env('BEP20_WALLET', default='')
TON_WALLET = env('TON_WALLET', default='')

TRONGRID_API_KEY = env('TRONGRID_API_KEY', default='')
BSCSCAN_API_KEY = env('BSCSCAN_API_KEY', default='')
TONCENTER_API_KEY = env('TONCENTER_API_KEY', default='')
