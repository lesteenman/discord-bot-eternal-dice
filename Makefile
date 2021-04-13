BOT_DIR=discord_bot_eternal_dice
ERROR_HANDLER_DIR=error_handler
INFRA_DIR=infra

quality:
	cd ${BOT_DIR} && poetry run flake8 --config ../.flake8 ./tests ./discord_bot_eternal_dice ../error_handler
	cd ${INFRA_DIR} && poetry run flake8 --config ../.flake8 .

test: quality
	cd ${BOT_DIR} && poetry run pytest

clean:
	rm -rf ${BOT_DIR}/.serverless
	rm -rf ${ERROR_HANDLER_DIR}/.serverless

package:
	cd ${BOT_DIR} && npx serverless package
	cd ${ERROR_HANDLER_DIR} && npx serverless package

bootstrap: # Bootstraps an account for CDK deployments
	cd ${INFRA_DIR} && CDK_NEW_BOOTSTRAP=1 cdk bootstrap

deploy:
	cd ${INFRA_DIR} && cdk deploy

all: test build deploy
