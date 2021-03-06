"""ask URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
import qa.views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', qa.views.index, name='index'),
    url(r'^login/$', qa.views.login, name='login'),
    url(r'^signup/$', qa.views.signup, name='signup'),
    url(r'^question/(\d+)/$', qa.views.question_details, name='question-details'),
    url(r'^ask/$', qa.views.add_question),
    url(r'^popular/$', qa.views.popular, name='popular-question'),
]
