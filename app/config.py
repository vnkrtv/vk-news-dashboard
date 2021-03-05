import os

PG_USER = os.getenv('PG_USER', 'postgres')
PG_PASS = os.getenv('PG_PASS', 'password')
PG_HOST = os.getenv('PG_HOST', '172.17.0.2')
PG_PORT = os.getenv('PG_PORT', 5432)
PG_NAME = os.getenv('PG_NAME', 'vknews')
DATA_UPDATING_INTERVAL = int(os.getenv('DATA_UPDATING_INTERVAL', '600'))  # 10 minutes
