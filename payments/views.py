from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from django.conf import settings
import stripe
from payments.models import DonationType, DonationAmount

# Create your views here.


@login_required()
def donate_home(request):
    donations = DonationType.objects.all()
    return render(request, "payments/home.html", {"donations": donations})


@login_required()
def donate_main(request, dono_id):
    dono_amounts = DonationAmount.objects.filter(
        donation=DonationType.objects.get(donation_id=dono_id)
    )
    dono_name = DonationType.objects.get(donation_id=dono_id)
    context = {"dono_name": dono_name, "dono_amounts": dono_amounts}
    return render(request, "payments/donation.html", context)


@csrf_exempt
def stripe_config(request):
    if request.method == "GET":
        stripe_config = {"public_key": settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


def create_checkout_session(request):
    if request.method == "POST":
        domain_url = "{}://{}/".format(request.scheme, request.get_host())
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + "success?success_id={CHECKOUT_SESSION_ID}",
                cancel_url=domain_url + "cancelled/",
                payment_method_types=["card"],
                mode="payment",
                line_items=[
                    {
                        "name": request.POST.get("name_dono"),
                        "quantity": int(request.POST.get("no_of_dono")),
                        "currency": "INR",
                        "amount": int(request.POST.get("dono_amount")) * 100,
                    }
                ],
            )
            return JsonResponse({"sessionId": checkout_session["id"]})
        except Exception as e:
            return JsonResponse({"error": str(e)})


def success_view(request):
    return render(request, "payments/success.html")


def cancelled_view(request):
    return render(request, "payments/cancelled.html")
