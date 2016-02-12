from django.contrib import admin

from .models import Material, Decoration, Color, Finding, Artifact


class ArtifactAdmin(admin.ModelAdmin):

    date_hierarchy = 'found_date'
    exclude = ('found_date',)
    filter_horizontal = ('colors', 'decorations',)
    list_display = ('name', 'main_material', 'get_colors', 'found')
    search_fields = (
        'name',
        'description',
        'main_material__name',
        'decorations__name',
        'colors__name',
        'found__place',
        'found__discoverers__name',
        'found__discoverers__last_name',
    )


class FindingAdmin(admin.ModelAdmin):

    filter_horizontal = ('discoverers',)


admin.site.register(Material)
admin.site.register(Decoration)
admin.site.register(Color)
admin.site.register(Finding, FindingAdmin)
admin.site.register(Artifact, ArtifactAdmin)
