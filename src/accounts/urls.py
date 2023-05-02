from django.urls import path
from . import views
from django.contrib.auth.views import LoginView,LogoutView

urlpatterns = [
    path('', views.home_view),

    path('adminclick', views.adminclick_view),
    path('studentclick', views.studentclick_view),

    path('adminsignup', views.adminsignup_view),
    path('studentsignup', views.studentsignup_view),
    path('adminlogin', LoginView.as_view(template_name='adminlogin.html')),
    path('studentlogin', LoginView.as_view(template_name='studentlogin.html')),

    path('logout', LogoutView.as_view(template_name='index.html')),
    path('afterlogin', views.afterlogin_view),

    path('addbook', views.addbook_view),
    path('viewbook', views.viewbook_view),
    path('studentviewbook', views.student_viewbook_view),

    path('search', views.search_view, name='search'),

    path('issuebook', views.issuebook_view),
    path('viewissuedbook', views.viewissuedbook_view),
    path('delete/<int:id>/', views.destroy, name='deletedata'),
    path('viewstudent', views.viewstudent_view),
    path('viewissuedbookbystudent', views.viewissuedbookbystudent),

]
