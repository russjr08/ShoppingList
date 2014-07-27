from django.conf.urls import patterns, include, url

from app import views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ShoppingList.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^new/', 'app.views.new_item', name='new'),
    url(r'^detail/items/(?P<item_id>\d+)/$', 'app.views.detail', name='detail'),
    url(r'^items/add/', 'app.views.add_item', name='add'),

    url(r'^api/items/', 'app.views.api_get_items'),
    url(r'^admin/', include(admin.site.urls)),
)
