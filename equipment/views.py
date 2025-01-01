from .models import Category, Equipment, Rental
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import RentForm, CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth import logout
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User
from django.http import HttpResponse
from datetime import timedelta



# Home page view displaying categories and equipment
def home(request):
    categories = Category.objects.all()
    equipment = Equipment.objects.all()

    category_id = request.GET.get('category_id')
    if category_id:
        category = get_object_or_404(Category, id=category_id)
        equipment = equipment.filter(category=category)

    context = {
        'categories': categories,
        'equipment': equipment,
    }

    return render(request, 'equipment/home.html', context)

# User profile view displaying rented equipment
@login_required
def user_profile(request):
    if request.method == 'POST' and 'logout' in request.POST:
        logout(request)
        return redirect('login')

    rentals = Rental.objects.filter(user=request.user).select_related('equipment')
    return render(request, 'equipment/user_profile.html', {'user': request.user, 'rentals': rentals})

# Rental form view for selecting equipment and rental details
@login_required
def rent_form(request, equipment_id):
    equipment = get_object_or_404(Equipment, id=equipment_id)

    if request.method == 'POST':
        form = RentForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            days = form.cleaned_data['days']
            end_date = start_date + timedelta(days=days)
            payment_method = form.cleaned_data['payment_method']
            comments = form.cleaned_data['comments']

            Rental.objects.create(
                user=request.user,
                equipment=equipment,
                start_date=start_date,
                end_date=end_date,
                payment_method=payment_method,
                comments=comments,
            )
            return redirect('home')
    else:
        form = RentForm(initial={'equipment_name': equipment.name})

    return render(request, 'equipment/rent_form.html', {'form': form, 'equipment': equipment})

# User registration view with email verification
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # Send email verification
            current_site = get_current_site(request)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = get_random_string(length=32)
            verification_link = reverse('email_verify', kwargs={'uidb64': uid, 'token': token})
            email_subject = 'Verify your email'

            email_message = render_to_string('registration/email_verification.html', {
                'user': user,
                'domain': current_site.domain,
                'verification_link': verification_link,
            })

            send_mail(
                email_subject,
                email_message,
                'noreply@example.com',
                [user.email],
                fail_silently=False,
                html_message=email_message
            )

            messages.success(request, "Account created! Check your email to verify your account.")
            return redirect('login')
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': form})

# Email verification view to activate the user account
def email_verify(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and not user.is_active:
        user.is_active = True
        user.save()
        messages.success(request, "Email verified successfully. You can now log in.")
        return redirect('login')
    else:
        return HttpResponse('Invalid or expired verification link.')

# Login view for user authentication
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})
