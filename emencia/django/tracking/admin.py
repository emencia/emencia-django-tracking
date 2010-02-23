"""Admin for emencia.django.tracking"""
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from emencia.django.tracking.models import Activity

class ActivityAdmin(admin.ModelAdmin):
    date_hierarchy = 'creation_date'
    search_fields = ('title', 'description')
    list_display = ('title', 'action', 'related_object_admin', 'creation_date')
    list_filter = ('action', 'creation_date')
    fieldsets = ((None, {'fields': ('title', 'description', 'url', 'action')}),
                 (_('Advanced'), {'fields': ('object_id', 'content_type'),
                                  'classes': ('collapse',)}),)
    actions_on_top = False
    actions_on_bottom = True

    def related_object_admin(self, activity):
        """Display link to related object's admin"""
        if activity.content_type and activity.object_id:
            try:
                admin_url = reverse('admin:%s_%s_change' % (activity.content_type.app_label,
                                                            activity.content_type.model),
                                    args=(activity.object_id,))
                return '%s: <a href="%s">%s</a>' % (activity.content_type.model.capitalize(),
                                                    admin_url,
                                                    activity.content_object.__unicode__())
            except:
                return '%s: %s' % (activity.content_type.model.capitalize(),
                                   activity.content_object.__unicode__())

        return _('No relative object')
    related_object_admin.allow_tags = True
    related_object_admin.short_description = _('Related object')

admin.site.register(Activity, ActivityAdmin)
