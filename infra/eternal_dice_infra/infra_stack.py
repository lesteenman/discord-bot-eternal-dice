from aws_cdk import (core, aws_lambda, aws_apigateway, aws_dynamodb, aws_sns, aws_logs, aws_logs_destinations)
from aws_cdk.aws_dynamodb import ITable
from aws_cdk.aws_lambda import Function
from aws_cdk.aws_sns import Topic

from eternal_dice_infra import config


class InfraStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.config = config.config
        self.create_discord_slash_commands()
        self.discord_bot_handler = self.create_app_handler()
        self.create_api()
        self.create_error_handler()

    def create_table(self) -> aws_dynamodb.ITable:
        partition_key = aws_dynamodb.Attribute(
            name="pk",
            type=aws_dynamodb.AttributeType.STRING
        )

        sort_key = aws_dynamodb.Attribute(
            name="sk",
            type=aws_dynamodb.AttributeType.STRING
        )

        return aws_dynamodb.Table(self, "EternalGuessesTable",
                                  partition_key=partition_key,
                                  sort_key=sort_key,
                                  billing_mode=aws_dynamodb.BillingMode.PAY_PER_REQUEST
                                  )

    def create_app_handler(self) -> Function:
        environment = {
            'DISCORD_PUBLIC_KEY': self.config['DISCORD_PUBLIC_KEY'],
            'DISCORD_BOT_TOKEN': self.config['DISCORD_BOT_TOKEN'],
            'LOGURU_LEVEL': self.config['APP_LOG_LEVEL'],
        }

        return aws_lambda.Function(self, "DiscordAppFunction",
                                   runtime=aws_lambda.Runtime.PYTHON_3_8,
                                   timeout=core.Duration.seconds(10),
                                   memory_size=1024,
                                   code=aws_lambda.Code.from_asset("../discord_app/.serverless/discord-app.zip"),
                                   handler="eternal_guesses.handler.handle_lambda",
                                   environment=environment
                                   )

    def grant_table_readwrite_permissions(self, dynamodb_table: ITable, function: Function):
        dynamodb_table.grant_full_access(function)
        # dynamodb_table.grant(function, "dynamodb:DescribeTable")

    def create_api(self):
        api = aws_apigateway.RestApi(self, "eternal-guesses-api",
                                     rest_api_name="Eternal Guesses API")
        discord_app_integration = aws_apigateway.LambdaIntegration(self.discord_bot_handler)
        discord_resource = api.root.add_resource("discord")
        discord_resource.add_method("POST", discord_app_integration)

    def create_error_handler(self) -> None:
        app_errors_sns_topic = self.create_sns_topic()
        cloudwatch_logs_handler = self.create_logs_handler(app_errors_sns_topic)

        self.subscribe_handler_to_function_logs(self.discord_bot_handler, cloudwatch_logs_handler)
        self.subscribe_emails_to_topic(app_errors_sns_topic, self.config['NOTIFICATION_EMAIL'])

    def create_sns_topic(self) -> Topic:
        sns_topic = aws_sns.Topic(self, "eternal-guess-error-topic")
        return sns_topic

    def subscribe_emails_to_topic(self, sns_topic: Topic, email_address: str) -> None:
        aws_sns.Subscription(self, "eternal-guess-error-subscription",
                             topic=sns_topic,
                             protocol=aws_sns.SubscriptionProtocol.EMAIL,
                             endpoint=email_address)

    def create_logs_handler(self, topic: Topic) -> Function:
        code_asset = aws_lambda.Code.from_asset("../error_parser_function/.serverless/error-parser.zip")
        environment = {
            'snsARN': topic.topic_arn,
        }

        logs_handler = aws_lambda.Function(self, "eternal-guess-logs-parser",
                                           runtime=aws_lambda.Runtime.PYTHON_3_7,
                                           code=code_asset,
                                           handler="parser.lambda_handler",
                                           environment=environment)

        topic.grant_publish(logs_handler)

        return logs_handler

    def subscribe_handler_to_function_logs(self, app_handler, logs_handler):
        aws_logs.SubscriptionFilter(self, "eternal-guess-handler-subscription-filter",
                                    log_group=app_handler.log_group,
                                    destination=aws_logs_destinations.LambdaDestination(logs_handler),
                                    filter_pattern=aws_logs.FilterPattern.any_term("ERROR", "WARNING"))

    def create_discord_slash_commands(self):
        pass
