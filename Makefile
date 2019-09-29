go:
	@python workhorse.py

clean:
	rm -f _cache/*

init:
	git pull
	pip install -r requirements.txt
