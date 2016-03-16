import os
from VCF4DTE.settings import BASE_DIR
from mdls.config import *
from django.template import Template, Context
import pytz
import dateutil.parser


def list_directories(path):
    return [name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))]


def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def read_file(path):
    with open(path) as file:
        return file.read()


def write_file(path, data):
    file = open(path, 'w+')
    file.write(data)
    file.close()


def first_level_dir_absolute_path(dir_name):
    return os.path.join(BASE_DIR, dir_name)


def get_absolute_template_path(template_name):
    return os.path.join(first_level_dir_absolute_path(TEMPLATE_DIR_NAME), template_name + TEMPLATE_FILE_EXTENSION)


def localize_to_utc(time_str):
    time = dateutil.parser.parse(time_str)
    return pytz.utc.localize(time)


class ScriptBuilder:
    static_templates = {
        'library': read_file(get_absolute_template_path('library')),
        'runner': read_file(get_absolute_template_path('runner'))
    }

    def __init__(self):
        self.blocks = list()

    def append_library(self):
        self.blocks.append(self.static_templates['library'])
        return self

    def append_main(self, main_block):
        self.blocks.append(main_block)
        return self

    def append_runner(self):
        self.blocks.append(self.static_templates['runner'])
        return self

    def build(self):
        return '\n'.join(self.blocks)


def generate_standard_script(output_path, main_template_file_name, data):
    main_template = read_file(get_absolute_template_path(main_template_file_name))
    main_block = (Template(main_template)).render(Context(data))
    full_script = ScriptBuilder().append_library().append_main(main_block).append_runner().build()
    write_file(os.path.join(output_path, main_template_file_name + '.py'), full_script)


class CommandBuilder:
    commands = list()

    def __init__(self):
        self.commands = list()

    def append(self, command):
        self.commands.append(command)
        return self

    def append_cd(self, path):
        self.commands.append('cd ' + path)
        return self

    def append_git_clone(self, repo):
        self.commands.append('git clone ' + repo)
        return self

    def append_git_add_all(self):
        self.commands.append('git add .')
        return self

    def append_git_commit(self, message='admin'):
        self.commands.append('git commit -m "' + message + '"')
        return self

    def append_git_pull(self):
        self.commands.append('git pull')
        return self

    def append_git_push(self):
        self.commands.append('git push -u origin master')
        return self

    def append_git_rm_dir(self, dir_name):
        self.commands.append('git rm -r ' + dir_name)
        return self

    def append_git_permanent_delete_dir(self, dir_name):
        self.commands.append("git filter-branch --tree-filter 'rm -rf " + dir_name + "' HEAD")
        return self

    def build(self):
        return '\n'.join(self.commands)
