from django.conf.urls import url, patterns, include
from api import EdgeResource, UserResource, CategoryResource, RequirementsResource


edge_resource = EdgeResource()
user_resource = UserResource()
category_resource = CategoryResource()
requirements_resource = RequirementsResource()


urlpatterns = patterns('',
    url(r'^api/', include(edge_resource.urls)),
    url(r'^api/', include(user_resource.urls)),
    url(r'^api/', include(category_resource.urls)),
    url(r'^api/', include(requirements_resource.urls)),
)