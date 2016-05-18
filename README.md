# Version Control Framework for Distributed Transcript Editing

## Introduction

This is a open-source version constrol framework for distributed transcript editing with ELAN. It was originally developed for Rolls-Royce@NTU Corporate Lab, under Apache License, Version 2.0.

There are two actors in this system - admin and editors. Admin is the guy who is responsible for editor database maintenance, job allocation, etc. Editors are professional transcriptors who use ELAN for editing transcripts, working on a single job (file) at a time.

The technologies under this project includes Git and Django. 

## System Requirements

### For Admin

1. Pyhton 3.5
2. Git 

### For Editors

1. Python 3.5
2. Git
3. ELAN

## Installation

1. Download source
2. Install dependencies: `$ pip install -r requirements.txt`


## Prerequisite Checklist

### Admin

#### Preparing Git

First, make sure you have an available Git hosting, such as GitHub, BitBucket, your own GitLab server, or your company's repository hosting.

Second, make sure you have set up SSH for Git so that you can successfully access remote SSH URLs from command line.

#### Choose a Local "Source" Folder

Choose a directory on your local computer as the "source", where you store the audio/video and transcript file pairs. 

For example, `"~/Documents/source"` on Mac. From now, we will denote the absolute path of the source folder as `[path_to_source]`

### Editor

1. Install all required tools/software in the previous section
1. Setup the file association on your operating system, so that when you double click the ELAN transcript file, the system starts the ELAN app with the transcript file loaded.
1. Setup the file association on your operating system, so that when you double click ".py" files, the system will prompt a command line window.
1. If you have any problem during the setup, contact your admin for assistance.

## User Guide

### Admin

#### Start Admin Site

`$ python manage.py runserver`

#### Create Super User (Admin)

If there is no super user in the system yet, create one using the following command:

```bash
$ python manage.py createsuperuser
```

#### Login to Admin Site

1. Go to http://127.0.0.1:8000/admin/login/
1. Login using the created super user account.

#### Setup Repository for a New Editor

First, create a user account in the Django admin:

1. Go to http://127.0.0.1:8000/admin/auth/user/
1. Click "ADD USER" on the upper right corner
1. Fill in the form and click "SAVE"
1. Go to the user details page and complete the "First name" and "Last name" fields under "Personal Info"

Then, configure your Git hosting

1. Create a user account on your Git hosting for this new eidtor
1. Create a Git repository, whose name is **exactly the same** as the "username" you chose for this editor in the Django system
1. Make sure both the new account and your own have push privilege on this repository

Finally, create an entry for `Editor` in the Django admin

1. Go to http://127.0.0.1:8000/admin/mdls/editor/
1. Click "ADD EDITOR" on the upper right corner
1. Select from the drop down menu "User" as the user that you just created
1. Fill in the rest of the form ("http" and "ssh" fields indicate the protocol of the Git repository URL), while leaving the "With local repository" as UNCHECKED
1. Click "SAVE"

#### Add a New Job

First, copy the to-be-edited audio/video and transcript file pair into the pre-designated "source" folder at `[path_to_source]`. Make sure the audio/video file has **exactly the same** filename prefix (filename without extension) as the transcript file.

Second, navigate to the web page

1. Go to http://127.0.0.1:8000/admin/mdls/file/
1. Click "ADD FILE" on the upper right corner

Fill in "Media file" and "Transcript file" fields in the form, which are the file names (with extensions) of the video/audio and transcript files.

Then, while leaving all other fields untouched, and click "SAVE".

#### Allocate a Job

1. http://127.0.0.1:8000/admin/mdls/file/
1. Click and enter the detail page of the file that you wish to allocation
1. Select the editor in the dropdown menu "Editor" and click "SAVE"
1. Click the "Assigned but not allocated" filter on the right
1. Tick the file that you just assigned to an editor
1. Select "Make allocation" in the "Action" dropdown menu
1. Click the button "Go"
1. Wait for the web page to finish loading

Now, you may check the folder at `workspace/[editor_name]/[file_id]` and verify if all the necessary files are present.

#### Get the Latest Update

1. Go to http://127.0.0.1:8000/admin/mdls/file/
1. Select "In progress" filter on the right column
1. Tick all the files that you wish to get the latest progress on
1. Select "Get latest data" in the dropdown menu of "Action" and click the "Go" button
1. Wait for the web page to finish loading

Now you can see each file's

1. Latest statistics - http://127.0.0.1:8000/admin/mdls/sessionhistory/
1. Editing session history - http://127.0.0.1:8000/admin/mdls/sessionhistory/

#### Complete a File

1. Go to http://127.0.0.1:8000/admin/mdls/file/
1. Tick the files that you wish to mark as completed and move back to the "source"  directory
1. Select "Complete and move back to source folder" in the "Action" dropdown menu, and click "Go"
1. Wait for the web page to finish loading

Now you can see all completed files by selecting the "Completed & moved back to source folder" filter on the right.

### Editor

#### First-time Setup Repository

1. Get the `clone.py` file from the admin
1. Place the `clone.py` in a folder that you'd prefer to be your workspace
1. Double click `clone.py` to run the script
1. Enter your username and password as instructed in the prompt window

#### Sync to the Latest Version

1. Go to your workspace folder
1. Double click `pull.py`
1. Enter your username and password as instructed in the prompt window

#### Work on a Transcript File

1. Go to the file folder in your workspace
1. Double click `start.py`
1. Work on the transcript file on the ELAN window
1. When finishing, close the ELAN window only, with the command prompt window open.
1. Fill in the prompt questions in the command line window, as well as your username and password, as instructed.

#### Push Your Changes to the Server

1. Go to the file folder in your workspace
1. Double click `push.py`
1. Fill in the prompt questions in the command line window, as well as your username and password, as instructed
