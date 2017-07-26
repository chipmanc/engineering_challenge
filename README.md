# Blacklist Query API

This repo provides a service to indicate if a URL is safe to visit or not.  It can be loaded with URLs from a site such as zeustracker, or from a local file.

The format of the file should be one URL per line.

### Virtualenvironment
This app requires python3, and has several dependencies.  It is recommended to create a virtual environment.  You may need to install virtualenv via pip:

```
pip install virtualenv
virtualenv -p python3 django_malware
```

After installation, activate the virtualenv and install requirements:
```
source django_malware/bin/activate
pip install -r requirements.txt
```

### Load URLs into database
You will need to prep the database for loading URLs:
```
python manage.py makemigrations
python manage.py migrate
python manage.py load_blacklist --location PATH_TO_BLACKLISTED_URLS
```

### API
To use the API, requests should come in like so:
`/urlinfo/1/DOMAIN:PORT/PATH/OF/URL`

### Miscellaneous
It is recommended to run this app behind a proxy such as nginx.  That is beyond the scope of this readme.  You can run this app from testing purposes with:
```
python manage.py runserver
```
This will listen for API requests on localhost at port 8000.