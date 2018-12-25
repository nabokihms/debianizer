debianizer
===
To package your python project into `.deb` package with `dh-virtualenv` you need 
to form `debian` folder with specific information. <br>
This tool helps to do it **in one click!**
## How to use
###Install
from PyPi
```bash
pip3 install debianizer
```
from Source
```bash
git clone `link_to_the_repo`
cd debianizer
pip3 install .
```
require python >= 3.5

### Use
Simple command tool.
Type `debianizer --help` for additional info.

Your project directory should look like this.
```
project_directory
├── your_project
│   ├── module_folder
│   │   ├── file_one.py
│   │   └── file_two.py
│   ├── file_one.py
│   └── file_two.py
└── setup.py
```

To run:
```bash
cd project_directory && debianizer
```
or 
```bash
debianizer --workdir project_directory
```
Script will silently do his best.
To add some output you can change the log level.
```
debianizer --workdir project_directory --loglevel INFO
```
## setup.py
We are trying to get all necessary information from your setup.py. 
* Your name (maintainer_name or author_name)
* Your email (maintainer_email or author_email)
* Package Name (name)
* Package Version (version)
* Command line scripts (entry_points.console_scripts) 

If something is absent, we will add something on our own.
