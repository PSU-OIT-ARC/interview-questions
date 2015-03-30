from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings

from .views import home
from .questions import views as questions
from .categories import views as categories
from .tags import views as tags

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    #url(r'^$', 'iq.views.home', name='home'),
    #url(r'^blog/', include('blog.urls')),

    # Admin
    url(r'^admin/', include(admin.site.urls)),

    # Authentication
    url(r'^accounts/login/$', 'djangocas.views.login', name='login'),
    url(r'^accounts/logout/$', 'djangocas.views.logout', name='logout'),

    # Questions
    url(r'^questions/list/?$', questions.list_, name='questions-list'),
    #url(r'^questions/detail/(?P<question_id>\d+)/?$', questions.detail, name='questions-detail'),
    url(r'^questions/edit/(?P<question_id>\d+)/?$', questions.edit, name='questions-edit'),
    url(r'^questions/create/?$', questions.create, name='questions-create'),
    url(r'^questions/delete/(?P<question_id>\d+)/?$', questions.delete, name='questions-delete'),

    # Categories
    url(r'^categories/list/?$', categories.list_, name='categories-list'),
    url(r'^categories/detail/(?P<category_id>\d+)/?$', categories.detail, name='categories-detail'),
    url(r'^categories/edit/(?P<category_id>\d+)/?$', categories.edit, name='categories-edit'),
    url(r'^categories/create/?$', categories.create, name='categories-create'),
    url(r'^categories/delete/(?P<category_id>\d+)/?$', categories.delete, name='categories-delete'),
    url(r'^categories/printout/(?P<category_id>\d+)/?$', categories.printout, name='categories-printout'),
    url(r'^categories/printout_applicant/(?P<category_id>\d+)/?$', categories.printout_applicant, name='categories-printout_applicant'),

    # Standard
    url(r'', include('django.contrib.auth.urls')),
    url(r'^cloak/', include('cloak.urls'))
)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static("htmlcov", document_root="htmlcov", show_indexes=True)
