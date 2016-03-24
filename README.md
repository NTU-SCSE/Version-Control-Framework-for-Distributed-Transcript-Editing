# Version Control Framework for Distributed Transcript Editing(tm)

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
2. Start admin site: `$ python manage.py runserver`

## User Guide

### Admin

#### Preparing Git

Make sure you have an available Git hosting, such as GitHub, BitBucket, your own GitLab server, or your company's repository hosting.



#### Create Super User

If there is no super user in the system yet, create one using the following command:

```bash
$ python manage.py createsuperuser
```

#### Login to Admin Site

1. Go to http://127.0.0.1:8000/admin/login/ 
1. Login using the created super user account.

#### Setup Repository for a New User

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
1. Fill in the rest of the form ("http" and "ssh" fields indicate the protocol of the Git repository URL)

#### Add a New Job

*To be continued - this document is still in progress, while the entire software system is working; you may wish to download the source and try out the features that are not documented yet*
