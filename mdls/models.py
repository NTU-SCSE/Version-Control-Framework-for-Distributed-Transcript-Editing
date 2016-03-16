import os

from django.contrib.auth.models import User
from django.db import models
from VCF4DTE.settings import BASE_DIR
from mdls.config import *

from django_countries.fields import CountryField


class Editor(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    country = CountryField()
    language_code = models.CharField(max_length=2, verbose_name="language")
    score = models.IntegerField(default=0)
    has_local_repo = models.BooleanField(default=False, verbose_name="with local repository")
    http_git_repo = models.TextField(max_length=2083, verbose_name="http")
    ssh_git_repo = models.TextField(max_length=2083, verbose_name="ssh")

    def full_name(self):
        return self.user.get_full_name()

    def full_country(self):
        return self.country.name + ' (' + self.country.code + ')'

    def __str__(self):
        return self.user.get_full_name()

    def current_files(self):
        return File.objects.all().filter(editor=self, is_completed=False).count()

    def get_absolute_dir(self):
        return os.path.join(BASE_DIR, WORKSPACE_DIR_NAME, self.user.username)

    def get_absolute_tools_dir(self):
        return os.path.join(self.get_absolute_dir(), TOOLS_DIR_NAME)


class File(models.Model):

    CREATION = 'creation'
    CORRECTION = 'correction'

    TYPES = (
        (CREATION, 'Creation'),
        (CORRECTION, 'Correction')
    )

    editor = models.ForeignKey(Editor, blank=True, null=True)
    start_datetime = models.DateTimeField(blank=True, null=True, verbose_name="start")
    deadline_datetime = models.DateTimeField(blank=True, null=True, verbose_name="deadline")
    media_filename = models.CharField(max_length=255, verbose_name="media file")
    transcript_filename = models.CharField(max_length=255, verbose_name="transcript file")
    source_dir_name = models.CharField(max_length=255, default=SOURCE_DIR_NAME, verbose_name="source directory")
    is_allocated = models.BooleanField(default=False, verbose_name="allocated")
    is_declared_finished = models.BooleanField(default=False, verbose_name="declared finished")
    is_completed = models.BooleanField(default=False, verbose_name="completed")
    latest_comment = models.TextField(default='', blank=True)
    progress = models.FloatField(default=0.0)
    type = models.CharField(max_length=25, choices=TYPES, default=CORRECTION)

    def editor_name(self):
        if self.editor is None:
            return ''
        else:
            return self.editor.user.get_full_name()

    def progress_percentage(self):
        return "{0:.2f}%".format(self.progress * 100)

    def __str__(self):
        return self.transcript_filename

    def get_absolute_dir(self):
        return os.path.join(self.editor.get_absolute_dir(), str(self.id))

    def get_absolute_metadata_dir(self):
        return os.path.join(self.get_absolute_dir(), METADATA_DIR_NAME)

    def get_absolute_session_dir(self):
        return os.path.join(self.get_absolute_metadata_dir(), SESSIONS_DIR_NAME)


class SessionHistory(models.Model):
    editor = models.ForeignKey(Editor)
    file = models.ForeignKey(File)
    start_datetime = models.DateTimeField(verbose_name="start")
    end_datetime = models.DateTimeField(verbose_name="end")
    marker_count = models.IntegerField(verbose_name="no. of markers")
    segment_count = models.IntegerField(verbose_name="no. of segments")

    def editor_name(self):
        return self.editor.user.get_full_name()

    def file_name(self):
        return self.file.transcript_filename

    def progress(self):
        return "{0:.2f}%".format((1 - (self.marker_count / self.segment_count)) * 100)

    class Meta:
        verbose_name_plural = "session histories"
