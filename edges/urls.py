from django.conf.urls import url, patterns, include
from api import EdgeResource, UserResource


edge_resource = EdgeResource()
user_resource = UserResource()


urlpatterns = patterns('',
    url(r'^api/', include(edge_resource.urls)),
    url(r'^api/', include(user_resource.urls)),
)