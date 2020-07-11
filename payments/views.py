from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from django.conf import settings
import stripe
# Create your views here.

@login_required()
def donate_home(request):
    print(request.scheme)
    print(request.get_host())
    return render(request, 'payments/home.html')


@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'public_key':settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)

@csrf_exempt
def create_checkout_session(request):
    if request.method == 'GET':
        domain_url = "{}://{}/".format(request.scheme, request.get_host())
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            checkout_session = stripe.checkout.Session.create(
                success_url = domain_url + 'success?success_id={CHECKOUT_SESSION_ID}',
                cancel_url = domain_url + 'cancelled/',
                payment_method_types = ['card'],
                mode = 'payment',
                line_items = [
                    {
                        'name' : 'Donation 1',
                        'quantity' : 1,
                        'currency' : 'inr',
                        'amount' : '100',
                    }
                ]
            )
            return JsonResponse({'sessionId' : checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error' : str(e)})


def success_view(request):
    return render(request, "payments/success.html")

def cancelled_view(request):
    return render(request, "payments/cancelled.html")

