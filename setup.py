#!/usr/bin/env python

import os
import glob

from setuptools import setup, Command

SERVER = os.environ["PY4SCI_SERVER"]
USER = os.environ["PY4SCI_USER"]

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

        # First convert the lecture notes to slides - we have to do them
        # individually in order to be able to specify a custom output prefix for
        # each.

        app = NbConvertApp()
        app.initialize()
        app.export_format = 'slides'
        app.template_file = 'lectures/py4sci_template.tpl'
        for notebook in glob.glob('lectures/*.ipynb'):
            app.notebooks = [notebook]
            app.output_base = notebook.replace('.ipynb', '')
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
            app.output_base = notebook.replace('.ipynb', '')
            app.start()

class DeployNotes(Command):

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):

        import getpass
        from ftplib import FTP
        from astropy.utils.console import ProgressBar

        ftp = FTP(SERVER)
        ftp.login(user=USER, passwd=getpass.getpass())

        ftp.cwd('/public_html/PY4SCI_WS_2013_14')

        for slides in ProgressBar.iterate(glob.glob('lectures/*.html')
                                          + glob.glob('problems/*.html')
                                          + glob.glob('practice/*.html')):
            ftp.storbinary('STOR ' + slides, open(slides, 'rb'))

        ftp.quit()


setup(name='py4sci', cmdclass={'build': BuildNotes, 'deploy':DeployNotes})
