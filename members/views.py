from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse

def home_view(request):
    """View for home page"""
    return render(request, 'members/home.html')  # Updated path

def login_view(request):
    """View for user login"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Debug info
        print(f"Login attempt for username: {username}")
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            print(f"Login successful for {username}")
            messages.success(request, "Login successful!")
            
            # Get next URL or default to home
            next_url = request.POST.get('next', '/')
            return redirect(next_url)
        else:
            print(f"Login failed for {username}")
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'members/login.html')  # Updated path

def logout_view(request):
    """View for user logout"""
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('/')

def signup_view(request):
    """View for user registration"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        full_name = request.POST.get('full_name', '')
        
        # Debug info
        print(f"Signup attempt: {username}, {email}")
        
        # Check passwords match
        if password1 != password2:
            messages.error(request, "Passwords don't match")
            return render(request, 'members/signup.html')  # Updated path
        
        # Check if username exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return render(request, 'members/signup.html')  # Updated path
        
        # Create user
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1
            )
            
            # Set name if provided
            if full_name:
                names = full_name.split(maxsplit=1)
                user.first_name = names[0]
                if len(names) > 1:
                    user.last_name = names[1]
                user.save()
            
            # Log in the user
            auth_user = authenticate(username=username, password=password1)
            login(request, auth_user)
            
            print(f"Signup successful for {username}")
            messages.success(request, "Your account has been created!")
            
            # Redirect to homepage
            return redirect('/')
            
        except Exception as e:
            print(f"Signup error: {str(e)}")
            messages.error(request, f"Error creating account: {str(e)}")
    
    return render(request, 'members/signup.html')  # Updated path

@login_required
def profile_view(request):
    """Profile view that renders HTML directly"""
    user = request.user
    
    # Create HTML for profile page
    profile_html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>User Profile</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #0a1128;
            color: white;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }}
        .profile-container {{
            width: 100%;
            max-width: 800px;
            margin: 30px auto;
            border-radius: 10px;
            overflow: hidden;
        }}
        h1 {{
            text-align: center;
            color: #fca311;
            font-size: 2.5rem;
            margin-bottom: 40px;
        }}
        .profile-section {{
            background: rgba(13, 20, 44, 0.95);
            margin-bottom: 20px;
            border-radius: 8px;
            overflow: hidden;
        }}
        .profile-section h2 {{
            color: #fca311;
            background: rgba(10, 16, 40, 0.95);
            margin: 0;
            padding: 15px 20px;
            border-bottom: 2px solid rgba(252, 163, 17, 0.3);
            font-size: 1.5rem;
        }}
        .field {{
            padding: 15px 20px;
            display: flex;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        }}
        .field:last-child {{
            border-bottom: none;
        }}
        .field-label {{
            font-weight: bold;
            width: 150px;
            color: rgba(255, 255, 255, 0.8);
        }}
        .field-value {{
            flex: 1;
        }}
        .actions {{
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-top: 30px;
        }}
        .btn {{
            background: #fca311;
            color: #0a1128;
            padding: 12px 30px;
            text-decoration: none;
            border-radius: 50px;
            font-weight: bold;
            border: 2px solid #fca311;
            transition: all 0.3s ease;
            cursor: pointer;
        }}
        .btn:hover {{
            background: transparent;
            color: #fca311;
        }}
        .btn-home {{
            background: transparent;
            color: #fca311;
            border-color: #fca311;
        }}
        .btn-home:hover {{
            background: rgba(252, 163, 17, 0.1);
        }}
        a {{
            text-decoration: none;
            color: inherit;
        }}
    </style>
</head>
<body>
    <div class="profile-container">
        <h1>User Profile</h1>
        
        <div class="profile-section">
            <h2>Account Information</h2>
            <div class="field">
                <div class="field-label">Username:</div>
                <div class="field-value">{user.username}</div>
            </div>
            <div class="field">
                <div class="field-label">Email:</div>
                <div class="field-value">{user.email or "Not provided"}</div>
            </div>
            <div class="field">
                <div class="field-label">Date Joined:</div>
                <div class="field-value">{user.date_joined.strftime('%B %d, %Y')}</div>
            </div>
        </div>
        
        <div class="profile-section">
            <h2>Personal Information</h2>
            <div class="field">
                <div class="field-label">First Name:</div>
                <div class="field-value">{user.first_name or "Not provided"}</div>
            </div>
            <div class="field">
                <div class="field-label">Last Name:</div>
                <div class="field-value">{user.last_name or "Not provided"}</div>
            </div>
        </div>
        
        <div class="actions">
            <a href="/" class="btn btn-home">Home</a>
            
        </div>
    </div>
</body>
</html>
"""
    
    return HttpResponse(profile_html)