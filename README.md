[![image](https://travis-ci.org/perewall/snaut.svg?branch=master)](https://travis-ci.org/perewall/snaut)
[![image](https://codecov.io/gh/perewall/snaut/branch/master/graph/badge.svg)](https://codecov.io/gh/perewall/snaut)
[![image](https://img.shields.io/pypi/pyversions/snaut.svg)](https://pypi.org/project/snaut/)
[![image](https://img.shields.io/pypi/l/snaut.svg)](https://pypi.org/project/snaut/)
[![image](https://img.shields.io/pypi/v/snaut.svg)](https://pypi.org/project/snaut/)


# Snaut
Artifact upload tool for Sonatype Nexus 3

Alternative to `curl -X POST -u user:pwd -F "pypi.asset=@mypackage.whl" ...`

Supported asset types: `pypi`, `rubygems`, `nuget`, `npm`

See [API docs](https://help.sonatype.com/repomanager3/rest-and-integration-api/components-api#ComponentsAPI-UploadComponent)


## Installation
`pip install snaut`


## Usage
`snaut --help`

`snaut -r http://host/service/rest/v1/components?repository=myrepo -a pypi mypackage.whl`

Environment variables can be useful in your CI/CD pipeline:
- SNAUT_REPO
- SNAUT_ASSET
- SNAUT_DIRECTORY
- SNAUT_USERNAME
- SNAUT_PASSWORD
- SNAUT_VERBOSE
- SNAUT_TIMEOUT
- SNAUT_NO_VERIFY

Example:
```
python setup.py sdist bdist_wheel
snaut dist/*
```
RAW asset type:
```
snaut -d /mypath dist/*
snaut -d / myfile.zip
```


### Requirements
* [click](https://click.palletsprojects.com)
* [requests2](https://2.python-requests.org)
