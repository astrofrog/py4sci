OBJECTS =	*.ipynb

all:		$(OBJECTS)
		ipython nbconvert --to slides --config slides_config.py $(OBJECTS)
		ipython nbconvert --to html $(OBJECTS)

deploy:		$(OBJECTS)
		lftp $(PY4SCI_FTP_DETAILS) -e "mirror -R -i '\.(html?|css|js)$$' . public_html/notes/lectures"