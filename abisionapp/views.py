from django.shortcuts import render,get_object_or_404,redirect
from django.shortcuts import render
from django.contrib import messages
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.db.models import Count
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from abisionapp.forms import RateyourcompanyForm, EmailsingupForm, SignupfinishForm, OtpverificationForm, postform, CommentForm, Resumeform,Resume_headlineform,Keyskills_form,Employmentform, Educationform,Itskillsform, Profile_summaryform, Projectform,career_profileform, Personal_detailsform, CombinedJobForm, JobApplicationForm, DynamicQuestionForm, CompanyForm
from abisionapp.models import Emailsignup, Designations, SignupFinish, Otpverifiction, Post, profile, Resume,Resume_headline,Keyskills,Employment,Education,Itskills,Project, Profile_summary,Career_profile,Personal_details, Follow, Notification, JobPosting, Qualification, JobQualification, JobApplication, Answer, Company
from django.core.mail import send_mail
import json
from datetime import datetime
from django.conf import settings
from django.http import HttpResponse
import random
from django.http import JsonResponse
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from taggit.models import Tag
from django.urls import reverse

# Create your views here.
def home(request):
    return render(request,"home.html")

# def login(request):
#     return render(request, 'registration/login.html')


def Rateyourcompany(request):
    form = RateyourcompanyForm()
    return render(request, 'Rateyourcompany.html',{'form':form})

def employer(request):
    return render(request, "employer.html")



def signup(request):
    sent = False
    form = EmailsingupForm()
    
    if request.method == "POST":
        form = EmailsingupForm(data=request.POST)
        
        if form.is_valid():
            # Extracting form data
            email = form.cleaned_data.get('Email')
            username = form.cleaned_data.get('Username')
            password = form.cleaned_data.get('password')
            
            # Check if the user already exists
            if User.objects.filter(username=username).exists():
                form.add_error('Username', 'Username already exists')
            # elif User.objects.filter(email=email).exists():
            #     form.add_error('Email', 'Email already exists')
            else:
                # Create the user in the Django User model
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                
                # Generate OTP for verification
                global otpveri
                otpveri = ''.join([str(random.randint(0, 9)) for _ in range(6)])
                
                # Send the OTP via email
                subject = 'Thank you for registering to our site'
                message = f'Your OTP is: {otpveri}'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [email]
                send_mail(subject, message, email_from, recipient_list)
                
                # Set sent flag to True and redirect to OTP verification page
                sent = True
                return HttpResponseRedirect('/Otpverification/', {'sent': sent})
    
    return render(request, 'signup.html', {'form': form, 'sent': sent})

def login_view(request):
    signupfinish = None 
    
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)

                # # Check for 'next' parameter in the request
                # next_url = request.POST.get('next') or request.GET.get('next')

                # if next_url:
                #     return redirect(next_url)

                
                # Check if signupfinish_id is in session
                signupfinish_id = request.session.get('signupfinish_id')

                # Redirect based on conditions

                if signupfinish_id:
                    signupfinish = get_object_or_404(SignupFinish, id=signupfinish_id)
                    return redirect('/tag/')  # Redirect to /tag/ if login is successful
                

                else:
                    # If no signupfinish_id, redirect to a different page
                    return redirect('/profile/')
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form, 'signupfinish': signupfinish, 'next': request.GET.get('next')})


@login_required
def signup2(request):
    sent = False
    formobj = SignupfinishForm()

    if request.method == "POST":
        formobj = SignupfinishForm(data=request.POST)
        
        if formobj.is_valid():  # Validate the form before saving
            # Extracting form data directly from cleaned_data after validation
            firstname = formobj.cleaned_data['Firstname']
            lastname = formobj.cleaned_data['Lastname']
            mobile = formobj.cleaned_data['Mobile']
            companyname = formobj.cleaned_data['Companyname']
            companywebsite = formobj.cleaned_data['Companywebsite']
            designation = formobj.cleaned_data['Designation']
            
            # Save the SignupFinish object
            form = SignupFinish(
                Firstname=firstname,
                Lastname=lastname,
                Mobile=mobile,
                Companyname=companyname,
                Companywebsite=companywebsite,
                Designation=designation
            )
            
            # Attach the user to the form if needed
            form.user = request.user  # If your SignupFinish model has a user field
            form.save()  # Save the form
            
            # Store the signupfinish_id in the session
            request.session['signupfinish_id'] = form.id
            print(f'SignupFinish ID stored in session: {request.session["signupfinish_id"]}')
            
            sent = True
            return redirect('/profile/')  # Redirect to profile after signup finish
    else:
        formobj = SignupfinishForm()

    return render(request, 'signup2.html', {'formobj': formobj, 'sent': sent})



def otp(request):
    print('hello')
    sent = False
    form = OtpverificationForm()
    if request.method == "POST":
        form = OtpverificationForm(data=request.POST)
        if request.POST.get('inputotp') == otpveri:
            print('welcom')
            return HttpResponseRedirect('/signupfinish/',{'sent':sent}) 
        else:
                # OTP is incorrect
                return render(request, 'otp.html', {'form': form, 'error': 'Invalid OTP'})
    else:
        print('bye')
        form = OtpverificationForm()
    return render(request, 'otp.html',{'form':form, 'sent':sent})

def feed(request):
    return render(request, 'feed.html',)
     

def post_view(request):
    if not request.user.is_authenticated:
        return redirect('/login/')
    company_page = Company.objects.filter(user=request.user).first()  # Get the user's company page, if any
    sent = False
    form = postform()
    

    if request.method == 'POST':
        post_type = request.POST.get('post_type')  # Get the post type from the form.
        form = postform(request.POST, request.FILES)
        
        if form.is_valid():
            post = form.save(commit=False)  # Save the form data without committing to the database.

            # Handle post creation based on post_type.
            if post_type == 'account':
                post.author = request.user  # Associate the post with the user's account.
                post.user = request.user    # Set the user field explicitly
                post.post_type = 'account'
                post.save()
                messages.success(request, "Post created under your account.")
            elif post_type == 'company' and company_page:
                post.author = request.user  # Record the user who created the post.
                post.user = request.user    # Set the user field explicitly
                post.company_page = company_page  # Associate the post with the user's company page.
                post.post_type = 'company'
                post.save()
                messages.success(request, f"Post created under your company page: {company_page.name}.")
            else:
                # Handle invalid post type or missing company page.
                messages.error(request, "Invalid post type or you don't have a company page.")
                return render(request, 'postlogin.html', {'form': form, 'sent': sent, 'company_page': company_page})

            # Redirect after successful post creation.
            return HttpResponseRedirect('/tagslug/')
    
    # Render the post creation form.
    return render(request, 'postlogin.html', {'form': form, 'sent': sent, 'company_page': company_page})

def post_list_view(request, tag_slug=None):
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        return redirect('/login/')  # Redirect to login if the user is not authenticated

    # Fetch SignupFinish for the current user
    signupfinish = SignupFinish.objects.filter(user=request.user).first()

    # If no signupfinish data is found, redirect to the signup finish page
    if not signupfinish:
        return redirect('/signupfinish/')
    
     # Get all posts with related user information
    posts = Post.objects.select_related('author').all()

    # Pass the posts to the template

    # Handle the tag-based filtering
    post_list = Post.objects.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])

    paginator = Paginator(post_list, 2)  # Pagination logic
    page_number = request.GET.get('page')
    try:
        post_list = paginator.page(page_number)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)

    return render(request, 'post_list.html', {'post_list': post_list, 'signupfinish': signupfinish,'posts': posts})


def post_detail_view(request,year,month,day,post):
    post=get_object_or_404(Post,slug = post,
                           status = 'published',
                           publish__year=year,
                           publish__month = month,
                           publish__day = day)
    post_tags_ids = post.tags.values_list('id',flat=True)
    similar_posts = Post.objects.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags'))
    comment = post.comments.filter(active=True)
    csubmit = False
    if request.method=='POST':
        form=CommentForm(data=request.POST)
        if form.is_valid():
            new_comment=form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            csubmit =True
    else:
        form = CommentForm()
    return render(request,'post_detail.html',{'post':post,'form':form,'comment':comment,'csubmit':csubmit,'similar_posts':similar_posts})

def post_list_view(request):
    post_list = Post.objects.all()
    return render(request,'post_list.html',{'post_list':post_list })


def profile(request):
    is_update = True
    # Ensure the user is logged in
    if not request.user.is_authenticated:
        return redirect('/login/')  # Redirect to login if the user is not authenticated

    # Fetch SignupFinish for the current user
    signupfinish = SignupFinish.objects.filter(user=request.user).first()

    # If no signupfinish data is found, redirect to the signup finish page
    if not signupfinish:
        return redirect('/signupfinish/')

    # Fetch the logged-in user and their latest resume
    user = request.user
    latest_resume = Resume.objects.filter(user=user).order_by('-created').first()

    # Fetch the latest objective for the headline form
    latest_objective = Resume_headline.objects.filter(user=user).all()

    keyskills = Keyskills.objects.filter(user=user).all()

    employment_data = Employment.objects.filter(user=request.user).all()

    company = Company.objects.filter(user=request.user).first()

    month_mapping = {
        "Jan": 1,
        "Feb": 2,
        "Mar": 3,
        "Apr": 4,
        "May": 5,
        "Jun": 6,
        "Jul": 7,
        "Aug": 8,
        "Sep": 9,
        "Oct": 10,
        "Nov": 11,
        "Dec": 12
    }

    for employment in employment_data:
        if employment.years_of_Joining and employment.months_of_Joining:
            try:
                # Convert string fields to integers
                joining_year = int(employment.years_of_Joining)
                joining_month_str = employment.months_of_Joining.strip()  # Remove any leading/trailing whitespace

                # Convert month name to integer
                joining_month = month_mapping.get(joining_month_str)
                
                if joining_month is not None:
                    # Create a datetime object for the joining date
                    joining_date = datetime(joining_year, joining_month, 1)
                    current_date = datetime.now()

                    # Calculate the difference in years and months
                    years_diff = current_date.year - joining_date.year
                    months_diff = current_date.month - joining_date.month

                    # Adjust the difference if the months are negative
                    if months_diff < 0:
                        years_diff -= 1
                        months_diff += 12

                    employment.total_years = years_diff
                    employment.total_months = months_diff
                else:
                    # Handle invalid month names
                    employment.total_years = 0
                    employment.total_months = 0
            except ValueError:
                # Handle invalid integer conversion
                employment.total_years = 0
                employment.total_months = 0
        else:
            employment.total_years = 0
            employment.total_months = 0


    education_data = Education.objects.filter(user=user).all()
    itskills_data = Itskills.objects.filter(user = user).all()
    project_data = Project.objects.filter(user=user).all()
    summary_data = Profile_summary.objects.filter(user=user).all()
    career_data = Career_profile.objects.filter(user = user).all()
    personal_data = Personal_details.objects.filter(user=user).all()
 

    # Initialize the forms
    form = Resumeform()  # For resume upload
    formobj = Resume_headlineform()  # For resume headline
    keyskillform = Keyskills_form()
    emplomentform  = Employmentform()
    educationform = Educationform()
    itskillsform = Itskillsform()
    projectform = Projectform()
    summaryform = Profile_summaryform()
    careerform = career_profileform()
    personalform = Personal_detailsform()

    # Initialize sent flag for resume headline form
    sent = False
    keyskills_handling = None
    keyform = None
    employment = None
    education_handle = None
    pk = None

    # Process form submissions
    if request.method == "POST":
        if 'resume_submit' in request.POST:  # Check if resume form is submitted
            form = Resumeform(request.POST, request.FILES)
            if 'resume' not in request.FILES:  # Check if a file is uploaded
                form.add_error('resume', 'Please select a file before submitting.')
            pk = request.POST.get('pk')
            if pk:
                resume = Resume.objects.get(pk=pk, user=user)
                resume.delete()  # Delete the project
                return redirect('/profile/')
            elif form.is_valid():
                resume_instance = form.save(commit=False)
                resume_instance.user = request.user
                resume_instance.save()
                return redirect('/profile/')  # Redirect to avoid re-posting on refresh

        elif 'headline_submit' in request.POST:  # Check if headline form is submitted
            pk = request.POST.get('pk')
            if pk:  # If pk exists, update the existing headline
                headline = Resume_headline.objects.get(pk=pk, user=user)
                formobj = Resume_headlineform(request.POST, instance=headline)
            elif pk:
                headline = Resume_headline.objects.get(pk=pk, user=user)
                headline.delete()  # Delete the project
                return redirect('/profile/')
            else:  # Otherwise create a new headline
                formobj = Resume_headlineform(request.POST)

            if formobj.is_valid():
                resume_headline = formobj.cleaned_data['objective']
                if pk:  # Update the existing headline
                    formobj.save()
                else:  # Create a new headline
                    Resume_headline.objects.create(
                        objective=resume_headline,
                        user=request.user
                    )
                sent = True
                return redirect('/profile/')

        elif 'keyskills_submit' in request.POST:  # Check if keyskills form is submitted
            pk = request.POST.get('pk')
            if pk:
                keyform = Keyskills.objects.get(pk=pk, user=user)
                keyform.delete()  # Delete the project
                return redirect('/profile/')
            else:
                keyskillform = Keyskills_form(request.POST)
            if keyskillform.is_valid():
                keyskills_handling = keyskillform.cleaned_data['keyskills']
                keyform = Keyskills.objects.create(
                    keyskills=keyskills_handling,
                    user=request.user
                )
                return redirect('/profile/')
            
        elif 'Employment_submit' in request.POST:  # Check if Employment form is submitted
            pk = request.POST.get('pk')  # Fetch the primary key for Employment record
            if pk:  # If pk exists, update the existing employment record
                employment_handle = Employment.objects.get(pk=pk, user=user)
                emplomentform = Employmentform(request.POST, instance=employment_handle)

            elif pk:
                employment = Employment.objects.get(pk=pk, user=user)
                employment.delete()  # Delete the project
                return redirect('/profile/')

            else:  # Otherwise create a new headline
                emplomentform = Employmentform(request.POST)


            if emplomentform.is_valid():
                print('hello2')
                current_employment = emplomentform.cleaned_data['current_employment']  # current employment field
                employment_type = emplomentform.cleaned_data['employment_type']        # employment type field
                years_of_experience = emplomentform.cleaned_data['years_of_experience'] # Get years from the form
                months_of_experience = emplomentform.cleaned_data['months_of_experience']  # Get months from the form
                current_company = emplomentform.cleaned_data['current_company']
                current_job = emplomentform.cleaned_data['current_job']
                years_of_Joining = int(emplomentform.cleaned_data['years_of_Joining'])
                months_of_Joining = emplomentform.cleaned_data['months_of_Joining']
                Current_salary = emplomentform.cleaned_data['Current_salary']
                skill_used = emplomentform.cleaned_data['skill_used']
                Job_prfile = emplomentform.cleaned_data['Job_prfile']
                Notice_period = emplomentform.cleaned_data['Notice_period']
                print('hello3')
                if pk:  # Update the existing headline
                    emplomentform.save()
                else:
                    employment = Employment.objects.create(
                        current_employment=current_employment,
                        employment_type=employment_type,
                        years_of_experience=years_of_experience, 
                        months_of_experience=months_of_experience,
                        current_company = current_company,
                        current_job = current_job,
                        years_of_Joining = years_of_Joining,
                        months_of_Joining = months_of_Joining,
                        Current_salary = Current_salary,
                        skill_used = skill_used,
                        Job_prfile = Job_prfile,
                        Notice_period = Notice_period,
                        user=request.user
                    )
                    print('hello4')
                return redirect('/profile/')
            

        elif 'Education_submit' in request.POST:
            pk = request.POST.get('pk')  # Fetch the primary key for Employment record
            if pk:  # If pk exists, update the existing employment record
                education_handle = Education.objects.get(pk=pk, user=user)
                educationform = Educationform(request.POST, instance=education_handle)

            elif pk:
                education = Education.objects.get(pk=pk, user=user)
                education.delete()  # Delete the project
                return redirect('/profile/')

            else:  # Otherwise create a new headline
                educationform = Educationform(request.POST)


            if educationform.is_valid():
                print('hello2')
                select_education = educationform.cleaned_data['select_education']  # current employment field
                university = educationform.cleaned_data['university']        # employment type field
                course = educationform.cleaned_data['course'] # Get years from the form
                specialixation = educationform.cleaned_data['specialixation']  # Get months from the form
                course_type = educationform.cleaned_data['course_type']
                startingyear_of_course = educationform.cleaned_data['startingyear_of_course']
                endingyear_of_course = educationform.cleaned_data['endingyear_of_course']
                grading_system = educationform.cleaned_data['grading_system']
                print('hello3')
                if pk:  # Update the existing headline
                    educationform.save()
                else:
                    education = Education.objects.create(
                        select_education=select_education,
                        university=university,
                        course=course, 
                        specialixation=specialixation,
                        course_type = course_type,
                        startingyear_of_course = startingyear_of_course,
                        endingyear_of_course = endingyear_of_course,
                        grading_system = grading_system,
                        user=request.user
                    )
                    print('hello4')
                return redirect('/profile/')
            

        elif 'Itskills_submit' in request.POST:
            pk = request.POST.get('pk')  # Fetch the primary key for Employment record
            if pk:  # If pk exists, update the existing employment record
                itskills_handle = Itskills.objects.get(pk=pk, user=user)
                itskillsform = Itskillsform(request.POST, instance=itskills_handle)

            else:  # Otherwise create a new headline
                itskillsform = Itskillsform(request.POST)


            if itskillsform.is_valid():
                print('hello2')
                skill_software_name = itskillsform.cleaned_data['skill_software_name']  # current employment field
                software_version = itskillsform.cleaned_data['software_version']        # employment type field
                last_used = itskillsform.cleaned_data['last_used'] # Get years from the form
                years_of_experiences = itskillsform.cleaned_data['years_of_experiences']  # Get months from the form
                months_of_experiences = itskillsform.cleaned_data['months_of_experiences']
                print('hello3')
                if pk:  # Update the existing headline
                    itskillsform.save()
                else:
                    itskills = Itskills.objects.create(
                        skill_software_name=skill_software_name,
                        software_version=software_version,
                        last_used=last_used, 
                        years_of_experiences=years_of_experiences,
                        months_of_experiences = months_of_experiences,
                        user=request.user
                    )
                    print('hello4')
                return redirect('/profile/')
            
            
        elif 'Project_submit' in request.POST:
            pk = request.POST.get('pk')  # Fetch the primary key for Employment record
            print(pk) 
            if pk:  # If pk exists, update the existing employment record
                project_handle = Project.objects.get(pk=pk, user=user)
                projectform = Projectform(request.POST, instance=project_handle)
            elif pk:
                project = Project.objects.get(pk=pk, user=user)
                project.delete()  # Delete the project
                return redirect('/profile/')

            else:  # Otherwise create a new headline
                projectform = Projectform(request.POST)


            if projectform.is_valid():
                print('hello2')
                project_title = projectform.cleaned_data['project_title']  # current employment field
                client = projectform.cleaned_data['client']        # employment type field
                project_type = projectform.cleaned_data['project_type'] # Get years from the form
                year_of_working = projectform.cleaned_data['year_of_working']  # Get months from the form
                month_of_working = projectform.cleaned_data['month_of_working']
                details_of_project = projectform.cleaned_data['details_of_project']
                project_location = projectform.cleaned_data['project_location']
                project_site_choices = projectform.cleaned_data['project_site_choices']
                employment_type_project = projectform.cleaned_data['employment_type_project'] # Get years from the form
                team_size = projectform.cleaned_data['team_size']  # Get months from the form
                role = projectform.cleaned_data['role']
                role_decription = projectform.cleaned_data['role_decription']
                skill_used = projectform.cleaned_data['skill_used']
                print('hello3')
                if pk:  # Update the existing headline
                    projectform.save()
                else:
                    project = Project.objects.create(
                        project_title=project_title,
                        client=client,
                        project_type=project_type, 
                        year_of_working=year_of_working,
                        month_of_working = month_of_working,
                        details_of_project = details_of_project,
                        project_location = project_location,
                        project_site_choices = project_site_choices,
                        employment_type_project=employment_type_project,
                        team_size = team_size,
                        role = role,
                        role_decription = role_decription,
                        skill_used = skill_used,
                        user=request.user
                    )
                    print('hello4')
                return redirect('/profile/')
        
        elif 'Profile_summary_submit' in request.POST:  # Check if resume form is submitted
            pk = request.POST.get('pk')  # Fetch the primary key for Employment record
            print(pk) 
            if pk:  # If pk exists, update the existing employment record
                summary_handle = Profile_summary.objects.get(pk=pk, user=user)
                summaryform = Profile_summaryform(request.POST, instance=summary_handle)
            elif pk:
                summary = Profile_summary.objects.get(pk=pk, user=user)
                summary.delete()  # Delete the project
                return redirect('/profile/')

            else:  # Otherwise create a new headline
                summaryform = Profile_summaryform(request.POST)
            if summaryform.is_valid():
                print('hello2')
                summary = summaryform.cleaned_data['summary']  # current employment field
                print('hello3')
                if pk:  # Update the existing headline
                    summaryform.save()
                
                else:
                    summary = Profile_summary.objects.create(
                        summary=summary,
                        user=request.user
                    )
                    print('hello4')
                return redirect('/profile/')
            
        elif 'Career_Profile_submit' in request.POST:
            pk = request.POST.get('pk')  # Fetch the primary key for Employment record
            print(pk) 
            if pk:  # If pk exists, update the existing employment record
                career_handle = Career_profile.objects.get(pk=pk, user=user)
                careerform = career_profileform(request.POST, instance=career_handle)
            elif pk:
                career = Career_profile.objects.get(pk=pk, user=user)
                career.delete()  # Delete the project
                return redirect('/profile/')

            else:  # Otherwise create a new headline
                careerform = career_profileform(request.POST)

            if careerform.is_valid():
                print('hello2')
                Current_industry = careerform.cleaned_data['Current_industry']  # current employment field
                Department = careerform.cleaned_data['Department']        # employment type field
                Role_category = careerform.cleaned_data['Role_category'] # Get years from the form
                Job_role = careerform.cleaned_data['Job_role']  # Get months from the form
                job_type_project = careerform.cleaned_data['job_type_project']
                employment_type_career = careerform.cleaned_data['employment_type_career']
                shift_type_project = careerform.cleaned_data['shift_type_project']
                chipsVal = careerform.cleaned_data['chipsVal']
                
                try:
                    selected_locations = json.loads(chipsVal)  # Try parsing chipsVal
                except json.JSONDecodeError:
                    # Handle the error if chipsVal is not a valid JSON string
                    selected_locations = []  # Default to an empty list or handle as needed
                
                salary = careerform.cleaned_data['salary']  # Get salary from the form

                print('hello3')
                if pk:  # Update the existing headline
                    careerform.save()
                else:
                    career = Career_profile.objects.create(
                        Current_industry=Current_industry,
                        Department=Department,
                        Role_category=Role_category, 
                        Job_role=Job_role,
                        job_type_project=job_type_project,
                        employment_type_career=employment_type_career,
                        shift_type_project=shift_type_project,
                        location=chipsVal,  # Save chipsVal or selected_locations as needed
                        salary=salary,
                        user=request.user
                    )
                    print('hello4')
                return redirect('/profile/')
            
        elif 'Personal_details_submit' in request.POST:
            pk = request.POST.get('pk')  # Fetch the primary key for Employment record
            print(pk) 
            if pk:  # If pk exists, update the existing employment record
                Personal_details_handle = Personal_details.objects.get(pk=pk, user=user)
                personalform = Personal_detailsform(request.POST, instance=Personal_details_handle)
            elif pk:
                details = Personal_details.objects.get(pk=pk, user=user)
                details.delete()  # Delete the project
                return redirect('/profile/')

            else:  # Otherwise create a new headline
                personalform = Personal_detailsform(request.POST)


            if personalform.is_valid():
                print('hello2')
                gender_type_project = personalform.cleaned_data['gender_type_project']  # current employment field
                Marital_type_project = personalform.cleaned_data['Marital_type_project']        # employment type field
                date = personalform.cleaned_data['date'] # Get years from the form
                month = personalform.cleaned_data['month']  # Get months from the form
                year = personalform.cleaned_data['year']
                differently_abled_type_career = personalform.cleaned_data['differently_abled_type_career']
                career_break_type_career = personalform.cleaned_data['career_break_type_career']
                permanent_address = personalform.cleaned_data['permanent_address']
                hometown = personalform.cleaned_data['hometown'] # Get years from the form
                pincode = personalform.cleaned_data['pincode']  # Get months from the form
                print('hello3')
                if pk:  # Update the existing headline
                    personalform.save()
                else:
                    details = Personal_details.objects.create(
                        gender_type_project=gender_type_project,
                        Marital_type_project=Marital_type_project,
                        date=date, 
                        month=month,
                        year = year,
                        differently_abled_type_career = differently_abled_type_career,
                        career_break_type_career = career_break_type_career,
                        permanent_address = permanent_address,
                        hometown=hometown,
                        pincode = pincode,
                        user=request.user
                    )
                    print('hello4')
                return redirect('/profile/')
            

    else:
        # Initialize forms for GET request
        form = Resumeform()
        formobj = Resume_headlineform()
        keyskillform = Keyskills_form()
        emplomentform  = Employmentform()
        educationform = Educationform()
        itskillsform = Itskillsform()
        projectform = Projectform()
        summaryform = Profile_summaryform()
        personalform = Personal_detailsform()

        print('bye')

    # Render the profile template with the context data
    return render(request, 'profile.html', {
        'signupfinish': signupfinish,
        'form': form,
        'latest_resume': latest_resume,
        'user': user,
        'sent': sent,
        'latest_objective': latest_objective,
        'formobj': formobj,
        'is_update': is_update,
        'keyskills':keyskills,
        'keyskillform':keyskillform,
        'keyskills_handling':keyskills_handling,
        'keyform':keyform,
        'emplomentform': emplomentform ,
        'employment':employment,
        'employment_data': employment_data,
        'educationform': educationform,
        'education_data':education_data,
        'education_handle':education_handle,
        'itskillsform':itskillsform,
        'itskills_data':itskills_data,
        'projectform':projectform,
        'project_data':project_data,
        'summaryform':summaryform,
        'summary_data':summary_data,
        'careerform':careerform,
        'career_data':career_data,
        'personalform':personalform,
        'personal_data':personal_data,
        'company': company,
    })





def list_headlines(request):
    if not request.user.is_authenticated:
        return redirect('/login/')
    user = request.user
    headlines = Resume_headline.objects.filter(user=user).all()  # Retrieve all ResumeHeadline objects
    return render(request, 'resume_headline_list.html', {'headlines': headlines})

def update_headline(request, pk):
    is_update = True
    # Ensure the user is logged in
    if not request.user.is_authenticated:
        return redirect('/login/')

    # Fetch SignupFinish for the current user
    signupfinish = SignupFinish.objects.filter(user=request.user).first()

    # If no signupfinish data is found, redirect to the signup finish page
    if not signupfinish:
        return redirect('/signupfinish/')

    # Fetch the logged-in user and their latest resume
    user = request.user
    latest_resume = Resume.objects.filter(user=user).order_by('-created').first()

    # Fetch the headline object to update
    headline = Resume_headline.objects.get(pk=pk, user=user)  # Ensure the headline belongs to the current user

    # Fetch all objectives for the user
    latest_objective = Resume_headline.objects.filter(user=user).all()

    # Fetch employment data for the user
    employment_data = Employment.objects.get(pk=pk, user=user)

    # Handle form submission for updating headline
    if request.method == 'POST':
        if 'headline_submit' in request.POST:  # Handle headline update
            formobj = Resume_headlineform(request.POST, instance=headline)
            if formobj.is_valid():
                formobj.save()
                return redirect('/profile/')  # Redirect back to profile after updating

        elif 'employment_submit' in request.POST:  # Handle employment update # Get the employment record to update
            employment_instance = Employment.objects.get(pk=pk, user=user)
            emplomentform = Employmentform(request.POST, instance=employment_instance)

            if emplomentform.is_valid():
                emplomentform.save()
                return redirect('/profile/')
            
        elif 'Education_submit' in request.POST:  # Handle employment update # Get the employment record to update
            education_instance = Education.objects.get(pk=pk, user=user)
            educationform = Educationform(request.POST, instance=education_instance)

            if educationform.is_valid():
                educationform.save()
                return redirect('/profile/')
            
        elif 'Itskills_submit' in request.POST:  # Handle employment update # Get the employment record to update
            itskills_handle = Itskills.objects.get(pk=pk, user=user)
            itskillsform = Itskillsform(request.POST, instance=itskills_handle)

            if itskillsform.is_valid():
                itskillsform.save()
                return redirect('/profile/')
            
        elif 'Project_submit' in request.POST:  # Handle employment update # Get the employment record to update
            project_handle = Project.objects.get(pk=pk, user=user)
            projectform = Projectform(request.POST, instance=project_handle)

            if projectform.is_valid():
                projectform.save()
                return redirect('/profile/')

    else:
        # Pre-fill forms for GET request
        formobj = Resume_headlineform(instance=headline)  # Pre-fill headline form
        emplomentform = Employmentform()  # Initialize an empty employment form
        educationform = Educationform()
        itskillsform = Itskillsform()
        projectform = Projectform()

    # Render the profile page with necessary context
    return render(request, 'profile.html', {
        'signupfinish': signupfinish,
        'form': Resumeform(),  # Empty resume form
        'latest_resume': latest_resume,
        'user': user,
        'objective': Resume_headlineform(),  # Empty form for new headlines
        'latest_objective': latest_objective,
        'formobj': formobj,  # Form for editing the specific headline
        'sent': False,  # Ensure the sent flag is set to False
        'is_update': is_update,
        'emplomentform': emplomentform,
        'employment': None,  # None because you are editing one employment record at a time
        'employment_data': employment_data,  # List of all employment records for the user
        'educationform': educationform,
        'itskillsform':itskillsform,
        'projectform':projectform,
    })

def delete_headline(request, pk):
    headline = Resume_headline.objects.get(pk=pk)
    if request.method == 'POST':
        headline.delete()
        return redirect('/profile/')
    return render(request, 'resume_headline_confirm_delete.html', {'headline': headline,})

def delect_skill(request,pk):
    skill = Keyskills.objects.get(pk=pk)
    if request.method == 'POST':
        skill.delete()
        return redirect('/profile/')
    return render(request, 'resume_headline_confirm_delete.html', { 'skill':skill})

def delete_employee(request,pk):
    employee = Employment.objects.get(pk=pk)
    if request.method == 'POST':
        employee.delete()
        return redirect('/profile/')
    return render(request, 'resume_headline_confirm_delete.html', { 'employee':employee})

def delete_education(request,pk):
    education = Education.objects.get(pk=pk)
    if request.method == 'POST':
        education.delete()
        return redirect('/profile/')
    return render(request, 'resume_headline_confirm_delete.html',{ 'education':education})

def delete_itskills(request,pk):
    itskills = Itskills.objects.get(pk=pk)
    if request.method == 'POST':
        itskills.delete()
        return redirect('/profile/')
    return render(request, 'resume_headline_confirm_delete.html',{ 'itskills':itskills})

def delete_project(request,pk):
    project = Project.objects.get(pk=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('/profile/')
    return render(request, 'resume_headline_confirm_delete.html',{ 'project':project})


def delete_profile(request,pk):
    profile = Profile_summary.objects.get(pk=pk)
    if request.method == 'POST':
        profile.delete()
        return redirect('/profile/')
    return render(request, 'resume_headline_confirm_delete.html',{ 'profile':profile})

def delete_career(request,pk):
    career = Career_profile.objects.get(pk=pk)
    if request.method == 'POST':
        career.delete()
        return redirect('/profile/')
    return render(request, 'resume_headline_confirm_delete.html',{ 'career':career})


def delete_personal(request,pk):
    personal = Personal_details.objects.get(pk=pk)
    if request.method == 'POST':
        personal.delete()
        return redirect('/profile/')
    return render(request, 'resume_headline_confirm_delete.html',{ 'personal':personal})


def delete_resume(request,pk):
    user = request.user
    resume = Resume.objects.filter(user=user).order_by('-created').all()
    if request.method == 'POST':
        resume.delete()
        return redirect('/profile/')
    return render(request, 'resume_headline_confirm_delete.html',{ 'resume':resume})









def jobs(request):
    jobs = JobPosting.objects.all()
    return render(request, 'jobs.html',{'jobs':jobs})

def logoutview(request):
    request.session.clear()
    return render(request, 'signup.html')

def user_profile(request, username):
    # Fetch the user whose profile is being viewed (based on the URL)
    profile_user = get_object_or_404(User, username=username)
    

    # Ensure the user is logged in
    if not request.user.is_authenticated:
        return redirect('/login/')  # Redirect to login if the user is not authenticated

    # Fetch SignupFinish for the profile_user, not necessarily the logged-in user
    signupfinish = SignupFinish.objects.filter(user=profile_user).first()

    # If no signupfinish data is found for the profile_user, redirect to signup finish page
    if not signupfinish and request.user == profile_user:
        return redirect('/signupfinish/')

    # Fetch the latest resume and other data for the profile_user (the user being viewed)
    latest_resume = Resume.objects.filter(user=profile_user).order_by('-created').first()
    latest_objective = Resume_headline.objects.filter(user=profile_user).all()
    keyskills = Keyskills.objects.filter(user=profile_user).all()
    employment_data = Employment.objects.filter(user=profile_user).all()

    # Calculate years/months of experience for the profile_user
    month_mapping = {
        "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
        "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12
    }

    for employment in employment_data:
        if employment.years_of_Joining and employment.months_of_Joining:
            try:
                joining_year = int(employment.years_of_Joining)
                joining_month_str = employment.months_of_Joining.strip()
                joining_month = month_mapping.get(joining_month_str)

                if joining_month is not None:
                    joining_date = datetime(joining_year, joining_month, 1)
                    current_date = datetime.now()

                    years_diff = current_date.year - joining_date.year
                    months_diff = current_date.month - joining_date.month

                    if months_diff < 0:
                        years_diff -= 1
                        months_diff += 12

                    employment.total_years = years_diff
                    employment.total_months = months_diff
                else:
                    employment.total_years = 0
                    employment.total_months = 0
            except ValueError:
                employment.total_years = 0
                employment.total_months = 0
        else:
            employment.total_years = 0
            employment.total_months = 0

    # Fetch other profile-related data for the profile_user
    education_data = Education.objects.filter(user=profile_user).all()
    itskills_data = Itskills.objects.filter(user=profile_user).all()
    project_data = Project.objects.filter(user=profile_user).all()
    summary_data = Profile_summary.objects.filter(user=profile_user).all()
    career_data = Career_profile.objects.filter(user=profile_user).all()
    personal_data = Personal_details.objects.filter(user=profile_user).all()

    # Pass all the necessary data to the template
    return render(request, 'dynamicprofile.html', {
        'signupfinish': signupfinish,
        'latest_resume': latest_resume,
        'user': request.user,  # Logged-in user
        'profile_user': profile_user,  # Profile being viewed (may be different from the logged-in user)
        'latest_objective': latest_objective,
        'keyskills': keyskills,
        'employment_data': employment_data,
        'education_data': education_data,
        'itskills_data': itskills_data,
        'project_data': project_data,
        'summary_data': summary_data,
        'career_data': career_data,
        'personal_data': personal_data,
    })

def follow_user(request, user_id):
    if request.method == 'POST':
        profile_user = get_object_or_404(User, id=user_id)

        # Check if the current user is already following the profile user
        follow, created = Follow.objects.get_or_create(follower=request.user, followed=profile_user)

        if created:
            # New follow request sent
            follow.status = 'requested'
            follow.save()
            return JsonResponse({'status': 'requested'})
        
        elif follow.status == 'requested':
            # Accept the follow request
            follow.status = 'accepted'
            follow.save()
            return JsonResponse({'status': 'accepted'})
        
        elif follow.status == 'accepted':
            # User is already following, unfollow
            follow.delete()
            return JsonResponse({'status': 'unfollowed'})

        return JsonResponse({'status': 'error'})

    return JsonResponse({'status': 'invalid'})


def notifications(request):
    user_notifications = request.user.notifications.all()
    print(user_notifications)

    # Pass notifications to the template
    context = {
        'user_notifications': user_notifications
    }

    # Render the HTML template and pass the notifications
    return render(request, 'notifications.html', context)

def feedforemployer(request):
    return render(request, 'feedforemployer.html')

@login_required
def dynamicemployer(request):
    return render(request, 'dynamicempolyerform.html')


# views.py
def registrationform(request):
    if request.method == 'POST':
        form = CombinedJobForm(request.POST)
        if form.is_valid():
            job_title = form.cleaned_data['job_title']
            company_name = form.cleaned_data['company_name']
            workplace = form.cleaned_data['workplace']
            job_location = form.cleaned_data['job_location']
            job_type = form.cleaned_data['job_type']
            description = form.cleaned_data['description']
            skills = form.cleaned_data['skills']
            identify_source = form.cleaned_data['identify_source']
            additional_info = form.cleaned_data['additional_info']

             # Validate URL if the user selects 'website'
            if request.POST.get('select_field') == 'website':
                validator = URLValidator()
                try:
                    validator(additional_info)
                except ValidationError:
                    return render(request, 'collect_applicant_info.html', {
                        'job': job,
                        'error': 'Invalid website URL.'
                    })

            # Create a JobPosting instance
            job = JobPosting.objects.create(
                job_title=job_title,
                company_name=company_name,
                workplace=workplace,
                job_location=job_location,
                job_type=job_type,
                description=description,
                skills=skills,
                identify_source=identify_source,
                additional_info=additional_info,
                user=request.user
            )

              # Process qualifications
            qualification_ids = request.POST.getlist('qualifications')  # Get selected qualifications
            for qualification_id in qualification_ids:
                qualification = get_object_or_404(Qualification, id=qualification_id)
                must_have = request.POST.get(f'must_have_{qualification_id}') == 'on'
                
                # Create JobQualification
                JobQualification.objects.create(
                    job=job,
                    qualification=qualification,
                    must_have=must_have
                )

            return redirect(reverse('job_detail', args=[job.id]))
            
    else:
        form = CombinedJobForm()
        qualifications = Qualification.objects.filter(user=request.user)  # Fetch all qualifications

    return render(request, 'client-registration-form.html', {'form': form, 'qualifications': qualifications,})


def apply_for_job(request, job_id):
    job = get_object_or_404(JobPosting, id=job_id)
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, job=job)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.save()
            # Save applicant's answers
            for field, answer_text in form.cleaned_data.items():
                if field.startswith('qualification_'):
                    question_id = field.split('_')[1]
                    Answer.objects.create(
                        question_id=question_id,
                        answer_text=answer_text,
                        job_application=application
                    )
            return redirect('application_success')
    else:
        form = JobApplicationForm(job=job)
    return render(request, 'apply_for_job.html', {'form': form, 'job': job})

def comfirmjobsetting(request):
    
    return render(request, 'confirmjobsetting.html')


def job_detail(request, job_id):
    job = get_object_or_404(JobPosting, id=job_id)
    must_have_qualifications = JobQualification.objects.filter(job=job, must_have=True)

    # Check if the user has already applied for this job
    if request.user.is_authenticated:
        existing_application = JobApplication.objects.filter(job=job, user=request.user).exists()
        if existing_application:
            messages.error(request, "You have already applied for this job.")
            return render(request, 'job_detail.html', {
                'job': job,
                'form': None,
                'already_applied': True
            })
    else:
        messages.error(request, "You need to log in to apply for jobs.")
        return redirect('login')  # Replace 'login' with your login URL name.

    if request.method == 'POST':
        # Collect applicant's information
        applicant_name = request.POST.get('applicant_name')
        applicant_email = request.POST.get('applicant_email')
        resume = request.FILES.get('applicant_resume')

        # Validate and collect answers
        validation_errors = []

        # Create a list to store saved answers
        saved_answers = []

        for mq in must_have_qualifications:
            question_id = mq.qualification.id
            applicant_answer = request.POST.get(f'answer_{question_id}')
            ideal_answer = mq.qualification.ideal_answer

            # Validate the applicant's answer
            if not applicant_answer:
                validation_errors.append(f"Answer to '{mq.qualification.question_text}' is required.")
            elif applicant_answer.lower() != ideal_answer.lower():
                validation_errors.append(f"Your answer to '{mq.qualification.question_text}' does not match the ideal answer.")

            # Save valid answers to the database
            if applicant_answer:
                answer = Answer.objects.create(
                    question=mq.qualification,
                    answer_text=applicant_answer
                )
                saved_answers.append(answer)

        # If validation errors exist, re-render the form with error messages
        if validation_errors:
            return render(request, 'job_detail.html', {
                'job': job,
                'must_have_qualifications': must_have_qualifications,
                'validation_errors': validation_errors,
            })

        # Save the job application
        job_application = JobApplication.objects.create(
            job=job,
            applicant_name=applicant_name,
            applicant_email=applicant_email,
            applicant_resume=resume,
            user=request.user
        )

        # Associate saved answers with the job application
        job_application.answers.set(saved_answers)
        job_application.save()

        messages.success(request, "Your application has been submitted successfully!")
        return redirect('application_success')  # Replace with your success page URL name.

    else:
        # Instantiate the application form dynamically
        form = JobApplicationForm()

    # Render the job detail page with the application form
    return render(request, 'job_detail.html', {
        'job': job,
        'form': form,
        'must_have_qualifications': must_have_qualifications
    })
def application_success(request):
    return render(request, 'application_success.html')

def jobshomepage(request,job_id):
    jobs = JobPosting.objects.all()
    job = get_object_or_404(JobPosting, id=job_id)
     # Fetch SignupFinish for the profile_user, not necessarily the logged-in user
    profile_user = get_object_or_404(User, id=job.user.id)
    signupfinish = SignupFinish.objects.filter(user=profile_user).first()
    user_applied = JobApplication.objects.filter(job=job, user=request.user).exists()
    return render(request, 'jobshomepage.html', {
        'jobs':jobs,
        'job':job,
        'signupfinish': signupfinish,
        'profile_user': profile_user,
        'user': request.user,
        'user_applied': user_applied,  # Pass the applied status to the template
                                                 })


def job_posting_detail(request, job_id, username):
    # Ensure the user is logged in
    if not request.user.is_authenticated:
        return redirect('/login/')

    # Fetch the profile user whose details are being viewed
    profile_user = get_object_or_404(User, username=username)

    # Fetch the specific job posting and all applications for it
    job_posting = get_object_or_404(JobPosting, id=job_id,)
    # Filter job applications
    applications = JobApplication.objects.filter(job=job_posting, user=profile_user)

    # Fetch employment data for the profile_user
    employment_data = Employment.objects.filter(user=profile_user)

    # Gather SignupFinish details for each application
    application_details = []
    for application in applications:
        signupfinish = SignupFinish.objects.filter(user=application.user).first()
        application_details.append({
            'user': application.user,
            'signupfinish': signupfinish,
            'resume': application.applicant_resume,
        })

    # Redirect to signup finish page if there is no signupfinish for the profile user
    signupfinish = SignupFinish.objects.filter(user=profile_user).first()
    if not signupfinish and request.user == profile_user:
        return redirect('/signupfinish/')

    # Calculate years/months of experience for each employment entry
    month_mapping = {
        "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
        "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12
    }
    for employment in employment_data:
        if employment.years_of_Joining and employment.months_of_Joining:
            try:
                joining_year = int(employment.years_of_Joining)
                joining_month_str = employment.months_of_Joining.strip()
                joining_month = month_mapping.get(joining_month_str)

                if joining_month is not None:
                    joining_date = datetime(joining_year, joining_month, 1)
                    current_date = datetime.now()
                    years_diff = current_date.year - joining_date.year
                    months_diff = current_date.month - joining_date.month

                    if months_diff < 0:
                        years_diff -= 1
                        months_diff += 12

                    employment.total_years = years_diff
                    employment.total_months = months_diff
                else:
                    employment.total_years = 0
                    employment.total_months = 0
            except ValueError:
                employment.total_years = 0
                employment.total_months = 0
        else:
            employment.total_years = 0
            employment.total_months = 0

    context = {
        'user': request.user,
        'job_posting': job_posting,
        'employment_data': employment_data,
        'applications': applications,
        'signupfinish': signupfinish,
        'application_details': application_details,
    }
    return render(request, 'job_posting_detail.html', context)


def my_posted_jobs(request):
    # Filter jobs by the logged-in user
    posted_jobs = JobPosting.objects.filter(user=request.user)
    applications = JobApplication.objects.filter(applicant_email=request.user.email)

    # Pass the jobs to the template
    context = {
        'posted_jobs': posted_jobs,
         'applications': applications,
    }
    return render(request, 'myitems.html', context)


def myappliedjobs(request):
    applications = JobApplication.objects.filter(applicant_email=request.user.email)

    context = {
       
         'applications': applications,
    }
    return render(request, 'appliedjobs.html', context)

def jobpostingdetail(request,job_id):
    
    # Retrieve the specific job posting
    job_posting = get_object_or_404(JobPosting, id=job_id)
    
    # Get all applications related to this job posting
    applications = JobApplication.objects.filter(job=job_posting)


    # Pass the job and applications to the template
    context = {
        'job_posting': job_posting,
        'applications': applications,
    }
    return render(request, 'hiring-jobs-details.html', context)


def posteduser(request, username):
    # Fetch the user whose profile is being viewed (based on the URL)
    profile_user = get_object_or_404(User, username=username)
    

    # Ensure the user is logged in
    if not request.user.is_authenticated:
        return redirect('/login/')  # Redirect to login if the user is not authenticated

    # Fetch SignupFinish for the profile_user, not necessarily the logged-in user
    signupfinish = SignupFinish.objects.filter(user=profile_user).first()

    # If no signupfinish data is found for the profile_user, redirect to signup finish page
    if not signupfinish and request.user == profile_user:
        return redirect('/signupfinish/')
    
    employment_data = Employment.objects.filter(user=profile_user).all()
    
    month_mapping = {
        "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
        "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12
    }

    for employment in employment_data:
        if employment.years_of_Joining and employment.months_of_Joining:
            try:
                joining_year = int(employment.years_of_Joining)
                joining_month_str = employment.months_of_Joining.strip()
                joining_month = month_mapping.get(joining_month_str)

                if joining_month is not None:
                    joining_date = datetime(joining_year, joining_month, 1)
                    current_date = datetime.now()

                    years_diff = current_date.year - joining_date.year
                    months_diff = current_date.month - joining_date.month

                    if months_diff < 0:
                        years_diff -= 1
                        months_diff += 12

                    employment.total_years = years_diff
                    employment.total_months = months_diff
                else:
                    employment.total_years = 0
                    employment.total_months = 0
            except ValueError:
                employment.total_years = 0
                employment.total_months = 0
        else:
            employment.total_years = 0
            employment.total_months = 0

             # Add applicant details for each application
    # application_details = []
    # for application in applications:
    #     applicant = application.user  # Get the user who applied
    #     application_details.append({
    #         'username': applicant.username,
    #         'email': applicant.email,
    #         'resume': application.resume,  # Assuming you have a `resume` field in JobApplication model
    #         'application_date': application.date_applied,  # Example field for application date
    #         'status': application.status  # Example field for application status
    #     })

    return render(request, 'dynamicprofile.html', {
        'signupfinish': signupfinish,
        'user': request.user,  # Logged-in user
        'profile_user': profile_user,  # Profile being viewed (may be different from the logged-in user)
        'employment_data': employment_data,
    })

def alljobapplicants(request,job_id):
    # Retrieve the specific job posting
    job_posting = get_object_or_404(JobPosting, id=job_id)
    
    # Get all applications related to this job posting
    applications = JobApplication.objects.filter(job=job_posting)


    # Pass the job and applications to the template
    context = {
        'job_posting': job_posting,
        'applications': applications,
    }
    return render(request, 'job_posting_detail_1.html', context)


def create_dynamic_questions(request):
    if request.method == 'POST':
        form = DynamicQuestionForm(request.POST)
        if form.is_valid():
            # Ensure that the user is set to the logged-in user
            dynamic_question = form.save(commit=False)  # Do not save yet
            dynamic_question.user = request.user  # Set the user to the logged-in user
            dynamic_question.save()  # Now save the instance
            return redirect('create_dynamic_questions')  # Redirect after saving
    else:
        form = DynamicQuestionForm()

    # Fetch existing questions to display below the form (optional)
    questions = Qualification.objects.all()

    return render(request, 'dynamic_questions_form.html', {'form': form, 'questions': questions})


def createcompany(request):
    return render(request, 'createcompany.html')

# def Companyadd(request):
#     return render(request, 'Companyaddform.html')


def Companyadd(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES)
        if form.is_valid():
            company_data = form.save(commit=False)
            company_data.user = request.user
            company_data.save()
            messages.success(request, "Company details submitted successfully!")
            return redirect(f"/{company_data.linkedin_url}/")  # Replace with your desired redirect URL
        else:
            messages.error(request, "There was an error submitting the form.")
    else:
        form = CompanyForm()
    
    return render(request, 'Companyaddform.html', {'form': form})

def company_page(request, linkedin_url):
    try:
        company = Company.objects.get(linkedin_url=linkedin_url)
    except Company.DoesNotExist:
        return HttpResponse("Page not found", status=404)
    
    return render(request, 'company_page.html', {'company': company})



def validate_company_url(request):
    if request.method == "GET":
        url = request.GET.get('url', '').strip()
        if url:
            is_taken = Company.objects.filter(linkedin_url=url).exists()
            return JsonResponse({'is_taken': is_taken})
    return JsonResponse({'error': 'Invalid request'}, status=400)