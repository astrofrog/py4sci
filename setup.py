#!/usr/bin/env python

import os
import glob
import shutil

from setuptools import setup, Command

import string


def strip_punctuation(text):
    return ''.join(ch for ch in text if ch not in string.punctuation)


class BuildTOC(Command):

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):

        from IPython.nbformat.current import read, write

        with open('template.rst', 'r') as f:
            template = f.read()

        toc = ""

        from urllib import quote

        for notebook in (glob.glob('lectures/*.ipynb')):

            with open(notebook, 'r') as f:
                nb = read(f, 'json')

            for ws in nb.worksheets:
                for cell in ws.cells:
                    if cell.cell_type == 'heading':
                        if cell['level'] > 1:
                            continue
                        toc += ("   " * (cell['level'] - 1) +
                                "* `{0} <_static/{1}.html#{2}>`__\n".format(cell['source'].replace('`', ''),
                                                                            quote(os.path.basename(notebook)).replace('.ipynb', ''),
                                                                            strip_punctuation(cell['source']).replace(' ', '-')))

        with open('www/index.rst', 'w') as f:
            f.write(template.format(lectures_toc=toc))

class ClearOutput(Command):

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):

        from IPython.nbformat.current import read, write

        for notebook in glob.glob('?.???/*.ipynb'):

            with open(notebook, 'r') as f:
                nb = read(f, 'json')

            for ws in nb.worksheets:
                for cell in ws.cells:
                    if cell.cell_type == 'code':
                        cell.outputs = []
                        if 'prompt_number' in cell:
                            cell.pop('prompt_number')

            with open(notebook, 'w') as f:
                write(nb, f, 'json')


class BuildNotes(Command):

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):

        import os
        import sys
        import shutil
        import tempfile

        from IPython.nbconvert.nbconvertapp import NbConvertApp

        self.reinitialize_command('run', inplace=True)
        self.run_command('run')

        for arg in range(len(sys.argv[1:])):
            sys.argv.pop(-1)

        if not os.path.exists(os.path.join('www', '_static')):
            os.mkdir(os.path.join('www', '_static'))

        # Now convert the lecture notes, problem sets, and practice problems to
        # HTML notebooks.

        app = NbConvertApp()
        app.initialize()
        app.export_format = 'html'
        for notebook in glob.glob('?.???/*.ipynb'):
            print("Rendering {0}...".format(notebook))
            app.notebooks = [notebook]
            app.output_base = os.path.join('www', '_static', os.path.basename(notebook.replace('.ipynb', '')))
            app.start()

        data_dir = os.path.join('www', '_static', 'data')
        if not os.path.exists(data_dir):
            os.mkdir(data_dir)


class DeployNotes(Command):

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):

        SERVER = os.environ["PY4SCI_SERVER"]
        USER = os.environ["PY4SCI_USER"]

        import getpass
        from ftplib import FTP
        from astropy.utils.console import ProgressBar

        ftp = FTP(SERVER)
        ftp.login(user=USER, passwd=getpass.getpass())

        for root, dirnames, filenames in os.walk('www/_build/html/'):

            print("Uploading files from {0}".format(root))

            ftp.cwd('/public_html/PY4SCI_WS_2015_16')
            for directory in root.split('/')[3:]:

                # Try and change to directory, make if not present
                try:
                    ftp.cwd(directory)
                except:
                    ftp.mkd(directory)
                    ftp.cwd(directory)

            for filename in ProgressBar(filenames):

                local_file = os.path.join(root, filename)

                try:
                    remote_size = ftp.size(filename)
                except:
                    remote_size = None

                local_size = os.path.getsize(local_file)

                if local_size != remote_size:
                    ftp.storbinary('STOR ' + filename, open(local_file, 'rb'))

        ftp.quit()


class RunNotes(Command):

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):

        # Now convert the lecture notes, problem sets, and practice problems to
        # HTML notebooks.

        from runipy.notebook_runner import NotebookRunner
        from IPython.nbformat.current import read, write

        start_dir = os.path.abspath('.')

        for notebook in glob.glob('?.???/*.ipynb'):
            print("Running {0}...".format(notebook))
            os.chdir(os.path.dirname(notebook))
            with open(os.path.basename(notebook)) as f:
                r = NotebookRunner(read(f, 'json'), pylab=False)
            r.run_notebook(skip_exceptions=True)
            with open(os.path.basename(notebook), 'w') as f:
                write(r.nb, f, 'json')
            os.chdir(start_dir)


setup(name='py4sci', cmdclass={'run':RunNotes, 'build': BuildNotes, 'deploy':DeployNotes, 'clear':ClearOutput, 'toc': BuildTOC})
