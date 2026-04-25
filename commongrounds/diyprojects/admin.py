from django.contrib import admin
from .models import Project, ProjectCategory, ProjectReview, ProjectRating, Favorite


class ProjectInLine(admin.TabularInline):
    model = Project


class ProjectCategoryAdmin(admin.ModelAdmin):
    model = ProjectCategory
    inline = [Project,]


class ProjectAdmin(admin.ModelAdmin):
    model = Project

    search_fields = ('title', 'category',)
    list_display = ('title', 'category', 'description', 'materials',
                    'materials', 'steps', 'created_on', 'updated_on',)
    list_filter = ('description', 'materials', 'steps', 'created_on',
                   'updated_on',)
    readonly_fields = ("created_on", "updated_on")
    fieldsets = [
        ('Details', {
            'fields': [
                ('title', 'description',
                 'materials', 'steps',
                 'created_on', 'updated_on',
                 ), 'category'
            ]
        }),
    ]


admin.site.register(ProjectCategory, ProjectCategoryAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectReview)
admin.site.register(ProjectRating)
admin.site.register(Favorite)