
preview: build
	bundle exec jekyll serve

deploy: build
	bundle exec octopress deploy

build:
	bundle exec jekyll build
