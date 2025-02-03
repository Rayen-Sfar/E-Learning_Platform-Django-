from django.shortcuts import render, redirect,get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,update_session_auth_hash, logout as auth_logout
from django.contrib import messages
from django.core.files.storage import FileSystemStorage

from .models import Video, Comment
from .forms import CommentForm, Video1Form, CourseForm
from django.contrib.auth.decorators import login_required
from .models import Tutor, Course, Video1

def home(request):
    return render(request, 'pages/home.html')

def indexLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user = authenticate(request, username=username, password=pass1)
        if user is not None:
            login(request, user)
            return redirect('courses')  # Remplacez 'pages/home.html' par le nom de l'URL
        else:
            return HttpResponse("Username or Password is incorrect!!!")
    return render(request, "pages/indexLogin.html")
def join2 (request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if pass1!=pass2:
            return HttpResponse("Your password and confrom password are not same!!")
        else:

            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
        return redirect('indexLogin')

    return render(request,"pages/join2.html")

def logout(request):
    auth_logout(request)
    return redirect('indexLogin')

# Create your views here.


def about (request):
    return render(request, 'pages/about.html')
@login_required
def contact(request):
    return render(request, 'pages/contact.html')
@login_required
def courses(request):
    return render(request, 'pages/courses.html')
def playlist(request):
    return render(request, 'pages/playlist.html')
@login_required
def teacher_private_account(request):
    return render(request, 'pages/teacher_private_account.html')
@login_required
def teacher_profile(request):
    return render(request, 'pages/teacher_profile.html')
@login_required
def teachers(request):
    return render(request, 'pages/teachers.html')
@login_required
def update(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        old_pass = request.POST.get('old_pass')
        new_pass = request.POST.get('new_pass')
        c_pass = request.POST.get('c_pass')
        profile_pic = request.FILES.get('profile_pic')
        
        user = request.user

        # Check old password
        if not user.check_password(old_pass):
            messages.error(request, "Your old password is incorrect!")
            return redirect('update')

        # Update name and email
        if name:
            user.username = name
        if email:
            user.email = email

        # Update password
        if new_pass and new_pass == c_pass:
            user.set_password(new_pass)
        elif new_pass != c_pass:
            messages.error(request, "New password and confirm password do not match!")
            return redirect('update')

        # Handle profile picture
        if profile_pic:
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name, profile_pic)
            user.profile.profile_pic = fs.url(filename)  # Assuming you have a profile model linked to user with a profile_pic field

        user.save()
        
        # Update session auth hash to prevent logout after password change
        update_session_auth_hash(request, user)
        
        messages.success(request, "Your profile has been updated successfully!")
        return redirect('update')

    return render(request, 'pages/update.html')

def navbar(request):
    return render(request, 'navbar.html')

@login_required
def watch_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    comments = video.comments.all()
    new_comment = None

    # Handle comment form submission
    if request.method == 'POST' and 'add_comment' in request.POST:
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.user = request.user
            new_comment.video = video
            new_comment.save()
            messages.success(request, "Your comment has been added.")
            return redirect('watch_video', video_id=video_id)
    else:
        comment_form = CommentForm()

    # Handle like button
    if request.method == 'POST' and 'like' in request.POST:
        if request.user.is_authenticated:
            if request.user in video.likes.all():
                video.likes.remove(request.user)
            else:
                video.likes.add(request.user)
            return redirect('watch_video', video_id=video_id)
        else:
            messages.error(request, "You must be logged in to like a video.")
            return redirect('watch_video', video_id=video_id)

    return render(request, 'pages/watch_video.html', {
        'video': video,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
    })




# views de teacher_private

@login_required
def teacher_profile(request):
    tutor = Tutor.objects.get(id=1)  # Vous pouvez modifier cela pour obtenir dynamiquement le tuteur
    courses = Course.objects.filter(tutor=tutor)

    if request.method == 'POST':
        if 'add_course' in request.POST:
            course_form = CourseForm(request.POST, request.FILES)
            if course_form.is_valid():
                course = course_form.save(commit=False)
                course.tutor = tutor
                course.save()
                return redirect('teacher_profile')
        elif 'delete_course' in request.POST:
            course_id = request.POST.get('course_id')
            Course.objects.get(id=course_id).delete()
            return redirect('teacher_profile')
    
    else:
        course_form = CourseForm()

    # Calcul des totaux pour l'affichage
    videos_count = sum(course.videos.count() for course in courses)
    likes_count = sum(video.likes for course in courses for video in course.videos.all())
    comments_count = sum(video.comments_count for course in courses for video in course.videos.all())

    context = {
        'tutor': tutor,
        'courses': courses,
        'course_form': course_form,
        'videos_count': videos_count,
        'likes_count': likes_count,
        'comments_count': comments_count,
    }
    return render(request, 'pages/teacher_private_account.html', context)
