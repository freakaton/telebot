import os


TOKEN = os.getenv('TG_TOKEN')
HOST = os.getenv('HOST')
MOVIEDB_TOKEN = os.getenv('MOVIEDB_TOKEN')

if None in (TOKEN, HOST, MOVIEDB_TOKEN):
    raise Exception('Some of variables are not set')

WEBHOOK_PORT = 8443
WEBHOOK_URL_BASE = f'https://{HOST}:{WEBHOOK_PORT}'
WEBHOOK_URL_PATH = f'/{TOKEN}/'
IMAGE_BASE_URL = ''
WEBHOOK_SSL_CERT = './webhook_cert.pem'
WEBHOOK_SSL_PRIV = './webhook_pkey.pem'
SSL = (WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV)