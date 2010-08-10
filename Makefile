.PHONY: test cover cover_html
test:
	/cygdrive/C/Python26/Scripts/coverage.exe run --rcfile=.coverage.ini tests/unittest_all.py

cover: 
	/cygdrive/C/Python26/Scripts/coverage.exe report --rcfile=.coverage.ini 

cover_html: cover
	/cygdrive/C/Python26/Scripts/coverage.exe html --rcfile=.coverage.ini 

