.PHONY: help
help: ## List commands
	@grep -E '^[a-zA-Z0-9][a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| sort \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "%-30s%s\n", $$1, $$2}'

.PHONY: build
build: ## Build the environment
	docker-compose build

.PHONY: run
run: ## up & run the environment
	docker-compose down && docker-compose up -d

.PHONY: down
down: ## turn down the environment
	docker-compose down
