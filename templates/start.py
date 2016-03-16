import os
import platform
import datetime
import json
import fnmatch
import sys

from xml.dom.minidom import parseString


def get_working_dir():
    return os.path.dirname(os.path.abspath(__file__))


def one_level_up():
    return os.path.abspath(os.path.join(get_working_dir(), os.pardir))


def parent_dir_name():
    return os.path.basename(one_level_up())


def from_working_dir(*args):
    current_dir = get_working_dir()
    for x in args:
        current_dir = os.path.join(current_dir, x)
    return current_dir


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


def pause():
    if platform.system() == 'Windows':
        os.system('pause')
    else:
        os.system('read -s -n 1 -p "Press any key to continue..."')


def count_markers(file_path):
    content = read_file(file_path)
    dom = parseString(content)
    result = dom.getElementsByTagName('ANNOTATION_VALUE')
    count = 0
    for x in result:
        data = x.firstChild.data
        if data.find('#') != -1:
            count += 1
    return count


def count_segments(file_path):
    content = read_file(file_path)
    dom = parseString(content)
    return len(dom.getElementsByTagName('ANNOTATION_VALUE'))


def get_file_name_ends_with(extension):
    for file in os.listdir('.'):
        if fnmatch.fnmatch(file, '*' + extension):
            return file


def start_elan():
    transcript_file_name = get_file_name_ends_with('.eaf')

    # get system utc time
    start_utc_time = datetime.datetime.utcnow().isoformat()

    if platform.system() == 'Windows':
        # todo
        os.system('start /wait' + transcript_file_name)

    elif platform.system() == 'Darwin':
        os.system('open -W ' + transcript_file_name)

    elif platform.system() == 'Linux':
        # todo
        ''
    # get system utc time
    end_utc_time = datetime.datetime.utcnow().isoformat()
    create_directory(os.path.join(get_working_dir(), 'metadata'))
    create_directory(os.path.join(get_working_dir(), 'metadata', 'sessions'))
    session = {
        'start': start_utc_time,
        'end': end_utc_time,
        'noOfMarkers': count_markers(from_working_dir(transcript_file_name)),
        'noOfSegments': count_segments(from_working_dir(transcript_file_name)),
        'editor': parent_dir_name()
    }

    write_file(from_working_dir('metadata', 'sessions', start_utc_time + '.json'), json.dumps(session))


def get_media_file():
    for file in os.listdir('.'):
        if (not os.path.isdir(file)) and (not file.startswith('.')) and (not file.endswith('.py')) and (not file.endswith('.eaf')) and (not file.endswith('.pfsx')):
            return file


def analyze_progress_for_correction():
    transcript_file_path = from_working_dir(get_file_name_ends_with('.eaf'))
    marker_count = count_markers(transcript_file_path)
    segment_count = count_segments(transcript_file_path)
    progress = 1 - (marker_count / segment_count)
    return progress


def commit_and_push():
    metadata_path = from_working_dir('metadata', 'metadata.json')
    content = read_file(metadata_path)
    metadata = json.loads(content)

    if metadata['type'] == 'correction':
        metadata['progress'] = analyze_progress_for_correction()
    elif metadata['type'] == 'creation':
        # todo: creation type
        metadata['progress'] = analyze_progress_for_correction()

    version = sys.version

    if version.startswith('3'):
        comment = input('Please enter your comment: ')
        declaration = input('Is this file finished? (y/N): ')
    elif version.startswith('2'):
        comment = raw_input('Please enter your comment: ')
        declaration = raw_input('Is this file finished? (y/N): ')

    metadata['comment'] = comment
    finished = False
    if declaration.lower() == 'y':
        finished = True
    metadata['finished'] = finished

    content = json.dumps(metadata)
    write_file(metadata_path, content)

    os.system('git status')
    os.system('git pull')
    os.system('git add .')
    os.system('git commit -m "editor"')
    os.system('git push')

    pause()


def main():
    start_elan()


if __name__ == "__main__":
    main()
