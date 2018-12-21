build-ui-dev:
	npm run all:dev

build-ui-prod:
	npm run all:prod
	git add frontend/static
	git commit -m "Built frontend for prod release"

push-to-prod:
	git push dokku master

make-migrations:
	./manage.py makemigrations

run-migrations:
	./manage.py migrate

migrations: make-migrations run-migrations

build: migrations build-ui-dev

release: build-ui-prod push-to-prod

default: build
