import random
import csv
import io
import zipfile

from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import Max
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from django.core.files.storage import default_storage
from django.http import FileResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser

from .forms import SolutionForm
from .models import Solution, LandingPage
from .forms import RegisterForm

# API

@api_view(['GET'])
@permission_classes([IsAdminUser])
def download_solutions(request):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w') as zip_file:
        # Add each solution file to the zip archive
        for solution in Solution.objects.all():
            filename = solution.file.name
            content = default_storage.open(filename).read()
            zip_file.writestr(filename, content)
        
        # Create and add the metadata CSV to the zip archive
        metadata_buffer = io.StringIO()
        writer = csv.writer(metadata_buffer)
        writer.writerow(['Username', 'Filename', 'Score', 'Submitted At'])

        for solution in Solution.objects.all():
            writer.writerow([solution.user.username, solution.file.name, solution.score, solution.submitted_at])

        zip_file.writestr('metadata.csv', metadata_buffer.getvalue())
    
    buffer.seek(0)
    response = FileResponse(buffer, as_attachment=True, filename='solutions.zip')
    return response

@api_view(['POST'])
@permission_classes([IsAdminUser])
def upload_results(request):
    if 'file' not in request.FILES:
        return Response({"error": "No file uploaded"}, status=400)

    file = request.FILES['file']
    decoded_file = file.read().decode('utf-8').splitlines()
    reader = csv.DictReader(decoded_file)

    for row in reader:
        try:
            user = User.objects.get(username=row['Username'])
            score = int(row['Score'])
            Solution.objects.filter(user=user).update(score=score)
        except User.DoesNotExist:
            continue

    return Response({"status": "Results updated successfully"})

# Views

def landing_page(request):
    content = LandingPage.objects.first()
    return render(request, 'competition/landing_page.html', {'content': content})

@csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('landing_page')
    else:
        form = RegisterForm()
    return render(request, 'competition/register.html', {'form': form})

@csrf_protect
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('landing_page')
        else:
            return render(request, 'competition/login.html', {'form': form, 'error': 'Invalid username or password'})
    else:
        form = AuthenticationForm()
    return render(request, 'competition/login.html', {'form': form})

@login_required
def submit_solution(request):
    if request.method == 'POST':
        form = SolutionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('leaderboard')
    else:
        form = SolutionForm()
    return render(request, 'competition/submit_solution.html', {'form': form})

def leaderboard(request):
    # Get the highest score for each user
    leaderboard_data = Solution.objects.values('user__username').annotate(max_score=Max('score')).order_by('-max_score')
    return render(request, 'competition/leaderboard.html', {'leaderboard': leaderboard_data})

def logout_view(request):
    logout(request)
    return redirect('landing_page')
