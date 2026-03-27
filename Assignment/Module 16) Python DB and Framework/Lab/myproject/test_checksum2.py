import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.conf import settings
import paytmchecksum

paytmParams = dict()
try:
    is_verify = paytmchecksum.verifySignature(paytmParams, settings.PAYTM_SECRET_KEY, "")
    print("Verification result:", is_verify)
except Exception as e:
    import traceback
    traceback.print_exc()
