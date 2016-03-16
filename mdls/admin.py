from django.contrib import admin

from .models import *
from .services import *


class EditorHasRepositoryFilter(admin.SimpleListFilter):
    title = "if he/she already has a repository"

    parameter_name = "status"

    def lookups(self, request, model_admin):
        return (
            ('have', 'have a repository'),
            ('doesnt', "doesn't have a repository")
        )

    def queryset(self, request, queryset):
        if self.value() == 'have':
            return queryset.filter(has_local_repo=True)

        if self.value() == 'doesnt':
            return queryset.filter(has_local_repo=False)


class EditorAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'current_files', 'full_country', 'language_code', 'score', 'has_local_repo')

    search_fields = (
        'user__first_name', 'user__last_name', 'git_username', 'language_code',
        'score')

    list_filter = ('language_code', 'score', EditorHasRepositoryFilter)

    create_repositories.short_description = 'Clone repository to local'
    actions = [create_repositories]


class FileStatusListFilter(admin.SimpleListFilter):
    title = 'status'

    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return (
            ('not-assigned', 'not assigned'),
            ('assigned-but-not-allocated', 'assigned but not allocated'),
            ('in-progress', 'in progress'),
            ('declared-finished', 'declared to be finished'),
            ('completed-and-removed', 'completed & moved back to source folder'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'not-assigned':
            return queryset.filter(editor__isnull=True)

        if self.value() == 'assigned-but-not-allocated':
            return queryset.filter(editor__isnull=False, is_allocated=False)

        if self.value() == 'in-progress':
            return queryset.filter(is_allocated=True, is_declared_finished=False, is_completed=False)

        if self.value() == 'declared-finished':
            return queryset.filter(is_declared_finished=True, is_completed=False)

        if self.value() == 'completed-and-removed':
            return queryset.filter(is_completed=True)


class FileAdmin(admin.ModelAdmin):
    list_display = (
        'transcript_filename', 'id', 'editor_name', 'start_datetime', 'deadline_datetime', 'progress_percentage',
        'latest_comment', 'type', 'is_allocated', 'is_declared_finished', 'is_completed')

    search_fields = ('editor__user__first_name', 'editor__user__last_name', 'transcript_filename')

    list_filter = ('editor', FileStatusListFilter)

    actions = [make_allocation, get_latest_data, complete_and_move_back_to_source_folder]


class SessionHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'file', 'editor', 'start_datetime', 'end_datetime', 'progress')

    search_fields = ('editor__user__first_name', 'editor__user__last_name', 'file__transcript_filename')


admin.site.register(Editor, EditorAdmin)
admin.site.register(File, FileAdmin)
admin.site.register(SessionHistory, SessionHistoryAdmin)
