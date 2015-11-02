from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView
from django.contrib.auth.views import login
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
import homework

admin.autodiscover()
# Examples:
# url(r'^$', 'homeworkpal_project.views.home', name='home'),
# url(r'^homeworkpal_project/', include('homeworkpal_project.foo.urls')),

# Uncomment the admin/doc line below to enable admin documentation:
# url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

# Uncomment the next line to enable the admin:
urlpatterns = patterns('',
                       url(r'^$', TemplateView.as_view(template_name='base.html')),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^homework/', include('homework.urls')),
                       url(r'^projects/', include('project_admin.urls', namespace='project')),
                       url(r'^employees/', include('employee.urls', namespace='employee')),
                       url(r'^accounts/login/$', 'django.contrib.auth.views.login',
                           {'template_name': 'admin/login.html'}, name='login'),
                       url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', name='logout'),
                       )

# Uncomment the next line to serve media files in dev.
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += patterns('',
                            url(r'^__debug__/', include(debug_toolbar.urls)),
                            )
