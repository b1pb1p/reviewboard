from kgb import SpyAgency
from reviewboard.scmtools.git import ShortSHA1Error, GitClient
from reviewboard.scmtools.hg import HgDiffParser, HgGitDiffParser
        def get_file(self, path, revision, **kwargs):
        def file_exists(self, path, revision, **kwargs):
        def file_exists(self, path, revision, **kwargs):
        def get_file(self, path, revision, **kwargs):
        def file_exists(self, path, revision, **kwargs):
    def test_get_file_signature_warning(self):
        """Test old SCMTool.get_file signature triggers warning"""
        def get_file(self, path, revision):
            return 'file data'

        self.scmtool_cls.get_file = get_file

        path = 'readme'
        revision = 'e965047'
        request = {}

        warn_msg = ('SCMTool.get_file() must take keyword arguments, '
                    'signature for %s is deprecated.' %
                    self.repository.get_scmtool().name)

        with self.assert_warns(message=warn_msg):
            self.repository.get_file(path, revision, request=request)

    def test_file_exists_signature_warning(self):
        """Test old SCMTool.file_exists signature triggers warning"""
        def file_exists(self, path, revision=HEAD):
            return True

        self.scmtool_cls.file_exists = file_exists

        path = 'readme'
        revision = 'e965047'
        request = {}

        warn_msg = ('SCMTool.file_exists() must take keyword arguments, '
                    'signature for %s is deprecated.' %
                    self.repository.get_scmtool().name)

        with self.assert_warns(message=warn_msg):
            self.repository.get_file_exists(path, revision, request=request)

    def test_git_parser_selection_with_header(self):
        """Testing HgTool returns the git parser when a header is present"""
        diffContents = (b'# HG changeset patch\n'
                        b'# Node ID 6187592a72d7\n'
                        b'# Parent  9d3f4147f294\n'
                        b'diff --git a/emptyfile b/emptyfile\n'
                        b'new file mode 100644\n')

        parser = self.tool.get_parser(diffContents)
        self.assertEqual(type(parser), HgGitDiffParser)

    def test_hg_parser_selection_with_header(self):
        """Testing HgTool returns the hg parser when a header is present"""
        diffContents = (b'# HG changeset patch'
                        b'# Node ID 6187592a72d7\n'
                        b'# Parent  9d3f4147f294\n'
                        b'diff -r 9d3f4147f294 -r 6187592a72d7 new.py\n'
                        b'--- /dev/null   Thu Jan 01 00:00:00 1970 +0000\n'
                        b'+++ b/new.py  Tue Apr 21 12:20:05 2015 -0400\n')

        parser = self.tool.get_parser(diffContents)
        self.assertEqual(type(parser), HgDiffParser)

    def test_git_parser_sets_commit_ids(self):
        """Testing HgGitDiffParser sets the parser commit ids"""
        diffContents = (b'# HG changeset patch\n'
                        b'# Node ID 6187592a72d7\n'
                        b'# Parent  9d3f4147f294\n'
                        b'diff --git a/emptyfile b/emptyfile\n'
                        b'new file mode 100644\n')

        parser = self.tool.get_parser(diffContents)
        parser.parse()
        self.assertEqual(parser.new_commit_id, b'6187592a72d7')
        self.assertEqual(parser.base_commit_id, b'9d3f4147f294')

                        b'rename from path/to file/readme.txt\n'
                        b'rename to new/path to/readme.txt\n'
                        'rename from path/to file/réadme.txt\n'
                        'rename to new/path to/réadme.txt\n'
                        '+++ b/new/path to/réadme.txt\n').encode('utf-8')
        self.assertTrue(self.tool.file_exists('doc/readme', rev))
        self.assertTrue(not self.tool.file_exists('doc/readme2', rev))
    def test_get_file_base_commit_id_override(self):
        """Testing base_commit_id overrides revision in HgTool.get_file"""
        base_commit_id = Revision('661e5dd3c493')
        bogus_rev = Revision('bogusrevision')
        file = 'doc/readme'

        value = self.tool.get_file(file, bogus_rev,
                                   base_commit_id=base_commit_id)
        self.assertTrue(isinstance(value, bytes))
        self.assertEqual(value, b'Hello\n\ngoodbye\n')

        self.assertTrue(self.tool.file_exists(
            'doc/readme',
            bogus_rev,
            base_commit_id=base_commit_id))
        self.assertTrue(not self.tool.file_exists(
            'doc/readme2',
            bogus_rev,
            base_commit_id=base_commit_id))

class GitTests(SpyAgency, SCMTestCase):
    def test_valid_repository_https_username(self):
        """Testing GitClient.is_valid_repository with an HTTPS URL and external
        credentials
        """
        client = GitClient('https://example.com/test.git',
                           username='username',
                           password='pass/word')

        self.spy_on(client._run_git)
        client.is_valid_repository()

        self.assertEqual(client._run_git.calls[0].args[0],
                         ['ls-remote',
                          'https://username:pass%2Fword@example.com/test.git',
                          'HEAD'])
