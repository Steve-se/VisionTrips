from .base import *
import dj_database_url

DEBUG = False

# DATABASES = {
#     'default': {
#         'ENGINE': env('DATABASE_ENGINE', None),
#         'NAME': env('DATABASE_NAME', None),
#         'USER': env('DATABASE_USER', None),
#         'PASSWORD': env('DATABASE_PASSWORD', None),
#         'HOST': env('DATABASE_HOST', None),
#         'PORT': env('DATABASE_PORT', None),
#     },
# }

# render postgres configuration (live)
DATABASES= {'default': dj_database_url.parse(env('DATABASE_URL'))}

