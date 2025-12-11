from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
import json
from json import JSONDecodeError
from .models import MembershipPayment, PaymentWebhookLog
from accounts.decorators import picture_required


class PaymentListView(LoginRequiredMixin, ListView):
    """List user's payment records"""
    model = MembershipPayment
    template_name = 'membership/payment_list.html'
    context_object_name = 'payments'
    login_url = 'login'
    
    def get_queryset(self):
        return MembershipPayment.objects.filter(user=self.request.user).order_by('-created_at')


class PaymentDetailView(LoginRequiredMixin, DetailView):
    """View payment details"""
    model = MembershipPayment
    template_name = 'membership/payment_detail.html'
    context_object_name = 'payment'
    login_url = 'login'
    
    def get_queryset(self):
        return MembershipPayment.objects.filter(user=self.request.user)


class PaymentCreateView(LoginRequiredMixin, CreateView):
    """Create a new membership payment"""
    model = MembershipPayment
    template_name = 'membership/payment_create.html'
    fields = ('provider',)
    login_url = 'login'
    success_url = reverse_lazy('membership:payment_list')
    
    @picture_required
    def get(self, request, *args, **kwargs):
        # Check if user already has active payment
        active_payment = MembershipPayment.objects.filter(
            user=request.user,
            status='success'
        ).exists()
        
        if active_payment:
            messages.info(request, 'You have already completed your membership payment.')
            return redirect('member_dashboard')
        
        return super().get(request, *args, **kwargs)
    
    def form_valid(self, form):
        payment = form.save(commit=False)
        payment.user = self.request.user
        payment.amount = 15000.00  # 15,000 TZS
        payment.status = 'pending'
        payment.save()
        
        messages.info(self.request, 'Payment initiated. Follow the instructions to complete payment.')
        return super().form_valid(form)


@csrf_exempt
@require_http_methods(['POST'])
def mpesa_webhook(request):
    """
    M-Pesa payment webhook handler
    
    This endpoint receives payment confirmations from M-Pesa API
    """
    try:
        data = json.loads(request.body)
    except JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    
    # Log the webhook
    PaymentWebhookLog.objects.create(
        provider='mpesa',
        event_type=data.get('Body', {}).get('stkCallback', {}).get('ResultCode'),
        raw_data=data,
    )
    
    # Handle payment confirmation
    # This is a stub - implement actual M-Pesa verification
    # You should:
    # 1. Verify webhook signature
    # 2. Extract transaction details
    # 3. Update MembershipPayment record
    # 4. Send confirmation email
    
    return JsonResponse({'status': 'success'})


@csrf_exempt
@require_http_methods(['POST'])
def stripe_webhook(request):
    """
    Stripe payment webhook handler
    
    This endpoint receives payment confirmations from Stripe
    """
    try:
        data = json.loads(request.body)
    except JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    
    # Log the webhook
    PaymentWebhookLog.objects.create(
        provider='stripe',
        event_type=data.get('type'),
        raw_data=data,
    )
    
    # Handle payment confirmation
    # This is a stub - implement actual Stripe verification
    # You should:
    # 1. Verify webhook signature with Stripe
    # 2. Extract transaction details
    # 3. Update MembershipPayment record
    # 4. Send confirmation email
    
    return JsonResponse({'status': 'success'})
