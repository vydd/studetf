import os
import json

if 'config.json' in os.listdir('.'):
    c = json.loads(open('config.json').read())
else:
    c = {}

STUDENT_USERNAME = c.get('STUDENT_USERNAME', '')
STUDENT_PASSWORD = c.get('STUDENT_PASSWORD', '')
CALENDAR_ID = c.get('CALENDAR_ID', '')
GECKODRIVER_PATH = c.get('GECKODRIVER_PATH', '')
CERTIFICATE_PATH = c.get('CERTIFICATE_PATH', '')
LOGLEVEL = c.get('LOGLEVEL', 'INFO')

STUDENT_USERNAME = os.environ.get('STUDENT_USERNAME', STUDENT_USERNAME)
STUDENT_PASSWORD = os.environ.get('STUDENT_PASSWORD', STUDENT_PASSWORD)
CALENDAR_ID = os.environ.get('CALENDAR_ID', CALENDAR_ID)
GECKODRIVER_PATH = os.environ.get('GECKODRIVER_PATH', GECKODRIVER_PATH)
CERTIFICATE_PATH = os.environ.get('CERTIFICATE_PATH', CERTIFICATE_PATH)
LOGLEVEL = os.environ.get('LOGLEVEL', LOGLEVEL)

LOGFORMAT = '%(asctime)-15s %(levelname)s %(message)s'
