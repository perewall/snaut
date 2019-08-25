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

    def test_upload_error(self):
        """Upload error"""
        args = (self.args[0], '-r', self.args[-1], '-a', 'wrong')
        result = self.cli.invoke(upload, args)  # wrong asset type
        self.assertEqual(result.exit_code, 1)
        self.assertIn('wrong', result.stdout)

        result = self.cli.invoke(upload, self.args)
        self.assertEqual(result.exit_code, 1)

    @activate
    def test_upload_failed(self):
        """Upload failed"""
        add('POST', self.args[-1], status=400, json={'message': 'wrong'})
        result = self.cli.invoke(upload, self.args)
        self.assertEqual(result.exit_code, 1)
        self.assertIn('wrong', result.stdout)

    @activate
    def test_upload_success(self):
        """Upload success"""
        add('POST', self.args[-1])
        args = (self.args[0], '-r', self.args[-1], '-a', self.args[-3])
        result = self.cli.invoke(upload, args)
        self.assertEqual(result.exit_code, 0)


if __name__ == '__main__':
    main()
