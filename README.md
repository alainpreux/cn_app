# About cn_app

## what it is
application providing services to parse a escapad formated files

## Versions
v 0.2 added template mechanism for home page

# Usage

## Installation

Install the requirements with pip:

```
$ pip install -r requirements.txt
```

Depending on your system, some python libraries depend on system-modules. For Debian-based distribution, make sure the following packages are installed:

- libxml2-dev
- libxslt-dev
- python-libxml2
- python-libxslt1
- python-dev
- zlib1g-dev

For the Django web app cn_app to work, you need to copy `cn_app/site_settings.template.py` as `cn_app/site_settings.py`:
 ```
 $ cp cn_app/site_settings.template.py cn_app/site_settings.py

 ```

and change the settings depending on your running environment (dev, production, domain name, database, etc)

## Export script src/CnExport.py

This script takes module structure as input, parses the module's markdown files `moduleX/moduletitle.md` and generates a web site export presenting course's modules in a user-friendly fashion. General usage is:
```
(considering current dir is cn_app dir)
$ python src/cnExport.py -r path/to/module_repository -d /path/to/destination/folder
```

This will generate a web site for all modules contained in given repository. Optionnaly you can:

- choose which module to export by specifying module folder's names separeted by space `-m module1 module2 `
- choose to generate also IMS CC  archive for use in LMSs like Moodle, Blackboard, etc. `-i`
- add feebacks and correct responses `-f`
- specify a global config file for the modules `-c path/to/config/file`



## Running the Web application locally

First do the migrations:

```
$ python manage.py migrate
```

Then start the web application locally with:

```
$ python manage.py runserver
```

and go to web adress at `http://localhost:8000`
