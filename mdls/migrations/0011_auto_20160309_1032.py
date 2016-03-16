# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-09 02:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mdls', '0010_auto_20160309_1027'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='editor',
            name='has_repository',
        ),
        migrations.RemoveField(
            model_name='file',
            name='source_directory_path',
        ),
        migrations.AddField(
            model_name='editor',
            name='has_local_repo',
            field=models.BooleanField(default=False, verbose_name='with local repository'),
        ),
        migrations.AddField(
            model_name='file',
            name='source_dir_name',
            field=models.CharField(default='source', max_length=255, verbose_name='source directory'),
        ),
        migrations.AlterField(
            model_name='editor',
            name='http_git_repo',
            field=models.TextField(max_length=2083, verbose_name='http'),
        ),
        migrations.AlterField(
            model_name='editor',
            name='language_code',
            field=models.CharField(max_length=2, verbose_name='language'),
        ),
        migrations.AlterField(
            model_name='editor',
            name='ssh_git_repo',
            field=models.TextField(max_length=2083, verbose_name='ssh'),
        ),
        migrations.AlterField(
            model_name='file',
            name='deadline_datetime',
            field=models.DateTimeField(blank=True, null=True, verbose_name='deadline'),
        ),
        migrations.AlterField(
            model_name='file',
            name='initial_segment_count',
            field=models.IntegerField(blank=True, null=True, verbose_name='initial no. of segments'),
        ),
        migrations.AlterField(
            model_name='file',
            name='is_allocated',
            field=models.BooleanField(default=False, verbose_name='allocated'),
        ),
        migrations.AlterField(
            model_name='file',
            name='is_completed',
            field=models.BooleanField(default=False, verbose_name='completed'),
        ),
        migrations.AlterField(
            model_name='file',
            name='is_declared_finished',
            field=models.BooleanField(default=False, verbose_name='declared finished'),
        ),
        migrations.AlterField(
            model_name='file',
            name='media_filename',
            field=models.CharField(max_length=255, verbose_name='media file'),
        ),
        migrations.AlterField(
            model_name='file',
            name='start_datetime',
            field=models.DateTimeField(blank=True, null=True, verbose_name='start'),
        ),
        migrations.AlterField(
            model_name='file',
            name='total_lines_count',
            field=models.IntegerField(blank=True, null=True, verbose_name='initial no. of lines'),
        ),
        migrations.AlterField(
            model_name='file',
            name='transcript_filename',
            field=models.CharField(max_length=255, verbose_name='transcript file'),
        ),
        migrations.AlterField(
            model_name='sessionhistory',
            name='end_datetime',
            field=models.DateTimeField(verbose_name='end'),
        ),
        migrations.AlterField(
            model_name='sessionhistory',
            name='marker_count',
            field=models.IntegerField(verbose_name='no. of markers'),
        ),
        migrations.AlterField(
            model_name='sessionhistory',
            name='segment_count',
            field=models.IntegerField(verbose_name='no. of segments'),
        ),
        migrations.AlterField(
            model_name='sessionhistory',
            name='start_datetime',
            field=models.DateTimeField(verbose_name='start'),
        ),
    ]
