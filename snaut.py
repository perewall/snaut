#!/usr/bin/env python

from dotenv import load_dotenv

from click import ClickException
from click import command, option, argument, version_option, echo, File, Path

from requests import post
from requests.auth import HTTPBasicAuth
from requests.exceptions import HTTPError
from requests.packages.urllib3 import disable_warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning


__version__ = '1.1.0'


ASSETS = ('pypi', 'rubygems', 'nuget', 'npm')


load_dotenv('.env')


@command(context_settings=dict(auto_envvar_prefix='SNAUT'))
@option('-r', '--repo', required=True,
        help='Full componens API URL with repository, e.g. '
        'http(s)://.../components?repository=myrepo')
@option('-a', '--asset', help='Asset type - {0}'.format(','.join(ASSETS)))
@option('-d', '--directory', type=Path(dir_okay=True, file_okay=False),
        help='Upload directory for RAW asset type,'
        ' argument of assert type will be ignored if this option is set')
@option('-u', '--username', help='Username [optional]')
@option('-p', '--password', help='Password [optional]')
@option('-v', '--verbose', is_flag=True, help='Verbose output')
@option('--timeout', type=int, default=10,
        show_default=True, help='Request timeout (sec)')
@option('--no-verify', is_flag=True, help='Ignore SSL verify error')
@argument('files', nargs=-1, type=File('rb'), required=True)
@version_option(__version__)
def upload(
        repo, asset, directory, username, password,
        verbose, timeout, no_verify, files):
    """Artifact upload tool for Sonatype Nexus 3"""

    if directory:
        if asset:
            echo('WARNING: -d option is set, -a option will be ignored')
        asset = 'raw'
    elif not asset:
        raise ClickException('Asset type must be provided')
    elif asset.lower() not in ASSETS:
        message = 'Unknown asset type "{0}", supported types - {1}'
        raise ClickException(message.format(asset, ', '.join(ASSETS)))

    credentials = None  # optional
    if username and password:
        credentials = HTTPBasicAuth(username, password)

    if no_verify:
        disable_warnings(category=InsecureRequestWarning)

    filename = '{0}.asset'.format(asset)
    rw = None
    failed = False
    for file in files:
        echo('uploading {0}: '.format(file.name), nl=False)

        if directory:
            filename = 'raw.asset0'
            rw = {'raw.directory': directory, 'raw.asset0.filename': file.name}

        try:
            response = post(
                url=repo, auth=credentials, verify=(not no_verify),
                data=rw, files={filename: file}, timeout=timeout)
            response.raise_for_status()
        except HTTPError as e:
            failed = True
            echo('failed')
            echo('code: {0}, response: {1}\n'.format(
                e.response.status_code, e.response.text), err=True)
        except Exception as e:
            failed = True
            echo('failed')
            echo('{0}\n'.format(e), err=True)
        else:
            echo('success')

    if failed:
        raise ClickException('One or more files failed to upload')


if __name__ == '__main__':  # pragma: no cover
    upload()
