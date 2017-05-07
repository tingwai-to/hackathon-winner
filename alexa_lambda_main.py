from __future__ import print_function
import logging
import json
import markovify

from AlexaDeploymentHandler import AlexaDeploymentHandler


"""
Main entry point for the Lambda function.
Handler: alex_lambda_min.lambda_handler
Role: lambda_basic_execution
"""

logger = logging.getLogger()
logger.setLevel(logging.INFO)


with open('markov.json', 'r') as f:
    model_json = json.load(f)

model = markovify.Text.from_json(model_json)
alexa = AlexaDeploymentHandler(model)


def lambda_handler(event, context):
    logging.info("Executing lambda_handler for HackGenerate")

    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.ask.skill.34319689-021b-40c8-b323-1475fcdccc3b"):
    #     raise ValueError("Invalid Application ID")


    alexa_response = alexa.process_request(event, context)

    return alexa_response