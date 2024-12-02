from django import forms
from .models import Rateyourcompany, Emailsignup, SignupFinish, Otpverifiction, Post, Comment, Resume,Resume_headline, Keyskills, Employment, Education,Itskills, Project, Profile_summary, Career_profile, Personal_details, JobPosting,Qualification, JobApplication,Company
from django.core.exceptions import ValidationError
from PIL import Image
import os

class RateyourcompanyForm(forms.ModelForm):
    class Meta:
        model = Rateyourcompany
        fields = ('Companyname','Jobtitle','overallrating','worklifebalance','salaryandbenefits','promostion',
                  'jobsecurity','skilldevelopment','worksatisfation','companyculture','companylikes','companydislikes',
                  'male','female','prefernottosay','workfromhome','office','hybrid','currentlyworkingyes','No','selectemploymenttype',
                  'deperment')
        

class EmailsingupForm(forms.ModelForm):
    class Meta:
        model = Emailsignup
        fields = ('Email', 'Username', 'password', 'Repassword')
        widgets = {
            'Email': forms.TextInput(attrs={'placeholder': 'Enter your work email address', 'class': 'input'}),
            'Username': forms.TextInput(attrs={'placeholder': 'UserName', 'class': 'input'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'input'}),
            'Repassword': forms.PasswordInput(attrs={'placeholder': 'Re-enter Password', 'class': 'input'})
        }

    def clean(self):
        cleaned_data = super().clean()
        valpwd = cleaned_data.get('password')
        valrpwd = cleaned_data.get('Repassword')

        # Check if the passwords match
        if valpwd and valrpwd and valpwd != valrpwd:
            self.add_error('Repassword', 'Passwords do not match')

        return cleaned_data

    # def clean_Email(self):
    #     email = self.cleaned_data.get('Email')

    #     # Check if email already exists
    #     if Emailsignup.objects.filter(Email=email).exists():
    #         raise ValidationError("An account with this email address already exists!")

    #     return email
            


class SignupfinishForm(forms.ModelForm):
    class Meta:
        model = SignupFinish
        fields = ('Firstname', 'Lastname',  'Mobile', 'Companyname', 'Companywebsite','Designation')


        widgets = {
            'Designation': forms.TextInput(attrs={'id':'input','placeholder':'Designation', 'name':'Designation'}),
            'Firstname': forms.TextInput(attrs={'placeholder':'Your first name', 'name':'Firstname'}),
            'Lastname': forms.TextInput(attrs={'placeholder':'Your last name', 'name':'Lastname'}),
            'Mobile': forms.TextInput(attrs={'placeholder':'Mobile Number', 'name':'Mobile'}),
            'Companyname': forms.TextInput(attrs={'placeholder':'Company Name', 'name':'Companyname'}),
            'Companywebsite': forms.TextInput(attrs={'placeholder':'Company Website', 'name':'Companywebsite'}),
        }

class OtpverificationForm(forms.ModelForm):
    class Meta:
        model = Otpverifiction
        fields = ('Inputotp',)

        widgets = {
            'Inputotp': forms.TextInput(attrs={'placeholder':'OTP', 'class':'input'})
        }

class postform(forms.ModelForm):
    class Meta:
        model=Post
        fields = ['title','slug','body','publish','status','images','tags','post_type']

        widgets = {
            'title': forms.TextInput(attrs={'placeholder':'Title', 'class':'input',}),
            'slug': forms.TextInput(attrs={'placeholder':'Slug', 'class':'input'}),
            'publish': forms.TextInput(attrs={'placeholder':'publish', 'class':'input'}),
            'body': forms.Textarea(attrs={'placeholder':'body', 'class':'input'}),
            'status': forms.Select(attrs={'placeholder':'status', 'class':'input'}),
            'tags': forms.TextInput(attrs={'placeholder':'Tags', 'class':'input'}),
            
            
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name','email','body')

class Resumeform(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['resume',]
        
class Resume_headlineform(forms.ModelForm):
    class Meta:
        model = Resume_headline
        fields = ['objective',]

        widgets = {
            'objective': forms.Textarea(attrs={'id':'resumeHeadlineTxt', 'class':'resumeHeadlineTxt materialize-textarea','placeholder':'Minimum 5 words. Sample headlines: Sales Manager well versed in Excel and Dynamics CRM. Senior-level Interior Designer with expertise in 3D modeling.','name':'objective'}),
        }
        labels = {
            'objective': '',  # This will remove the label
        }

class Keyskills_form(forms.ModelForm):
    class Meta:
        model = Keyskills
        fields = ['keyskills',]
        widgets = {
            'keyskills': forms.TextInput(attrs={'id': 'skillsTxt', 'class': 'skillsTxt', 'placeholder': 'Minimum 1 skill.', 'name': 'keyskills'}),
        }
        labels = {
            'keyskills': '',
        }

class Employmentform(forms.ModelForm):
    class Meta:
        model = Employment
        fields = ['current_employment', 'employment_type', 'years_of_experience', 'months_of_experience', 'current_company', 'current_job', 'years_of_Joining', 'months_of_Joining', 'Current_salary', 'skill_used', 'Job_prfile', 'Notice_period',]


        
        widgets = {
        #     'current_employment': forms.RadioSelect(
        #         choices=[
        #             ('YES', 'Yes'),
        #             ('NO', 'No'),
        #         ],
        #         attrs={
        #             'name': 'current_employment',                   # Set the name (optional, Django automatically sets this)
        #         }
        #     ),
        #     'employment_type': forms.RadioSelect(
        #         choices=[
        #             ('FULL_TIME', 'Full time'),
        #             ('INTERNSHIP', 'Internship'),
        
        #         ],
        #         attrs={
        #             'name': 'employment_type',                   # Set the name (optional, Django automatically sets this)
        #         }),

        #         'years_of_experience': forms.TextInput(
        #         attrs={
        #             'name': 'years_of_experience',                   # Set the name (optional, Django automatically sets this)
        #         }),

        #         'months_of_experience': forms.TextInput(
        #         attrs={
        #             'name': 'months_of_experience',                   # Set the name (optional, Django automatically sets this)
        #         }),

        #         'current_company': forms.TextInput(
        #         attrs={
        #             'name': 'current_company',                   # Set the name (optional, Django automatically sets this)
        #         }),

                'current_job': forms.TextInput(
                attrs={
                    'name': 'current_job',                   # Set the name (optional, Django automatically sets this)
                    'placeholder': 'Type your designation',
                }),

        #         'years_of_Joining': forms.TextInput(
        #         attrs={
        #             'name': 'years_of_Joining',                   # Set the name (optional, Django automatically sets this)
        #         }),

        #          'months_of_Joining': forms.TextInput(
        #         attrs={
        #             'name': 'months_of_Joining',                   # Set the name (optional, Django automatically sets this)
        #         }),

        #         'Current_salary': forms.TextInput(
        #         attrs={
        #             'name': 'Current_salary',                   # Set the name (optional, Django automatically sets this)
        #         }),

        #          'skill_used': forms.TextInput(
        #         attrs={
        #             'name': 'skill_used',                   # Set the name (optional, Django automatically sets this)
        #         }),

        #          'Job_prfile': forms.Textarea(
        #         attrs={
        #             'name': 'Job_prfile',                   # Set the name (optional, Django automatically sets this)
        #         }),

        #          'Notice_period': forms.Textarea(
        #         attrs={
        #             'name': 'Notice_period',                   # Set the name (optional, Django automatically sets this)
        #         }),
        }
class Educationform(forms.ModelForm):
    FULL_TIME = 'FULL_TIME'
    PART_TIME = 'PART_TIME'
    CORRESPONDENCE = 'CORRESPONDENCE'

    COURSE_TYPE_CHOICES = [
        (FULL_TIME, 'Full time'),
        (PART_TIME, 'Part time'),
        (CORRESPONDENCE, 'Correspondence/Distance learning'),
    ]
    course_type =forms.ChoiceField(
        choices=COURSE_TYPE_CHOICES,
        widget=forms.RadioSelect
    )
    class Meta:
        model = Education
        fields = ['select_education', 'university', 'course', 'specialixation', 'course_type', 'startingyear_of_course', 'endingyear_of_course', 'grading_system']


class Itskillsform(forms.ModelForm):
    class Meta:
        model = Itskills
        fields = ['skill_software_name', 'software_version', 'last_used', 'years_of_experiences', 'months_of_experiences',]


class Projectform(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['project_title','client','project_type','year_of_working','month_of_working','details_of_project','project_location','project_site_choices','employment_type_project','team_size','role','role_decription','skill_used',]

class Profile_summaryform(forms.ModelForm):
    class Meta:
        model = Profile_summary
        fields = ['summary',]


class career_profileform(forms.ModelForm):
    chipsVal = forms.CharField(required=False) 
    class Meta:
        model = Career_profile
        fields = ['Current_industry','Department','Role_category','Job_role','job_type_project','employment_type_career', 'shift_type_project','chipsVal','salary']

class Personal_detailsform(forms.ModelForm):
    class Meta:
        model = Personal_details
        fields = ['gender_type_project','Marital_type_project','date','month','year','differently_abled_type_career','career_break_type_career','permanent_address','hometown','pincode']

class CombinedJobForm(forms.ModelForm):
    qualifications = forms.ModelMultipleChoiceField(
        queryset=Qualification.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    class Meta:
        model = JobPosting
        fields = [
            'job_title', 'company_name', 'workplace', 'job_location',
            'job_type', 'description', 'skills', 'identify_source', 'additional_info','qualifications'
        ]

    def save(self, commit=True):
        job_post = super().save(commit=commit)
        return job_post

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['applicant_name', 'applicant_email','applicant_resume']

    
    def __init__(self, *args, **kwargs):
        self.job = kwargs.pop('job', None)
        super().__init__(*args, **kwargs)

        # Dynamically add fields for each qualification
        if self.job:
            for q in self.job.jobqualification_set.filter(must_have=True):
                field_name = f'qualification_{q.qualification.id}'
                self.fields[field_name] = forms.CharField(
                    label=q.qualification.question_text,
                    required=True,  # Ensure must-have qualifications are mandatory
                )
                self.fields[field_name].widget.attrs['is_qualification'] = True
        
class DynamicQuestionForm(forms.ModelForm):
    class Meta:
        model = Qualification
        fields = ['question_text', 'answer_type','ideal_answer', 'dropdown_options']
        widgets = {
            'dropdown_options': forms.Textarea(attrs={'placeholder': 'Comma-separated options for dropdown (if applicable)'})
        }

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = [
            'name', 'linkedin_url', 'website', 'industry', 
            'organization_size', 'organization_type', 'logo', 'tagline'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Add your organization’s name'}),
            'linkedin_url': forms.TextInput(attrs={'placeholder': 'Add your unique Scientificiq address'}),
            'website': forms.TextInput(attrs={'placeholder': 'Begin with http://, https:// or www.'}),
            'industry': forms.TextInput(attrs={'placeholder': 'ex: Information Services.'}),
            'tagline': forms.Textarea(attrs={'placeholder': 'ex: An information services firm helping small businesses succeed.'}),
        }

    
    def clean_logo(self):
        logo = self.cleaned_data.get('logo')

        if logo:
            # Validate file extension
            valid_extensions = ['jpg', 'jpeg', 'png']
            ext = os.path.splitext(logo.name)[1][1:].lower()
            if ext not in valid_extensions:
                raise ValidationError("Only JPG, JPEG, and PNG file formats are supported.")

            # Validate file format by inspecting content
            try:
                image = Image.open(logo)
                if image.format not in ['JPEG', 'JPG', 'PNG']:
                    raise ValidationError("Invalid image file format.")
                if image.width != 300 or image.height != 300:
                    raise ValidationError("The logo must be exactly 300x300 pixels.")
            except Exception as e:
                raise ValidationError(f"Error processing image: {str(e)}")
        return logo
    
    def clean_linkedin_url(self):
        linkedin_url = self.cleaned_data.get('linkedin_url')
        if Company.objects.filter(linkedin_url=linkedin_url).exists():
            raise forms.ValidationError("This public URL is already in use. Please choose a unique URL.")
        return linkedin_url