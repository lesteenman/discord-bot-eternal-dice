#!/usr/bin/env python3

from aws_cdk import core

from eternal_dice_infra.infra_stack import InfraStack


app = core.App()
InfraStack(app, "discord-bot-eternal-dice")

app.synth()
