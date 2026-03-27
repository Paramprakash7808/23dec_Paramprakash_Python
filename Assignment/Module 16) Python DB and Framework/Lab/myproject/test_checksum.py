import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.conf import settings
import paytmchecksum

paytmParams = dict()
paytmParams["MID"] = settings.PAYTM_MERCHANT_ID
paytmParams["ORDER_ID"] = "ORD12345"
paytmParams["CUST_ID"] = 'CUST_001'
paytmParams["TXN_AMOUNT"] = "10.00"
paytmParams["WEBSITE"] = settings.PAYTM_WEBSITE
paytmParams["INDUSTRY_TYPE_ID"] = settings.PAYTM_INDUSTRY_TYPE_ID
paytmParams["CHANNEL_ID"] = settings.PAYTM_CHANNEL_ID
paytmParams["CALLBACK_URL"] = settings.PAYTM_CALLBACK_URL

try:
    checksum = paytmchecksum.generateSignature(paytmParams, settings.PAYTM_SECRET_KEY)
    print("Checksum generated successfully:", checksum)
except Exception as e:
    import traceback
    traceback.print_exc()
