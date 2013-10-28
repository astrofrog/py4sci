#!/usr/bin/env python

import os
import glob

from setuptools import setup, Command


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

        # Make an index of all notes
        f = open('index.html', 'w')
        f.write("<html>\n  <body>\n")

        f.write("    <h1>Lectures:</h1>\n")
        f.write("    <ul>\n")
        for page in glob.glob('lectures/*.html'):
            f.write('      <li><a href="{0}">{1}</a></li>\n'.format(page, os.path.basename(page).replace('.html', '')))
        f.write('    </ul>\n')

        f.write("    <h1>Problem Sets:</h1>\n")
        f.write("    <ul>\n")
        for page in glob.glob('problems/*.html'):
            f.write('      <li><a href="{0}">{1}</a></li>\n'.format(page, os.path.basename(page).replace('.html', '')))
        f.write('    </ul>\n')

        f.write("    <h1>Practice Sheets:</h1>\n")
        f.write("    <ul>\n")
        for page in glob.glob('practice/*.html'):
            f.write('      <li><a href="{0}">{1}</a></li>\n'.format(page, os.path.basename(page).replace('.html', '')))
        f.write('    </ul>\n')

        f.write('  </body>\n</html>')
        f.close()

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

        for slides in ProgressBar.iterate(glob.glob('lectures/*.html')
                                          + ['lectures/custom.css']
                                          + glob.glob('problems/*.html')
                                          + glob.glob('problems/*.txt')
                                          + glob.glob('problems/*.fasta')
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
            os.chdir(os.path.dirname(notebook))
            r = NotebookRunner(os.path.basename(notebook))
            r.run_notebook(skip_exceptions=True)
            r.save_notebook(os.path.basename(notebook))
            os.chdir(start_dir)


setup(name='py4sci', cmdclass={'run':RunNotes, 'build': BuildNotes, 'deploy':DeployNotes})
