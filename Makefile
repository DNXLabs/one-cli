export JEKYLL_VERSION=4.0


run:
	docker run --rm \
		--volume $(PWD):/srv/jekyll \
		-p 4000:4000 \
		-it jekyll/jekyll:$(JEKYLL_VERSION) \
		jekyll serve --incremental

build:
	docker run --rm \
		--volume $(PWD):/srv/jekyll \
		-it jekyll/jekyll:$(JEKYLL_VERSION) \
		jekyll build

update:
	docker run --rm \
		--volume $(PWD):/srv/jekyll \
		-it jekyll/jekyll:$(JEKYLL_VERSION) \
		bundle update
