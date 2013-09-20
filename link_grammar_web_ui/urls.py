from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', 'parser_ui.views.index', name='index'),
                       url(r'^parse_result(?P<page>)$', 'parser_ui.views.parse_result', name='parse'),
                       url(r'^site_settings$', 'parser_ui.views.settings', name='settings'),
                       # Examples:
                       # url(r'^$', 'link_grammar_web_ui.views.home', name='home'),
                       # url(r'^link_grammar_web_ui/', include('link_grammar_web_ui.foo.urls')),

                       # Uncomment the admin/doc line below to enable admin documentation:
                       # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

                       # Uncomment the next line to enable the admin:
                       # url(r'^admin/', include(admin.site.urls)),
)