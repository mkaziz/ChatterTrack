import os
import sys

path = os.path.join(os.path.dirname(__file__), "..")

if path not in sys.path:
  sys.path.append(path)
  sys.path.append(os.path.join(path, 'ChatterTrack'))

os.environ['DJANGO_SETTINGS_MODULE'] = 'ChatterTrack.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
