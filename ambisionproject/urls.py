"""
URL configuration for ambisionproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include,re_path
from abisionapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('allauth.urls')),
    path('', views.home),
    path('login/',views.login_view, name='login'),
    path('Writereview/',views.Rateyourcompany),
    path('employer/',views.employer),
    path('notifications/', views.notifications, name='notifications'),
    path('validate-company-url/', views.validate_company_url, name='validate_company_url'),
    path('signup/',views.signup),
    path('signupfinish/',views.signup2),
    path('Otpverification/',views.otp),
    path('createcompany/',views.createcompany, name='createcompany'),
    path('feed/',views.feed),
    path('postlogin/',views.post_view),
    path('profile/',views.profile,name='profile'),
    path('tag/',views.post_list_view),
    path('tagslug/',views.post_list_view,name='post_list_by_tag_name'),
    path('jobs/',views.jobs),
    path('logout/',views.logoutview),
    path('Companyadd/',views.Companyadd, name='Companyadd'),
    path('<str:username>/', views.user_profile, name='user_profile'),
    path('list/', views.list_headlines, name='list_headlines'),
    path('update/<int:pk>/', views.update_headline, name='update_headline'),
    path('delete/<int:pk>/', views.delete_headline, name='delete_headline'),
    path('delete1/<int:pk>/', views.delect_skill, name='delete_skill'),
    path('delete_employee/<int:pk>/', views.delete_employee, name='delete_employee'),
    path('delete_education/<int:pk>/', views.delete_education, name='delete_education'),
    path('delete_itskills/<int:pk>/', views.delete_itskills, name='delete_itskills'),
    path('delete_project/<int:pk>/', views.delete_project, name='delete_project'),
    path('delete_profile/<int:pk>/', views.delete_profile, name='delete_profile'),
    path('delete_career/<int:pk>/', views.delete_career, name='delete_career'),
    path('delete_personal/<int:pk>/', views.delete_personal, name='delete_personal'),
    path('delete_resume/<int:pk>/', views.delete_resume, name='delete_resume'),
    path('follow/<int:user_id>/', views.follow_user, name='follow_user'),
    path('feedforemployer/', views.feedforemployer, name='feedforemployer'),
    path('employerlogin/',views.dynamicemployer, name='dynamicemployer'),
    path('Job-posting-description/',views.registrationform, name='registrationform'),
    path('comfirmjobsetting/',views.comfirmjobsetting, name='comfirmjobsetting'),
    path('<int:job_id>/', views.job_detail, name='job_detail'),
    path('<str:linkedin_url>/', views.company_page, name='company_page'),
    path('jobshomepage/<int:job_id>/', views.jobshomepage, name='jobshomepage'),
    path('application_success/', views.application_success, name='application_success'),
    path('job/<int:job_id>/applicant/<str:username>/', views.job_posting_detail, name='job_posting_detail'),
    path('my-posted-jobs/', views.my_posted_jobs, name='my_posted_jobs'),
    path('applied-jobs/', views.myappliedjobs, name='myappliedjobs'),
    path('dynamic_questions/', views.create_dynamic_questions, name='create_dynamic_questions'),
    path('jobpostingdetail/<int:job_id>/', views.jobpostingdetail, name='jobpostingdetail'),
    path('apply/<int:job_id>/', views.apply_for_job, name='apply_for_job'),
    path('alljobapplicants/<int:job_id>/', views.alljobapplicants, name='alljobapplicants'),
    path('<str:username>/', views.posteduser, name='posteduser'),
   
    # path('<tag_slug>/',views.post_list_view,name='post_list_by_tag_name'),
    path('<year>/<month>/<day>/<post>', views.post_detail_view,name='post_detail'),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
# urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)


