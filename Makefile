
serve: build
	bundle exec jekyll serve

release: build
	bundle exec octopress deploy

build:
	bundle exec jekyll build
