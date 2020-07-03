from .base import *

DEBUG = False
PRODUCTION = True

if PRODUCTION:
    ALLOWED_HOSTS = ['www.nestormonroy.com']
else:
    ALLOWED_HOSTS = ['*']

# if PRODUCTION:
#     SESSION_COOKIE_SECURE = True
#     CSRF_COOKIE_SECURE = True
#     SECURE_SSL_REDIRECT = True
#     SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
#     CORS_REPLACE_HTTPS_REFERER      = True
#     HOST_SCHEME                     = "https://"
#     SECURE_HSTS_INCLUDE_SUBDOMAINS  = True
#     SECURE_HSTS_SECONDS             = 1000000
#     SECURE_FRAME_DENY               = True
# # Let's Encrypt ssl/tls https