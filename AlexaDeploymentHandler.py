from __future__ import print_function
import json
import markovify
import os

from AlexaBaseHandler import AlexaBaseHandler


class AlexaDeploymentHandler(AlexaBaseHandler):
    def __init__(self, model):
        super(self.__class__, self).__init__()
        self.model = model

    def on_processing_error(self, event, context, exc):
        print("on_processing_error", event, context, exc)

    def on_session_started(self, session_started_request, session):
        print("on_session_started")

    def on_launch(self, launch_request, session):
        print("on_launch")

        return self.get_welcome_response()

    def on_session_ended(self, session_ended_request, session):
        session_attributes = {}
        speech_output = "Exiting."
        reprompt_text = None
        should_end_session = True

        speechlet = self._build_speechlet_response_without_card(speech_output, reprompt_text, should_end_session)

        return self._build_response(session_attributes, speechlet)

    def on_intent(self, intent_request, session):
        """
        Handles "IntentRequest".
        Args:
            intent_request (dict): from Alexa
            session (dict): from Alexa
        Returns:
            (func): handle functions corresponding to intent
        Raises:
            ValueError: when intent is not supported
        """
        intent_name = intent_request['intent']['name']
        print('Intent: ' + str(intent_name))

        # Dispatch to skill's intent handlers
        if intent_name == "GenerateIdea":
            return self.handle_generate_idea(intent_request, session)
        # elif intent_name == "RepeatRepo":
        #     return self.handle_repeat_repo(intent_request, session)
        # elif intent_name == "FeelingLucky":
        #     return self.handle_feeling_lucky(intent_request, session)
        elif intent_name == "AMAZON.HelpIntent":
            return self.handle_help_response()
        # elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        #     return self.handle_session_end_request()
        else:
            raise ValueError("Invalid intent")

    def get_welcome_response(self):
        """
        Welcome response. Repeats speech if user does not reply.
        Returns:
            _build_response: passed to Alexa
        """
        session_attributes = {}
        card_title = "Welcome"
        card_output = "Welcome to Hack Generate. " \
                      "Try asking me to generate a hackathon idea."
        speech_output = card_output
        reprompt_text = "I didn't catch that. " \
                        "Try asking me to generate a hackathon idea."
        should_end_session = False

        speechlet = self._build_speechlet_response(card_title, card_output, speech_output, reprompt_text, should_end_session)

        return self._build_response(session_attributes, speechlet)

    def handle_help_response(self):
        """
        intent: "AMAZON.HelpIntent"
        Provides help and examples.
        Returns:
            _build_response: passed to Alexa
        """
        session_attributes = {}
        card_title = "What is HackGenerate?"
        card_output = \
            "HackGenerate generates random hackathon ideas!" \
            "For example, try asking me, Alexa give me a random hackathon idea. \n"
        speech_output = \
            'Hack Generate generates random hackathon ideas!' \
            "For example, try asking me, Alexa give me a random hackathon idea. \n"
        reprompt_text = "Check your Alexa app for more examples."
        should_end_session = False

        speechlet = self._build_speechlet_ssml(card_title, card_output, speech_output, reprompt_text, should_end_session)

        return self._build_response(session_attributes, speechlet)

    def handle_session_end_request(self):
        """
        intent: "AMAZON.CancelIntent" or "AMAZON.StopIntent"
        Ends session.
        Returns:
             _build_response: passed to Alexa
        """
        session_attributes = {}
        speech_output = "Exiting HackGenerate."
        reprompt_text = None
        should_end_session = True

        speechlet = self._build_speechlet_response_without_card(speech_output, reprompt_text, should_end_session)

        return self._build_response(session_attributes, speechlet)

    def handle_generate_idea(self, intent_request, session):
        """
        intent: "GenerateIdea"
        Args:
            intent_request (dict): from Alexa
            session (dict): from Alexa
        Returns:
            create_repo_response: speechlet response
        """
        print(intent_request)

        pitch = self.model.make_short_sentence(140)


        session_attributes = {'idea': pitch}
        card_title = "Hackathon Idea"
        card_output = pitch
        speech_output = pitch
        reprompt_text = "Your hackathon idea can be found in your Alexa app."
        should_end_session = True

        speechlet = self._build_speechlet_response(card_title, card_output, speech_output, reprompt_text, should_end_session)

        return self._build_response(session_attributes, speechlet)
