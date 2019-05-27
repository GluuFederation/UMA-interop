


go: *.py
	-mkdir cgi-bin
	cp *.py cgi-bin/
	chmod -R 755 cgi-bin/*
	python -m CGIHTTPServer

curl:
	curl -v http://localhost:8000/cgi-bin/index.py

clean:
	rm -r cgi-bin/

.PHONY=go curl