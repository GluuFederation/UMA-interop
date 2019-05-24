


go: *.py
	-mkdir cgi-bin
	cp *.py cgi-bin/
	chmod 755 cgi-bin/*
	python -m CGIHTTPServer

curl:
	curl -v http://localhost:8000/cgi-bin/index.py


.PHONY=go curl