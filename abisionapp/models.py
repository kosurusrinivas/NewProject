from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from phone_field import PhoneField
from django.contrib.auth.models import User
from django.utils import timezone
from  django.urls import reverse
from django.core.validators import FileExtensionValidator
from taggit.managers import TaggableManager
from django.core.exceptions import ValidationError
from django.utils.text import slugify
import os

# Create your models here.

class Rateyourcompany(models.Model):
    Companyname = models.CharField(max_length=200)
    Jobtitle = models.CharField(max_length=200)
    overallrating = models.IntegerField(default=0)
    worklifebalance = models.IntegerField(default=0)
    salaryandbenefits = models.IntegerField(default=0)
    promostion = models.IntegerField(default=0)
    jobsecurity = models.IntegerField(default=0)
    skilldevelopment = models.IntegerField(default=0)
    worksatisfation = models.IntegerField(default=0)
    companyculture = models.IntegerField(default=0)
    companylikes = models.TextField(max_length=300)
    companydislikes = models.TextField(max_length=300)
    male = models.BooleanField(default=False)
    female = models.BooleanField(default=False)
    prefernottosay = models.BooleanField(default=False)
    workfromhome = models.BooleanField(default=False)
    office = models.BooleanField(default=False)
    hybrid = models.BooleanField(default=False)
    currentlyworkingyes = models.BooleanField(default=False)
    No = models.BooleanField(default=False)
    selectemploymenttype = (('Fulltime',"Fulltime"),
                          ('Parttime',"Parttime"),
                          ('Contractual',"Contractual"),
                          ('Inter',"Inter"),
                          ('Freelancer',"Freelancer"))
    
    selectemploymenttype = models.CharField(max_length=20,choices=selectemploymenttype)

    deperment = models.TextField(max_length=200)


class Emailsignup(models.Model):
    Email = models.EmailField(max_length=200)
    Username = models.CharField(max_length=200, default='')
    password = models.CharField(max_length=50, default='')
    Repassword = models.CharField(max_length=50 ,default='')

    def __str__(self) :
        return self.Email
    

class Designations(models.Model):
    Designations = models.CharField(max_length=200)

    def __str__(self): 
        return f"{self.Designations}"
    

class SignupFinish(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    Firstname = models.CharField(max_length=200)
    Lastname = models.CharField(max_length=200)
    Designation = models.CharField(max_length=200)
    Mobile = models.IntegerField(validators=[MinValueValidator(1000000000), MaxValueValidator(9999999999)])
    Companyname = models.CharField(max_length=200)
    Companywebsite = models.URLField()

class Otpverifiction(models.Model):
    Inputotp = models.IntegerField()

class CustomManger(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status = 'published')


    
class profile(models.Model):
    signupFinish = models.ForeignKey(SignupFinish, on_delete=models.CASCADE,)

def validate_file_size(value):
    filesize = value.size
    if filesize > 2 * 1024 * 1024:  # 2 MB limit
        raise ValidationError("The maximum file size that can be uploaded is 2 MB")
    return value

class Resume(models.Model):
    resume = models.FileField(upload_to="uploads/",validators=[FileExtensionValidator(allowed_extensions=['doc', 'docx', 'rtf', 'pdf']),validate_file_size],blank=True,null=True  )
    user = models.ForeignKey(User, on_delete=models.CASCADE,  null=False, default='')  # Associate resume with a user
    created = models.DateTimeField(auto_now_add=True) # Add timestamp to track when resume was uploaded

    def filename(self):
        return os.path.basename(self.resume.name)
    

class Resume_headline(models.Model):
    objective = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE,  null=False, default='') 
    def __str__(self):
        return self.objective
    

class Keyskills(models.Model):
    keyskills = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE,  null=False, default='')
    def __str__(self):
        return self.keyskills
    

class Employment(models.Model):
    YES = 'yes'
    NO = 'no'

    CURRENT_EMPLOYMENT_CHOICES = [
        (YES, 'Yes'),
        (NO, 'No'),
    ]

    FULL_TIME = 'full_time'
    INTERNSHIP = 'internship'

    EMPLOYMENT_TYPE_CHOICES = [
        (FULL_TIME, 'Full time'),
        (INTERNSHIP, 'Internship'),
    ]

    current_employment = models.CharField(
        max_length=3,
        choices=CURRENT_EMPLOYMENT_CHOICES,
        default=NO
    )

    employment_type = models.CharField(
        max_length=10,
        choices=EMPLOYMENT_TYPE_CHOICES,
        default=FULL_TIME
    )

    years_of_experience = models.CharField(max_length=50)
    months_of_experience = models.CharField(max_length=50)
    current_company = models.CharField(max_length=100)
    current_job = models.CharField(max_length=100)
    years_of_Joining = models.IntegerField(default=0)
    months_of_Joining = models.CharField(max_length=50)
    Current_salary = models.IntegerField(default=0)
    skill_used = models.CharField(max_length=50)
    Job_prfile = models.CharField(max_length=4000)
    Notice_period = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE,  null=False, default='')


class Education(models.Model):
    select_education = models.CharField(max_length=100)
    university = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    specialixation = models.CharField(max_length=100)
    FULL_TIME = 'FULL_TIME'
    PART_TIME = 'PART_TIME'
    CORRESPONDENCE = 'CORRESPONDENCE'

    COURSE_TYPE_CHOICES = [
        (FULL_TIME, 'Full time'),
        (PART_TIME, 'Part time'),
        (CORRESPONDENCE, 'Correspondence/Distance learning'),
    ]

    course_type = models.CharField(
        max_length=50,
        choices=COURSE_TYPE_CHOICES,
        default=FULL_TIME,  # Set a default if necessary
    )

    startingyear_of_course = models.CharField(max_length=100)
    endingyear_of_course = models.CharField(max_length=100)
    grading_system = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE,  null=False, default='')


class Itskills(models.Model):
    skill_software_name = models.CharField(max_length=100)
    software_version = models.CharField(max_length=100)
    last_used = models.CharField(max_length=100)
    years_of_experiences = models.CharField(max_length=100)
    months_of_experiences = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE,  null=False, default='')


class Project(models.Model):
    project_title = models.CharField(max_length=100)
    client = models.CharField(max_length=100)
    In_progress = 'In progress'
    Finished = 'Finished'

    PROJECT_CHOICES = [
        (In_progress, 'In progress'),
        (Finished, 'Finished'),

    ]

    project_type = models.CharField(
        max_length=50,
        choices=PROJECT_CHOICES,
        default=In_progress,  # Set a default if necessary
    )


    year_of_working = models.CharField(max_length=50)
    month_of_working = models.CharField(max_length=50)
    details_of_project = models.CharField(max_length=1000)
    project_location = models.CharField(max_length=100)

    Offsite = 'Offsite'
    Onsite = 'Onsite'

    PROJECT_SITE_CHOICES = [
        (Offsite, 'Offsite'),
        (Onsite, 'Onsite'),

    ]

    project_site_choices = models.CharField(
        max_length=50,
        choices=PROJECT_SITE_CHOICES,
        default=Offsite,  # Set a default if necessary
    )
    FULL_TIME = 'FULL_TIME'
    PART_TIME = 'PART_TIME'
    CONTRACTUAL = 'CONTRACTUAL'

    EMPLOYMENT_TYPE_CHOICES = [
        (FULL_TIME, 'Full time'),
        (PART_TIME, 'Part time'),
        (CONTRACTUAL, 'Contractual'),
    ]

    employment_type_project = models.CharField(
        max_length=50,
        choices=EMPLOYMENT_TYPE_CHOICES,
        default=FULL_TIME,  # Set a default if necessary
    )

    team_size = models.CharField(max_length=50)
    role = models.CharField(max_length=100)
    role_decription = models.CharField(max_length=250)
    skill_used = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE,  null=False, default='')



class Profile_summary (models.Model):
    summary = models.CharField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE,  null=False, default='')

class Career_profile(models.Model):
    Current_industry = models.CharField(max_length=100)
    Department = models.CharField(max_length=100)
    Role_category = models.CharField(max_length=100)
    Job_role = models.CharField(max_length=100)
    permanent = 'permanent'
    contractual = 'contractual'

    JOB_TYPE_CHOICES = [
        (permanent, 'permanent'),
        (contractual, 'contractual'),
    ]

    job_type_project = models.CharField(
        max_length=50,
        choices=JOB_TYPE_CHOICES,
        default=permanent,  # Set a default if necessary
    )

    fullTime = 'fullTime'
    partTime = 'partTime'

    EMPLOYMENT_TYPE_CHOICES = [
        (fullTime, 'fullTime'),
        (partTime, 'partTime'),
    ]

    employment_type_career = models.CharField(
        max_length=50,
        choices=    EMPLOYMENT_TYPE_CHOICES,
        default=fullTime,  # Set a default if necessary
    )

    Day = 'Day'
    Night = 'Night'
    Flexible = 'Flexible'

    SHIFT_TYPE_CHOICES = [
        (Day, 'Day'),
        (Night, 'Night'),
        (Flexible, 'Flexible'),
    ]

    shift_type_project = models.CharField(
        max_length=50,
        choices= SHIFT_TYPE_CHOICES,
        default=Day,  # Set a default if necessary
    )

    location = models.CharField(max_length=1000,)
    salary = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE,  null=False, default='')




class Personal_details(models.Model):
    Male = 'Male'
    Female = 'Female'
    Transgender = 'Transgender'

    GENDER_TYPE_CHOICES = [
        (Male, 'Male'),
        (Female, 'Female'),
        (Transgender, 'Transgender'),
    ]

    gender_type_project = models.CharField(
        max_length=50,
        choices= GENDER_TYPE_CHOICES,
    )

    Single = 'Single'
    Married = 'Married'
    Widowed = 'Widowed'
    Divorced = 'Divorced'
    Separated = 'Separated'
    Other = 'Other'

    Marital_TYPE_CHOICES = [
        (Single, 'Single/unmarried'),
        (Married, 'Married'),
        (Widowed, 'Widowed'),
        (Divorced, 'Divorced'),
        (Separated, 'Separated'),
        (Other, 'Other'),
    ]

    Marital_type_project = models.CharField(
        max_length=50,
        choices= Marital_TYPE_CHOICES,
    )

    date = models.CharField(max_length=100)
    month = models.CharField(max_length=100)
    year = models.CharField(max_length=100)
    Yes = 'Yes'
    No = 'No'

    differently_abled_TYPE_CHOICES = [
        (Yes, 'Yes'),
        (No, 'No'),
    ]

    differently_abled_type_career = models.CharField(
        max_length=50,
        choices=    differently_abled_TYPE_CHOICES,
    )

    yes = 'yes'
    no = 'no'

    career_break_TYPE_CHOICES = [
        (yes, 'yes'),
        (no, 'no'),
    ]

    career_break_type_career = models.CharField(
        max_length=50,
        choices=    career_break_TYPE_CHOICES,
    )

    permanent_address = models.CharField(max_length=100)
    hometown = models.CharField(max_length=100)
    pincode = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE,  null=False, default='')


class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    followed = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=[('requested', 'Requested'), ('accepted', 'Accepted')], default='requested')

    class Meta:
        unique_together = ('follower', 'followed')  

class Notification(models.Model):
    user = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)


class JobPosting(models.Model):
    job_title = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    workplace = models.CharField(max_length=50)
    job_location = models.CharField(max_length=255)
    job_type = models.CharField(max_length=50)
    description = models.TextField()
    skills = models.TextField()  # Store as comma-separated values
    identify_source = models.CharField(max_length=50)
    additional_info = models.CharField(max_length=100)  # Additional info from second 
    qualifications = models.ManyToManyField('Qualification', through='JobQualification')
    user = models.ForeignKey(User, on_delete=models.CASCADE,  null=False, default='')

    def __str__(self):
        return self.job_title
    

class Qualification(models.Model):
    question_text = models.TextField()
    ideal_answer = models.TextField(default="No ideal answer provided")  
    answer_type = models.CharField(
        max_length=50,
        choices=[
            ('text', 'Text'),
            ('number', 'Number'),
            ('dropdown', 'Dropdown'),
            ('boolean', 'Yes/No'),
        ],
        default='text'  # Default value for existing rows
    )
    dropdown_options = models.TextField(blank=True, null=True)  # Comma-separated dropdown options if applicable
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.question_text

class JobQualification(models.Model):
    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE)
    qualification = models.ForeignKey(Qualification, on_delete=models.CASCADE)
    must_have = models.BooleanField(default=False)  # Indicates if the qualification is required for application


class JobApplication(models.Model):
    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE)
    applicant_name = models.CharField(max_length=255)
    applicant_email = models.EmailField()
    applicant_resume = models.FileField(
        upload_to="uploads/",
        validators=[FileExtensionValidator(allowed_extensions=['doc', 'docx', 'rtf', 'pdf']), validate_file_size],
        blank=True, null=True
    )
    answers = models.ManyToManyField('Answer')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    

class Answer(models.Model):
    question = models.ForeignKey(Qualification, on_delete=models.CASCADE)
    answer_text = models.TextField()



class Company(models.Model):
    name = models.CharField(max_length=255)
    linkedin_url = models.CharField(max_length=255, unique=True)
    website = models.URLField()
    industry = models.CharField(max_length=255)
    organization_size = models.CharField(max_length=50)
    organization_type = models.CharField(max_length=50)
    logo = models.ImageField(upload_to='logos/')
    tagline = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE,  null=False, default='')

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.linkedin_url:
            self.linkedin_url = slugify(self.name)
        
        # Ensure unique URL by appending a counter if necessary
        original_url = self.linkedin_url
        counter = 1
        while Company.objects.filter(linkedin_url=self.linkedin_url).exists():
            self.linkedin_url = f"{original_url}-{counter}"
            counter += 1

        super().save(*args, **kwargs)

class Post(models.Model):
    POST_TYPE_CHOICES = [
        ('account', 'Account'),
        ('company', 'Company Page'),
    ]
    STATUS_CHOICES = (('draft','Draft'),('published','Published'))
    title = models.CharField(max_length=256)
    slug = models.SlugField(max_length=264,unique_for_date='publish')
    author = models.ForeignKey(User,related_name='blog_post',on_delete=models.CASCADE)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='draft')
    images = models.FileField(null=True,blank=True,upload_to="images/",validators=[FileExtensionValidator(allowed_extensions=['jpg','mp4','mp3','pdf','txt',])])
    objects = CustomManger()
    tags = TaggableManager()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', null=False, default='')
    company_page = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='posts', null=True, blank=True)
    post_type = models.CharField(
        max_length=20, 
        choices=POST_TYPE_CHOICES, 
        default='account'  # Set 'account' as the default value
    )

    class Meta :
        ordering = ('-publish',)
        def __str__(self):
            return self.title

    def get_absolute_url(self):
        return reverse('post_detail',args=[self.publish.year,self.publish.strftime('%m'),self.publish.strftime('%d'),self.slug])
    def __str__(self):
        if self.post_type == 'company' and self.company_page:
            return f"Post by {self.company_page.name}"
        return f"Post by {self.user.username}"
    
class Comment(models.Model):
    post = models.ForeignKey(Post,related_name='comments',on_delete=models.CASCADE)
    name = models.CharField(max_length=32)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active=models.BooleanField(default=True)
    class Meta:
        ordering = ('created',)
    def __str__(self):
        return "Comment By {} on {}".format(self.name,self.post)
    def get_absolute_url(self):
        return reverse('detail', kwargs={'pk': self.pk})

 