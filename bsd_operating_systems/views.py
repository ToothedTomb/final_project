from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from .forms import OperatingSystemsForm
from .models import OperatingSystems, Comment

def homepage_view(request):
    # Get search query from URL parameters
    search_query = request.GET.get('search', '')
    
    # Filter operating systems based on search query
    if search_query:
        all_operating_systems = OperatingSystems.objects.filter(
            Q(name__icontains=search_query) |
            Q(Package_Manager__icontains=search_query) |
            Q(CPU_Architecture__icontains=search_query) |
            Q(Latest_Version__icontains=search_query)
        )
    else:
        all_operating_systems = OperatingSystems.objects.all()
    
    # Handle form submissions
    if request.method == 'POST':
        # FIRST: Check if this is a comment submission
        if 'comment_text' in request.POST and 'os_id' in request.POST:
            if not request.user.is_authenticated:
                messages.error(request, "You need to login to add comments.")
                return redirect('homepage')
            
            os_id = request.POST.get('os_id')
            os_instance = get_object_or_404(OperatingSystems, pk=os_id)
            text = request.POST.get('comment_text')
            
            if text:
                # Update or create comment for this user and OS
                comment, created = Comment.objects.update_or_create(
                    operating_system=os_instance,
                    user=request.user,
                    defaults={'text': text}
                )
                if created:
                    messages.success(request, "Comment added successfully!")
                else:
                    messages.success(request, "Comment updated successfully!")
                return redirect('homepage')
            else:
                messages.error(request, "Comment cannot be empty.")
                return redirect('homepage')
        
        # If not a comment submission, check if user is superuser
        if not request.user.is_superuser:
            messages.error(request, "Only the root user can add operating systems.")
            return redirect('homepage')
        
        # Handle OS form (only for superuser)
        form = OperatingSystemsForm(request.POST, request.FILES)
        if form.is_valid():
            os_instance = form.save()
            messages.success(request, "Operating system added successfully!")
            return redirect('homepage')
        else:
            messages.error(request, "Please fix the errors in the form.")
    
    # For GET requests, just show the form
    form = OperatingSystemsForm()
    
    # For each OS, check if current user has a comment
    os_data = []
    for os in all_operating_systems:
        user_comment = None
        if request.user.is_authenticated:
            try:
                user_comment = Comment.objects.get(operating_system=os, user=request.user)
            except Comment.DoesNotExist:
                user_comment = None
        os_data.append({
            'os': os,
            'user_comment': user_comment
        })
    
    return render(request, "bsd-os/index.html",
        {
            "os_data": os_data,
            "form": form,
            "user": request.user,
            "search_query": search_query
        }              
    )

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('homepage')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    
    return render(request, 'bsd-os/login.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Account created for {user.username}!")
            return redirect('homepage')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserCreationForm()
    
    return render(request, 'bsd-os/signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('homepage')

# Delete Comment - User can delete their own comment
@login_required
@require_POST
def delete_comment_view(request, os_id):
    os_instance = get_object_or_404(OperatingSystems, pk=os_id)
    
    try:
        comment = Comment.objects.get(operating_system=os_instance, user=request.user)
        comment.delete()
        messages.success(request, "Comment deleted successfully!")
    except Comment.DoesNotExist:
        messages.error(request, "Comment not found.")
    
    return redirect('homepage')

# Create OS - Only superuser
@login_required
def create_os_view(request):
    if not request.user.is_superuser:
        messages.error(request, "Only the root user can add operating systems.")
        return redirect('homepage')
    
    if request.method == 'POST':
        form = OperatingSystemsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Operating system added successfully!")
            return redirect('homepage')
    else:
        form = OperatingSystemsForm()
    
    return render(request, 'bsd-os/create_os.html', {'form': form})

# Edit OS - Only superuser
@login_required
def edit_os_view(request, pk):
    if not request.user.is_superuser:
        messages.error(request, "Only the root user can edit operating systems.")
        return redirect('homepage')
    
    os_instance = get_object_or_404(OperatingSystems, pk=pk)
    
    if request.method == 'POST':
        form = OperatingSystemsForm(request.POST, request.FILES, instance=os_instance)
        if form.is_valid():
            form.save()
            messages.success(request, "Operating system updated successfully!")
            return redirect('homepage')
    else:
        form = OperatingSystemsForm(instance=os_instance)
    
    return render(request, 'bsd-os/edit_os.html', {'form': form, 'os': os_instance})

# Delete OS - Only superuser
@login_required
def delete_os_view(request, pk):
    if not request.user.is_superuser:
        messages.error(request, "Only the root user can delete operating systems.")
        return redirect('homepage')
    
    os_instance = get_object_or_404(OperatingSystems, pk=pk)
    
    if request.method == 'POST':
        os_instance.delete()
        messages.success(request, "Operating system deleted successfully!")
        return redirect('homepage')
    
    return render(request, 'bsd-os/delete_os.html', {'os': os_instance})