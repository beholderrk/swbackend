from django.conf.urls import url
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from tastypie.authentication import ApiKeyAuthentication
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.http import HttpMethodNotAllowed
from tastypie.models import ApiKey
from tastypie.resources import ModelResource
from tastypie import fields
from tastypie.utils import dict_strip_unicode_keys
from .models import Category, Edge, Requirements


class ApiKeyResource(ModelResource):
    class Meta:
        queryset = ApiKey.objects.all()
        resource_name = 'apikey'
        fields = ('key', 'created')


class UserResource(ModelResource):
    apikey = fields.OneToOneField(ApiKeyResource, 'api_key', full=True, readonly=True, null=True)

    class Meta:
        queryset = User.objects.all()
        resource_name = 'users'
        fields = ('id', 'username', 'first_name', 'last_name', 'date_joined')
        allowed_methods = ['get']
        authentication = ApiKeyAuthentication()

    def prepend_urls(self):
        return [
            url('^login$', self.wrap_view('login'), name='login')
        ]

    def login(self, request, *args, **kwargs):
        if request.method != 'POST':
            return HttpMethodNotAllowed()

        deserialized = self.deserialize(request, request.body, format=request.META.get('CONTENT_TYPE', 'application/json'))
        bundle = self.build_bundle(data=dict_strip_unicode_keys(deserialized), request=request)
        form = AuthenticationForm(data=bundle.data)
        if not form.is_valid():
            raise ImmediateHttpResponse(response=self.error_response(request, form.errors))

        username = form.cleaned_data['username']
        password_raw = form.cleaned_data['password']
        user = authenticate(username=username, password=password_raw)
        login(request, user)

        return self.get_detail(request, pk=user.pk)


class CategoryResource(ModelResource):
    class Meta:
        queryset = Category.objects.all()
        resource_name = 'category'


class RequirementsResource(ModelResource):
    class Meta:
        queryset = Requirements.objects.all()
        resource_name = 'requirements'


class EdgeResource(ModelResource):
    category = fields.ToOneField(CategoryResource, 'category', full=True)
    requirements = fields.ToManyField(RequirementsResource, 'requirements', full=True)

    class Meta:
        queryset = Edge.objects.all()
        resource_name = 'edges'
        authentication = ApiKeyAuthentication()


