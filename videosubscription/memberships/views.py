from django.shortcuts import render
from django.views.generic import ListView
from .models import Membership, UserMembership, Subscription

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
            
