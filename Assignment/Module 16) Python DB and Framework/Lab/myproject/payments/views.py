import string
import random
from django.shortcuts import render
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .models import Transaction
import paytmchecksum

# Generate unique order id
def generate_order_id():
    return 'ORD' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

def initiate_payment(request):
    if request.method == "POST":
        amount = request.POST.get('amount')
        order_id = generate_order_id()
        
        # Save transaction
        transaction = Transaction.objects.create(order_id=order_id, amount=amount)
        
        # Paytm params dictionary
        paytmParams = dict()
        paytmParams["MID"] = settings.PAYTM_MERCHANT_ID
        paytmParams["ORDERID"] = order_id
        paytmParams["CUST_ID"] = 'CUST_001'
        paytmParams["TXN_AMOUNT"] = "{:.2f}".format(float(amount))
        paytmParams["WEBSITE"] = settings.PAYTM_WEBSITE
        paytmParams["INDUSTRY_TYPE_ID"] = settings.PAYTM_INDUSTRY_TYPE_ID
        paytmParams["CHANNEL_ID"] = settings.PAYTM_CHANNEL_ID
        paytmParams["CALLBACK_URL"] = settings.PAYTM_CALLBACK_URL
        
        # Generate Checksum
        checksum = paytmchecksum.generateSignature(paytmParams, settings.PAYTM_SECRET_KEY)
        paytmParams["CHECKSUMHASH"] = checksum
        
        # staging url
        action_url = f"https://securegw-stage.paytm.in/order/process"
        
        return render(request, 'payments/paytm_redirect.html', {
            'action_url': action_url,
            'paytmParams': paytmParams
        })
    return render(request, 'payments/checkout.html')

@csrf_exempt
def callback(request):
    if request.method == "POST":
        print("--- CALLBACK POST DATA ---")
        print(request.POST.dict())
        print("--------------------------")
        
        paytmParams = request.POST.dict()
        checksum = paytmParams.pop('CHECKSUMHASH', '')
        print("CHECKSUM RECEIVED:", checksum)
        
        # Verify Checksum
        is_verify_signature = False
        if checksum:
            try:
                is_verify_signature = paytmchecksum.verifySignature(paytmParams, settings.PAYTM_SECRET_KEY, checksum)
                print("VERIFY SIGNATURE RESULT:", is_verify_signature)
            except Exception as e:
                print("EXCEPTION IN VERIFY:", e)
                pass
        
        order_id = paytmParams.get('ORDERID', '')
        status = paytmParams.get('STATUS', '')
        resp_msg = paytmParams.get('RESPMSG', '')
        
        if is_verify_signature:
            if order_id:
                try:
                    transaction = Transaction.objects.get(order_id=order_id)
                    transaction.status = status
                    transaction.checksum = checksum
                    transaction.save()
                except Transaction.DoesNotExist:
                    pass
            
            if status == "TXN_SUCCESS":
                msg = "Payment Successful!"
            else:
                msg = f"Payment Failed or Pending. Status: {status}"
        else:
            msg = "Checksum Validation Failed!"
            status = "FAILED"
            
        return render(request, 'payments/callback.html', {
            'msg': msg, 
            'status': status, 
            'order_id': order_id,
            'resp_msg': resp_msg
        })
    return render(request, 'payments/callback.html', {'msg': 'Invalid request'})
