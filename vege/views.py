from django.shortcuts import render, redirect
from .models import*
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from .models import Receipe, Like, Comment, ReceipeView
from .forms import UserUpdateForm

def receipes(request):
    if request.method == "POST":
        data = request.POST
        receipe_name = data.get('receipe_name')
        receipe_description = data.get('receipe_description')
        receipe_steps = request.POST.get("receipe_steps")   # <-- get steps
        receipe_image = request.FILES.get('receipe_image')
        
        Receipe.objects.create(
            user = request.user,
            receipe_name = receipe_name,
            receipe_description = receipe_description,
            receipe_steps = receipe_steps,
            receipe_image = receipe_image,
        )
        
        return redirect('/receipes')
    queryset = Receipe.objects.all().order_by('-receipe_view_count')
    
    
    if request.GET.get('search'):
        queryset = queryset.filter(receipe_name__icontains = request.GET.get('search'))
    context = {'receipes': queryset}
    return render(request, 'receipes.html', context)

def update_receipe(request, id):
    queryset = Receipe.objects.get(id = id)
    
    
    if request.method == "POST":
        data = request.POST
        receipe_name = data.get('receipe_name')
        receipe_description = data.get('receipe_description')
        receipe_steps = data.get('receipe_steps')
        receipe_image = request.FILES.get('receipe_image')
        
        queryset.receipe_name = receipe_name
        queryset.receipe_description = receipe_description
        queryset.receipe_steps = receipe_steps
        
        if receipe_image:
            queryset.receipe_image = receipe_image
            
        queryset.save()
        return redirect('/receipes')
        
    context = {'receipe': queryset}   
    return render(request, 'update_receipes.html', context)

# def delete_receipe(request, id):
#     queryset = Receipe.objects.get(id = id)
#     queryset.delete()            
#     return redirect('/receipes/')   

def delete_receipe(request, id):
    receipe = get_object_or_404(Receipe, id=id)

    # Only owner can delete
    if receipe.user == request.user:
        receipe.delete()
        messages.success(request, "Your recipe was deleted successfully.")
    else:
        messages.error(request, "You are not allowed to delete this recipe.")

    return redirect('/receipes/')                                
    
def login_page(request):
    
    if request.method == "POST":
        
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not User.objects.filter(username = username).exists():
            messages.error(request, 'invalid username')
            return redirect('/login/')
        
        user = authenticate(request, username = username , password = password)
        
        if user is None:
            messages.error(request, 'invalid password')
            return redirect('/login/')
        
        else:
            login(request, user)
            return redirect('/receipes/')
        
    return render(request, 'login.html') 

def logout_page(request):
    logout(request)
    return redirect('/login/')

@login_required
def like_receipe(request, id):
    receipe = get_object_or_404(Receipe, id=id)
    like , created = Like.objects.get_or_create(user=request.user, receipe = receipe)
    if not created:
        like.delete()
    return redirect('/receipes/')

@login_required
def add_comment(request, id):
    if request.method == "POST":
        receipe = get_object_or_404(Receipe, id=id)
        text = request.POST.get("comment")
        if text.strip():
            Comment.objects.create(user=request.user, receipe = receipe, text=text)
    return redirect('/receipes/')

@login_required
def delete_comment(request, id):
    comment = get_object_or_404(Comment, id=id)
    if comment.user == request.user:            #only the owner can delete
        comment.delete()
    return redirect('/receipes/')
    
def register_page(request):
    
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = User.objects.filter(username = username)
        
        if user.exists():
            messages.info(request, 'username already existed')
            return redirect('/register/')
        
        user = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            username = username,    
        )
        user.set_password(password)
        user.save()
        
        messages.info(request, 'Account created successfully')
        
        return redirect('/register/')
    
    return render(request, 'register.html')  

def receipe_detail(request, pk):
    receipe = get_object_or_404(Receipe, pk=pk)

    if request.user.is_authenticated:
        # Check if user already viewed
        if not ReceipeView.objects.filter(user=request.user, receipe=receipe).exists():
            receipe.receipe_view_count += 1
            receipe.save(update_fields=['receipe_view_count'])
            
            # Save view record
            ReceipeView.objects.create(user=request.user, receipe=receipe)

    return render(request, "receipe_detail.html", {"receipe": receipe})

def receipe_list(request):
    receipes = Receipe.objects.all().order_by('-receipe_view_count')
    return render(request, "receipes.html", {"receipes": receipes})

@login_required
def add_receipe(request):
    if not request.user.is_authenticated:
        messages.warning(request, "You must be logged in to add a recipe!")
        return redirect('login_page')
    
    if request.method == "POST":
        data = request.POST
        receipe_name = data.get('receipe_name')
        receipe_description = data.get('receipe_description')
        receipe_steps = data.get("receipe_steps")
        receipe_image = request.FILES.get('receipe_image')

        Receipe.objects.create(
            user=request.user,
            receipe_name=receipe_name,
            receipe_description=receipe_description,
            receipe_steps=receipe_steps,
            receipe_image=receipe_image,
        )
        return redirect("receipes")

    return render(request, "add_receipe.html")

@login_required
def profileSetting(request):
    u_form = UserUpdateForm(instance=request.user)  # prefill user data
    return render(request, "profileSetting.html", {"u_form": u_form})

@login_required
def profile_update(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        # Update User model
        request.user.username = request.POST.get("username")
        request.user.email = request.POST.get("email")
        request.user.save()

        # Update Profile model
        profile.bio = request.POST.get("bio")
        profile.users_about = request.POST.get("users_about")

        if request.FILES.get("Profile_picture"):
            profile.Profile_picture = request.FILES.get("Profile_picture")

        profile.save()
        messages.success(request, "Profile updated successfully!")
        return redirect("profileSetting")

    return render(request, "profile_update.html", {"profile": profile})


        
@login_required
def profile_delete(request):
    if request.method == "POST":
        user = request.user
        user.delete()
        messages.success(request, "Your account has been deleted....!")
        return redirect('/register/')
    return render(request, 'profile_delete.html')

def user_profile(request, username):
    # Get the User object
    user = get_object_or_404(User, username=username)

    # Ensure a Profile exists for this user
    profile, created = Profile.objects.get_or_create(user=user)

    # Get all recipes by this user
    user_receipes = Receipe.objects.filter(user=user)

    context = {
        'profile': profile,
        'user_receipes': user_receipes,
    }
    return render(request, 'user_profile.html', context)