# VCF4DTE - Version Control Framework for Distributed Transcript Editing

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
2. Start admin site: `$ python manage.py startserver`

## Workflow

### Admin

To be continued


