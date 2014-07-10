from django.contrib import admin
from .models import Edge, Category, Requirements


class RequirementsInline(admin.TabularInline):
    model = Requirements


class EdgeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = [RequirementsInline,]


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Edge, EdgeAdmin)
admin.site.register(Category, CategoryAdmin)