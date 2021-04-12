BOT_DIR=discord_bot_eternal_dice
ERROR_HANDLER_DIR=error_parser_function
INFRA_DIR=infra

quality:
	cd ${BOT_DIR} && poetry run flake8 --config ../.flake8 ./tests ./discord_bot_eternal_dice ../error_handler
	cd ${INFRA_DIR} && poetry run flake8 --config ../.flake8 .

test: quality
	cd ${BOT_DIR} && poetry run pytest

build:
	cd ${BOT_DIR} && serverless package
	cd ${ERROR_HANDLER_DIR} && serverless package

deploy:
	cd ${INFRA_DIR} && cdk deploy

all: test build deploy
