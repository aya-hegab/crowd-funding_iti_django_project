from django.shortcuts import render, redirect, reverse,get_object_or_404
from .models import *
from .forms import *
from django.http import HttpResponse, HttpResponseRedirect
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from .models import Project, ProjectRating
from .forms import RatingForm
from django.db.models import Avg
from taggit.models import Tag
from django.views.generic import ListView

def projectslist(request):
    myprojectslist = Project.project_list()  # Assuming this returns a list of projects
    user_ratings = {}  # Dictionary to store user ratings for each project
    if request.user.is_authenticated:
        for project in myprojectslist:
            user_rating_instance = ProjectRating.objects.filter(user=request.user, project=project).first()
            if user_rating_instance:
                user_ratings[project.id] = user_rating_instance.rating
            else:
                user_ratings[project.id] = None  # Set to None if user hasn't rated the project

    context = {'myprojectslist': myprojectslist, 'user_ratings': user_ratings}
    return render(request, 'projectdir/projectlist.html', context)

def projectdetailes(request, proid):
    try:
        pro = Project.objects.get(id=proid)
    except Project.DoesNotExist:
        # Handle the case where the project with the given ID does not exist
        return redirect('projects.list')  # Redirect to the project list page or another appropriate page

    comments = pro.comments.all()
    comment_form = CommentForm()
    reports = Report.objects.filter(project=pro)

    # Calculate average rating
    average_rating = ProjectRating.objects.filter(project=pro).aggregate(Avg('rating'))['rating__avg']

    if request.method == 'POST':
        if 'donation_amount' in request.POST:
            donation_amount = Decimal(request.POST.get('donation_amount', 0))
            if donation_amount > 0:
                pro.donation_amount += donation_amount
                pro.save()
                return redirect('projects.list')
        elif 'content' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.project = pro
                new_comment.user = request.user
                new_comment.save()
                return redirect('projects.list')
    else:
        # Handle unknown form submissions or GET requests here
        pass
    tags = pro.tags.values_list('name', flat=True)
    related_projects = list(dict.fromkeys(Project.objects.filter(tags__name__in=tags).exclude(id=pro.id)))[:3]
    context = {
        'project': pro,
        'images': pro.images.all(),
        'comments': comments,
        'comment_form': comment_form,
        'reports': reports,
        'report_form': ReportForm(),
        'average_rating': average_rating,
        'tags': tags,
        'related_projects': related_projects
    }
    return render(request, 'projectdir/projectdetailes.html', context)
    # context = {'project': pro, 'images': pro.images.all(), 'comments': comments, 'comment_form': comment_form,'reports': reports, 'report_form': ReportForm()  }
    # return render(request, 'projectdir/projectdetailes.html', context)
@login_required
def createproject(request):
    if request.method == 'POST':
        metaform = ProjectForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES)
        if metaform.is_valid() and formset.is_valid():
            project = metaform.save(commit=False)
            project.user = request.user  # Assign the current user to the project
            project.save()  # Save the project now that the user is assigned
            metaform.save_m2m()

            for form in formset:
                image = form.cleaned_data.get('image')
                if image:
                    ProjectImage.objects.create(project=project, image=image)
            return redirect(reverse("projects.list"))
    else:
        metaform = ProjectForm()
        formset = ImageFormSet()
    return render(request, 'projectdir/projectcreate.html', {'metaform':  metaform, 'formset': formset})
# @login_required()
# def createproject(request):
#     if request.method == 'POST':
#         metaform = ProjectForm(request.POST)
#         formset = ImageFormSet(request.POST, request.FILES)
#         if metaform.is_valid() and formset.is_valid():
#             project = metaform.save(commit=False)
#             for form in formset:
#                 image = form.cleaned_data.get('image')
#                 if image:
#                     ProjectImage.objects.create(project=project, image=image)
#             return redirect(reverse("projects.list"))
#     else:
#         metaform = ProjectForm()
#         formset = ImageFormSet()
#     return render(request, 'projectdir/projectcreate.html', {'metaform':  metaform, 'formset': formset})


def report_project(request, proid):
    project = Project.objects.get(id=proid)
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            reason = form.cleaned_data['reason']
            # Create a new report instance and save it
            report = Report(project=project, reason=reason)
            report.user = request.user
            report.save()
            return redirect('thank_you_for_reporting')
    else:
        form = ReportForm()
    return render(request, 'projectdir/report_project.html', {'form': form, 'project': project})

def thank_you_for_reporting(request):
    return render(request, 'projectdir/thank_you_for_reporting.html')


def report_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    if request.method == 'POST':
        form = ReportCommentForm(request.POST)
        if form.is_valid():
            reason = form.cleaned_data['comment_reason']
            report = ReportComment(comment=comment, comment_reason=reason)
            report.user = request.user
            report.save()
            return redirect('thank_you_for_reporting')  # Redirect after successful report
        else:
            print(form.errors)  # Print form errors for debugging
    else:
        form = ReportCommentForm()
    return render(request, 'projectdir/report_comment.html', {'form': form, 'comment': comment})



def rate_project(request, project_id):
    project = Project.objects.get(id=project_id)
    user_rating = None
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating_value = form.cleaned_data['rating']
            # Check if the user has already rated this project
            existing_rating = ProjectRating.objects.filter(user=request.user, project=project).first()
            if existing_rating:
                existing_rating.rating = rating_value
                existing_rating.save()
            else:
                ProjectRating.objects.create(user=request.user, project=project, rating=rating_value)
            return redirect(reverse("project.detailes", kwargs={'proid': project_id}))
    else:
        form = RatingForm()
        user_rating_instance = ProjectRating.objects.filter(user=request.user, project=project).first()
        if user_rating_instance:
            user_rating = user_rating_instance.rating

    return render(request, 'projectdir/rate_project.html', {'form': form, 'project': project, 'user_rating': user_rating})

def cancel_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if project.is_cancelable:
        project.delete()
        return redirect(reverse('user_project'))
    else:
        return redirect('user_profile', project_id=project_id)
    

def user_projects(request):
    # Retrieve projects associated with the currently logged-in user
    user_projects = Project.objects.filter(user=request.user)  
    return render(request, 'projectdir/user_profile.html', {'user_projects': user_projects})

def Tagging(request, slug):

    tags = Tag.objects.filter(slug=slug).values_list('name', flat=True)
    projects = Project.objects.filter(tags__name__in=tags)

    context = {
        'tags': tags,
        'projects': projects,
        'tag_name': slug
    }
    return render(request, 'projectdir/project_tag.html', context)

# def user_profile(request):
#     # Retrieve the current user's profile picture URL
#     profile_picture_url = None
#     user_profile = UserProfile.objects.filter(user=request.user).first()
#     if user_profile:
#         profile_picture_url = user_profile.profile_picture.url
#     return render(request, 'project/user_profile.html', {'profile_picture_url': profile_picture_url})

# class TagsList(ListView):
#     model = Project
#     template_name= 'project/user_profile.html'
#     context_object_name='tags'
