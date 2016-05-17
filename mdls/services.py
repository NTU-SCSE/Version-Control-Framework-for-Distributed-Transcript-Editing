from mdls.utils import *
from mdls.models import *
import os
import json
import shutil


def create_repositories(self, request, queryset):
    editors = queryset.filter(has_local_repo=False)

    for editor in editors:
        # git clone
        command = CommandBuilder().append_cd(first_level_dir_absolute_path(WORKSPACE_DIR_NAME)).append_git_clone(
            editor.ssh_git_repo).build()
        os.system(command)

        # generate .gitignore
        gitignore = read_file(get_absolute_template_path('gitignore'))
        write_file(os.path.join(editor.get_absolute_dir(), '.gitignore'), gitignore)

        # copy tools folder
        # shutil.copytree(first_level_dir_absolute_path(TOOLS_DIR_NAME), editor.get_absolute_tools_dir())

        # generate pull script
        generate_standard_script(editor.get_absolute_dir(), 'pull', {})

        # git add, commit and push
        command = CommandBuilder().append_cd(
            editor.get_absolute_dir()).append_git_pull().append_git_add_all().append_git_commit().append_git_push().build()
        os.system(command)

        # generate clone script
        data = {
            'repo': editor.http_git_repo
        }
        generate_standard_script(editor.get_absolute_dir(), 'clone', data)

        # update flag
        editor.has_local_repo = True
        editor.save()


def make_allocation(self, request, queryset):
    files = queryset.filter(editor__isnull=False, is_allocated=False)

    for file in files:
        # create job directories
        create_directory(file.get_absolute_dir())
        create_directory(file.get_absolute_metadata_dir())
        create_directory(file.get_absolute_session_dir())

        # generate start script
        generate_standard_script(file.get_absolute_dir(), 'start', {})

        # generate push script
        generate_standard_script(file.get_absolute_dir(), 'push', {})

        # generate metadata file
        metadata = {
            'id': file.id,
            'type': file.type
        }
        write_file(os.path.join(file.get_absolute_metadata_dir(), METADATA_FILE_NAME), json.dumps(metadata))

        # copy transcript file
        shutil.copy(os.path.join(BASE_DIR, SOURCE_DIR_NAME, file.transcript_filename),
                    os.path.join(file.get_absolute_dir(), file.transcript_filename))

        # copy media file
        shutil.copy(os.path.join(BASE_DIR, SOURCE_DIR_NAME, file.media_filename),
                    os.path.join(file.get_absolute_dir(), file.media_filename))

        # git add, commit and push
        command = CommandBuilder().append_cd(file.editor.get_absolute_dir()).append_git_add_all().append_git_commit().append_git_push().build()
        os.system(command)

        # update flag
        file.is_allocated = True
        file.save()


def get_latest_data(self, request, queryset):
    files = queryset.filter(is_allocated=True, is_completed=False)

    for file in files:
        # git pull
        command = CommandBuilder().append_cd(file.get_absolute_dir()).append_git_pull().build()
        os.system(command)

        # read session files
        for session_file in os.listdir(file.get_absolute_session_dir()):
            # get absolute file path
            session_file_path = os.path.join(file.get_absolute_session_dir(), session_file)

            # create new entries in SessionHistory
            content = read_file(session_file_path)
            data = json.loads(content)
            session_entry = SessionHistory.objects.create(
                start_datetime=localize_to_utc(data['start'].replace('@', ':')),
                end_datetime=localize_to_utc(data['end'].replace('@', ':')),
                marker_count=data['noOfMarkers'],
                segment_count=data['noOfSegments'],
                editor=Editor.objects.get(user__username=data['editor']),
                file=file
            )
            session_entry.save()

            # delete session files
            os.remove(session_file_path)

        # read metadata file
        metadata_file_path = os.path.join(file.get_absolute_metadata_dir(), METADATA_FILE_NAME)
        content = read_file(metadata_file_path)
        data = json.loads(content)

        # update flag
        file.latest_comment = data['comment']
        file.progress = data['progress']
        file.is_declared_finished = data['finished']
        file.save()

        # git add, commit and push
        command = CommandBuilder().append_cd(
            file.editor.get_absolute_dir()).append_git_add_all().append_git_commit().append_git_push().build()
        os.system(command)


def complete_and_move_back_to_source_folder(self, request, queryset):
    files = queryset.filter(is_allocated=True, is_completed=False)

    for file in files:
        # move transcript back to source folder and replace
        source_dir_path = first_level_dir_absolute_path(SOURCE_DIR_NAME)
        os.remove(os.path.join(source_dir_path, file.transcript_filename))
        shutil.move(os.path.join(file.get_absolute_dir(), file.transcript_filename), source_dir_path)

        # git rm
        command = CommandBuilder().append_cd(file.editor.get_absolute_dir()).append_git_rm_dir(str(file.id)).build()
        os.system(command)
        shutil.rmtree(file.get_absolute_dir())

        # git add, commit and push
        command = CommandBuilder().append_cd(
            file.editor.get_absolute_dir()).append_git_pull().append_git_add_all().append_git_commit().append_git_push().build()
        os.system(command)

        # update flag
        file.is_completed = True
        file.save()
