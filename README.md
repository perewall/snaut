# Snaut
Artifact upload tool for Sonatype Nexus 3

Alternative to `curl -X POST -u user:pwd -F "pypi.asset=@mypackage.whl" ...`

Supported asset types: `pypi`, `rubygems`, `nuget`, `npm`


## Installation
`pip install snaut`


## Usage
`snaut --help`

`snaut -r http://host/service/rest/v1/components?repository=myrepo -a pypi mypackage.whl`

Environment variables can be useful in your CI/CD pipeline:
- SNAUT_REPO
- SNAUT_ASSET
- SNAUT_USERNAME
- SNAUT_PASSWORD
- SNAUT_VERBOSE
- SNAUT_TIMEOUT
- SNAUT_NO_VERIFY

Example:
```
python setup.py bdist_wheel
snaut dist/mypackage.whl
```


### Requirements
* [click](https://click.palletsprojects.com)
* [requests2](https://2.python-requests.org)
