
preview: build
	bundle exec jekyll serve --watch

deploy: build
	bundle exec octopress deploy

build:
	bundle exec jekyll build
