import os

settings_path = os.path.join('myproject', 'settings.py')
with open(settings_path, 'r') as f:
    content = f.read()

# Add payments to INSTALLED_APPS
if "'payments'" not in content and '"payments"' not in content:
    content = content.replace("'doctors',\n]", "'doctors',\n    'payments',\n]")

# Add Paytm Configs
paytm_configs = """
# Paytm Configuration
PAYTM_MERCHANT_ID = 'YOUR_TEST_MERCHANT_ID'
PAYTM_SECRET_KEY = 'YOUR_TEST_SECRET_KEY'
PAYTM_WEBSITE = 'WEBSTAGING'
PAYTM_CHANNEL_ID = 'WEB'
PAYTM_INDUSTRY_TYPE_ID = 'Retail'
PAYTM_CALLBACK_URL = 'http://127.0.0.1:8000/payments/callback/'
"""
if "PAYTM_MERCHANT_ID" not in content:
    content += "\n" + paytm_configs

with open(settings_path, 'w') as f:
    f.write(content)
print("Settings updated successfully.")
