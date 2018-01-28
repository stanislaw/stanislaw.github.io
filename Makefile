# Self-Documented Makefile
# http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
.PHONY: help
help: ## Show this help message.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

preview: build ## Run preview server
	bundle exec jekyll serve --watch

draft: build ## Run preview server with drafts included
	bundle exec jekyll serve --watch --draft

deploy: clean build ## Deploy
	bundle exec octopress deploy

build: ## Build
	bundle exec jekyll build

clean: ## Clean _site folder
	rm -rfv _site

