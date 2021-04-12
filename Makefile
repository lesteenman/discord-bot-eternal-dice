BOT_DIR=discord_bot_eternal_dice
ERROR_HANDLER_DIR=error_handler
INFRA_DIR=infra

quality:
	cd ${BOT_DIR} && poetry run flake8 --config ../.flake8 ./tests ./discord_bot_eternal_dice ../error_handler
	cd ${INFRA_DIR} && poetry run flake8 --config ../.flake8 .

test: quality
	cd ${BOT_DIR} && poetry run pytest

clean:
	rm -rf ${BOT_DIR}/.build
	rm -rf ${ERROR_HANDLER_DIR}/.build

package:
	cd ${BOT_DIR} && \
		mkdir -p .build/bundle || true && \
		cp -r discord_bot_eternal_dice .build/bundle/ && \
		poetry export -f requirements.txt --without-hashes > .build/requirements.txt && \
		pip install -r .build/requirements.txt -t .build/bundle/ && \
		rm .build/discord_bot_eternal_dice.zip && \
		cd .build/bundle/ && \
		zip --verbose ../discord_bot_eternal_dice.zip *

	cd ${ERROR_HANDLER_DIR} && \
		mkdir .build || true && \
		zip .build/error_handler.zip parser.py

bootstrap: # Bootstraps an account for CDK deployments
	cd ${INFRA_DIR} && CDK_NEW_BOOTSTRAP=1 cdk bootstrap

deploy:
	cd ${INFRA_DIR} && cdk deploy

all: test build deploy
