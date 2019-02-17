import argparse
import os
import sys
import textwrap
import unittest
from argparse import ArgumentParser
from contextlib import redirect_stdout
from io import StringIO
from typing import Union, List, Optional, Callable

from tests import refresh_files


class ArgParseExitException(Exception):
    ...


def _parser_exit(_: argparse.ArgumentParser,  __=0, message: Optional[str]=None) -> None:
    raise ArgParseExitException(message)


ArgumentParser.exit = _parser_exit


class CLITestCase(unittest.TestCase):
    testdir: str = None
    test_output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'output'))
    test_input_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'input'))
    testprog: str = None
    creation_messages: List[str] = None

    @staticmethod
    def prog_ep(argv: List[str]) -> bool:
        return False

    @classmethod
    def setUpClass(cls):
        cls.testdir_path = os.path.join(cls.test_output_dir, cls.testdir)
        os.makedirs(cls.testdir_path, exist_ok=True)
        cls.creation_messages = []

    @classmethod
    def tearDownClass(cls):
        if cls.creation_messages:
            for msg in cls.creation_messages:
                print(msg, file=sys.stderr)
            cls.creation_messages = []
            assert False, "Tests failed because baseline files were being created"

    def do_test(self, args: Union[str, List[str]], testfile: Optional[str]="",
                update_test_file: bool=False, error: type(Exception)=None, tox_wrap_fix: bool=False,
                failexpected: bool=False, text_filter: Callable[[str], str]=None) -> None:
        """ Execute a cli test

        @param args: Argument string or list to command
        @param testfile: name of file to record output in.  If absent, using directory mode
        @param update_test_file: True means we need to update the test file
        @param error: If present, we expect this error
        @param tox_wrap_fix: tox seems to wrap redirected output at 60 columns.  If true, try wrapping the test
        file before failing
        @param failexpected: True means we're logging an error
        @param text_filter: edits to remove non-matchable items
        """
        testfile_path = os.path.join(self.testdir_path, testfile)
        if text_filter is None:
            text_filter = lambda txt: txt.replace('\r\n', '\n').strip()

        outf = StringIO()
        arg_list = args.split() if isinstance(args, str) else args
        if error:
            with self.assertRaises(error):
                self.prog_ep(arg_list)
            return

        with redirect_stdout(outf):
            try:
                success = not self.prog_ep(arg_list)
            except ArgParseExitException:
                success = False

        self.assertTrue(success or failexpected)
        if not os.path.exists(testfile_path):
            with open(testfile_path, 'w') as f:
                f.write(outf.getvalue())
                self.creation_messages.append(f'{testfile_path} did not exist - updated')

        if testfile:
            with open(testfile_path) as f:
                new_txt = text_filter(outf.getvalue())
                old_txt = text_filter(f.read())
                if old_txt != new_txt and tox_wrap_fix:
                    old_txt = textwrap.fill(old_txt, 60)
                    new_txt = textwrap.fill(new_txt, 60)
                self.assertEqual(old_txt, new_txt)
        else:
            print("Directory comparison needs to be added", file=sys.stderr)

    @staticmethod
    def clear_dir(folder: str) -> None:
        import os
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)


if __name__ == '__main__':
    unittest.main()
