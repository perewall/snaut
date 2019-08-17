from unittest import TestCase, main

from click.testing import CliRunner
from responses import add, reset, activate

from snaut import upload


class SnautTest(TestCase):

    args = (
        __file__,
        '--verbose',
        '--no-verify',
        '--timeout', '5',
        '--username', 'example',
        '--password', 'p@ssw0rd',
        '--asset', 'pypi',
        '--repo', 'https://nexus.url'
    )

    def setUp(self):
        self.cli = CliRunner()

    def tearDown(self):
        reset()

    def test_without_file(self):
        """Call without file"""
        result = self.cli.invoke(upload, [])
        self.assertEqual(result.exit_code, 2)

    def test_without_repo(self):
        """Call without repository"""
        result = self.cli.invoke(upload, (self.args[0], '-a', 'pypi'))
        self.assertEqual(result.exit_code, 1)

    def test_without_asset(self):
        """Call without asset type"""
        result = self.cli.invoke(upload, (self.args[0], '-r', self.args[-1]))
        self.assertEqual(result.exit_code, 1)

    @activate
    def test_upload_failed(self):
        """Upload failed"""
        add('POST', self.args[-1], status=400, json={'ok': 'Bad'})
        result = self.cli.invoke(upload, self.args)
        self.assertEqual(result.exit_code, 1)

    @activate
    def test_upload_error(self):
        """Upload error"""
        add('POST', self.args[-1], body=Exception('Untrusted'))
        result = self.cli.invoke(upload, self.args)
        self.assertEqual(result.exit_code, 1)

    @activate
    def test_upload_success(self):
        """Upload success"""
        add('POST', self.args[-1])
        result = self.cli.invoke(upload, self.args)
        self.assertEqual(result.exit_code, 0)


if __name__ == '__main__':
    main()
