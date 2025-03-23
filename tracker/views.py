from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from .forms import UserSignupForm, WaterIntakeForm
from .models import WaterIntake
from datetime import date
def home(request):
    return render(request, 'tracker/home.html')


# Signup View
def signup(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')  # Redirect to login page after signup
    else:
        form = UserSignupForm()
    return render(request, 'tracker/signup.html', {'form': form})


# Login View
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'tracker/login.html')

# Logout View
@login_required
def user_logout(request):
    logout(request)
    return redirect('home')

# Dashboard View
@login_required
def dashboard(request):
    water_intake_list = WaterIntake.objects.filter(user=request.user).order_by('-date')
    paginator = Paginator(water_intake_list, 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.method == 'POST':
        form = WaterIntakeForm(request.POST)
        if form.is_valid():
            if WaterIntake.objects.filter(user=request.user, date=date.today()).exists():
                error_message = "You have already logged your water intake for today."
                return render(request, 'tracker/dashboard.html', {'form': form, 'error_message': error_message, 'page_obj': page_obj})
            intake = form.save(commit=False)
            intake.user = request.user
            intake.save()
            return redirect('dashboard')
    else:
        form = WaterIntakeForm()
    return render(request, 'tracker/dashboard.html', {'form': form, 'page_obj': page_obj})

# AJAX: Calculate Difference
@login_required
def calculate_difference(request):
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        intake_start = WaterIntake.objects.filter(user=request.user, date=start_date).first()
        intake_end = WaterIntake.objects.filter(user=request.user, date=end_date).first()

        if intake_start and intake_end:
            difference = abs(intake_start.quantity - intake_end.quantity)
            return JsonResponse({'difference': difference})
        return JsonResponse({'error': 'No data found for the selected dates'}, status=404)


@csrf_exempt  # Use this only if CSRF token is not handled on the frontend
@login_required
def update_water_intake(request):
    if request.method == "POST":
        intake_id = request.POST.get('id')
        new_quantity = request.POST.get('quantity')

        try:
            intake = WaterIntake.objects.get(id=intake_id, user=request.user)
            intake.quantity = float(new_quantity)
            intake.save()
            return JsonResponse({"success": True, "message": "Water intake updated successfully"})
        except WaterIntake.DoesNotExist:
            return JsonResponse({"success": False, "message": "Water intake entry not found"}, status=404)
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=500)
    return JsonResponse({"success": False, "message": "Invalid request"}, status=400)



@csrf_exempt  # Use only if CSRF token is not handled on the frontend
@login_required
def delete_water_intake(request):
    if request.method == "POST":
        intake_id = request.POST.get('id')

        try:
            intake = WaterIntake.objects.get(id=intake_id, user=request.user)
            intake.delete()
            return JsonResponse({"success": True, "message": "Water intake entry deleted successfully"})
        except WaterIntake.DoesNotExist:
            return JsonResponse({"success": False, "message": "Water intake entry not found"}, status=404)
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=500)
    return JsonResponse({"success": False, "message": "Invalid request"}, status=400)