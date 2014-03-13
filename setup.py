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

class LiveVersion(Command):

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):

        if os.path.exists('live_version'):
            shutil.rmtree('live_version')
        os.mkdir('live_version')

        from IPython.nbformat.current import read, write

        for notebook in (glob.glob('lectures/*.ipynb')
                        + glob.glob('problems/*.ipynb')
                        + glob.glob('practice/*.ipynb')):

            with open(notebook, 'r') as f:
                nb = read(f, 'json')

            for ws in nb.worksheets:
                for cell in ws.cells:
                    if cell.cell_type == 'code':
                        cell.outputs = []

            with open(os.path.join('live_version', os.path.basename(notebook)), 'w') as f:
                write(nb, f, 'json')


class BuildNotes(Command):

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):

        import os
        import shutil
        import tempfile

        from IPython.nbconvert.nbconvertapp import NbConvertApp

        import sys
        for arg in range(len(sys.argv[1:])):
            sys.argv.pop(-1)

        # First convert the lecture notes to slides - we have to do them
        # individually in order to be able to specify a custom output prefix for
        # each.

        app = NbConvertApp()
        app.initialize()
        app.export_format = 'slides'
        app.config.Exporter.template_file = 'lectures/py4sci_template.tpl'
        for notebook in glob.glob('lectures/*.ipynb'):
            app.notebooks = [notebook]
            app.output_base = os.path.join('www', '_static', os.path.basename(notebook.replace('.ipynb', '')))
            app.start()

        # Now convert the lecture notes, problem sets, and practice problems to
        # HTML notebooks.

        app = NbConvertApp()
        app.initialize()
        app.export_format = 'html'
        for notebook in (glob.glob('lectures/*.ipynb')
                        + glob.glob('problems/*.ipynb')
                        + glob.glob('practice/*.ipynb')):
            app.notebooks = [notebook]
            app.output_base = os.path.join('www', '_static', os.path.basename(notebook.replace('.ipynb', '')))
            app.start()


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

        ftp.cwd('/public_html/PY4SCI_WS_2013_14')

        for slides in ProgressBar.iterate(glob.glob('lectures/data/*')
                                          + glob.glob('lectures/*.html')
                                          + ['lectures/custom.css']
                                          + glob.glob('problems/data/*')
                                          + glob.glob('problems/*.html')
                                          + glob.glob('practice/data/*')
                                          + glob.glob('practice/*.html')):
            try:
                remote_size = ftp.size(slides)
            except:
                remote_size = None
            local_size = os.path.getsize(slides)
            if local_size != remote_size:
                ftp.storbinary('STOR ' + slides, open(slides, 'rb'))

        ftp.storbinary('STOR index.html', open('index.html', 'rb'))

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

        start_dir = os.path.abspath('.')

        for notebook in (glob.glob('lectures/*.ipynb')
                        + glob.glob('problems/*.ipynb')
                        + glob.glob('practice/*.ipynb')):
            if "Understanding" in notebook:
                continue
            os.chdir(os.path.dirname(notebook))
            r = NotebookRunner(os.path.basename(notebook), pylab=True)
            r.run_notebook(skip_exceptions=True)
            r.save_notebook(os.path.basename(notebook))
            os.chdir(start_dir)


setup(name='py4sci', cmdclass={'run':RunNotes, 'build': BuildNotes, 'deploy':DeployNotes, 'live':LiveVersion, 'toc': BuildTOC})
