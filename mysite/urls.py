"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path,include
from myapp import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),
    path('input1/',views.input1,name='input1'),
    path('input2/',views.input2,name='input2'),
    path('output/',views.output,name='output'),
    path('rslots/',views.rslots,name='rlots'),
    path('rteachers/',views.rteachers,name='rteachers'),
    path('slot_up/',views.slot_up,name='slot_up'),
    path('teacher_up/',views.teacher_up,name='teacher_up'),
    path('offer_up/',views.offer_up,name='offer_up'),
    path('course_up/',views.course_up,name='course_up'),
    path('output_page_next/',views.output_page_next,name='output_page_next'),
    path('output_page_prev/',views.output_page_prev,name='output_page_prev'),
    path('morning_only/',views.morning_only,name='morning_only'),
    path('evening_only/',views.evening_only,name='evening_only')
]
