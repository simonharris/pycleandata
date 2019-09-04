go:
	@python workhorse.py

clean:
	rm -f _cache/*

init:
	git pull
	pip install -qr requirements.txt

