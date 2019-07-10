import os


TOKEN = os.getenv('TG_TOKEN')
URL = os.getenv('URL')
MOVIEDB_TOKEN = os.getenv('MOVIED_TOKEN')
IMAGE_BASE_URL = os.getenv('IMAGE_BASE_URL')
WEBHOOK_SSL_CERT = './webhook_cert.pem'
WEBHOOK_SSL_PRIV = './webhook_pkey.pem'
SSL = (WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV)