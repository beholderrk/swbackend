from django.conf.urls import url
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.http import HttpMethodNotAllowed, HttpAccepted
from tastypie.models import ApiKey
from tastypie.resources import ModelResource
from tastypie import fields
from tastypie.utils import dict_strip_unicode_keys, trailing_slash
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
        authorization = DjangoAuthorization()
        authentication = ApiKeyAuthentication()

    def prepend_urls(self):
        return [
            url('^login$', self.wrap_view('login'), name='login'),
            url('^logout', self.wrap_view('logout'), name='logout'),
        ]

    def login(self, request):
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

    def logout(self, request):
        if request.method != 'DELETE':
            return HttpMethodNotAllowed()
        logout(request)
        return HttpAccepted()


class CategoryResource(ModelResource):
    class Meta:
        queryset = Category.objects.all()
        resource_name = 'categories'
        authorization = DjangoAuthorization()
        authentication = ApiKeyAuthentication()


class RequirementsResource(ModelResource):
    class Meta:
        queryset = Requirements.objects.all()
        resource_name = 'requirements'
        authorization = DjangoAuthorization()
        authentication = ApiKeyAuthentication()

    def prepend_urls(self):
        return [
            url(r'^(?P<resource_name>%s)/values%s' % (self._meta.resource_name, trailing_slash()), self.wrap_view('values'), name="api_requirements_values"),
        ]

    def values(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)

        values = Requirements.objects.filter(mode='rank').values_list('value', flat=True).distinct()
        values = [ {'name': value} for value in values ]

        self.log_throttled_access(request)
        return self.create_response(request, values)


class EdgeResource(ModelResource):
    category = fields.ToOneField(CategoryResource, 'category', readonly=True, full=True)
    requirements = fields.ToManyField(RequirementsResource, 'requirements', readonly=True, full=True)

    class Meta:
        queryset = Edge.objects.all()
        resource_name = 'edges'
        authorization = DjangoAuthorization()
        authentication = ApiKeyAuthentication()
        allowed_methods = ['get', 'delete', 'post', 'put', 'patch']
        list_allowed_methods = ['get', 'post']
        always_return_data = True

    def obj_create(self, bundle, **kwargs):
        # todo: rewrite this logic to custom view with custom validation
        reqres = RequirementsResource()
        req_obj = Requirements.objects.filter(value=bundle.data['rank']['name'])[0]
        req_bundle = reqres.build_bundle(obj=req_obj, request=bundle.request)
        req_bundle = reqres.full_dehydrate(req_bundle)
        bundle.data['requirements'] = [req_bundle.data]
        del bundle.data['rank']
        return super(EdgeResource, self).obj_create(bundle, **kwargs)


