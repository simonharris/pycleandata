go:
	@python cleandata.py

cacheclean:
	rm -f _cache/*

dataclean:
	rm -rf cd_data/*

distclean: cacheclean dataclean
	rm -f cd_report.csv

init:
	git pull
	pip install -r requirements.txt
