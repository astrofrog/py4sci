OBJECTS =	*.ipynb

all:		$(OBJECTS)
		ipython nbconvert --to slides --config slides_config.py $(OBJECTS)
		ipython nbconvert --to html $(OBJECTS)

deploy:
		lftp ftp://$(PY4SCI_USER)@$(PY4SCI_SERVER) -e "mirror -R -i '\.(html?|css|js)$$' . public_html/notes/lectures"