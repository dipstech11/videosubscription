from django.shortcuts import render
from django.views.generic import ListView
from django.http import HttpResponseRedirect
from django.conf import settings
from django.urls import reverse
from django.contrib import messages
from .models import Membership, UserMembership, Subscription
import stripe

def get_user_membership(request):
    user_membership = UserMembership.objects.filter(user=request.user)
    if user_membership.exists():
        return user_membership.first()
    else:
        return None

def get_user_subscription(request):
    user_subscription = Subscription.objects.filter(
                        user_membership=get_user_membership(request))

    if user_subscription.exists():
        user_subscription = user_subscription.first()
        return user_subscription
    else:
        return None

def get_selected_membership(request):
    membership_type = request.session['selected_membership_type']
    selected_membership_qs = Membership.objects.filter(
                    membership_type=membership_type)

    if selected_membership_qs.exists():
        return selected_membership_qs.first()
    else:
        return None

class MembershipSelectView(ListView):
    model = Membership

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        current_membership = get_user_membership(self.request)
        context['current_membership'] = str(current_membership.membership)
        return context



    def post(self,request, *kwargs):
        selected_membership_type = request.POST.get('membership_type')

        user_membership = get_user_membership(request)
        user_subscription = get_user_subscription(request)

        selected_membership_qs = Membership.objects.filter(
                    membership_type=selected_membership_type)

        if selected_membership_qs.exists():
            selected_membership = selected_membership_qs.first()


        #validations
        if user_membership.membership == selected_membership:
            if user_subscription !=None:
                messages.info(request, "You allready have this membership. Your next\
                payment due on {}".format("get this value from stripe"))
                return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


        #assign to the session
        request.session['selected_membership_type'] = selected_membership.membership_type
        return HttpResponseRedirect(reverse('memberships:payment'))



def PaymentView(request):
    user_membership = get_user_membership(request)
    selected_membership = get_selected_membership(request)

    publishKey = settings.STRIPE_PUBLISHABLE_KEY

    context= {
    'publishKey': publishKey,
    'selected_membership':selected_membership
    }
    return render(request, "memberships/membership_payment.html", context)
