from django.contrib import admin
from show.models import Show
from django import forms

class ShowAdmin(admin.ModelAdmin):
    search_fields = ('title', 'director', 'cast', )

    list_display = (
        'title', 'director', 'countries', 'release_year', 'rating', 'duration', 'show_type'
        )

    list_filter = (
        'show_type', 'rating', 'release_year', 
    )

    fieldsets = (
        (None, {
            'fields': ('show_type', 'title', 'director', 'cast', 'description', 'release_year', )
        }),
        ('eins', {
            'fields': ('duration', 'countries', 'categories', 'rating', ),
        }),     
        ('Internal', {
            'fields': ('date_added', ),
        }),
    )

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(ShowAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name in ('cast', 'description'):
            formfield.widget = forms.Textarea(attrs=formfield.widget.attrs)
        return formfield    

admin.site.register(Show, ShowAdmin)