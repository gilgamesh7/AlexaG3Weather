# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.

# BeautifulSoup : https://www.dataquest.io/blog/web-scraping-tutorial-python/

import logging
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

from datetime import datetime
import pytz
import requests
import json
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def getWeather(period):
    logger.info("In getWeather function,Time invoked : {datetime.now().hour}")

    metserviceURL="https://services.metservice.com/weather-widget/widget?loc=north-shore"
    metserviceHeaders={'Accept': 'application/html'}
    metserviceResponse=requests.get(metserviceURL,headers=metserviceHeaders)
    logger.info(f"Returned : {metserviceResponse.status_code}")

    soup = BeautifulSoup(metserviceResponse.content, 'html.parser')
    # logger.info(f"{soup.prettify()}")
    allInformation = soup.find_all('span')
    # logger.info(allInformation)
    
    warning = f"Warnings. {allInformation[1].get_text()}."

    todaysDate = f"For {allInformation[2].get_text()}."
    todaysHigh = f"High. {allInformation[4].get_text()}."
    todaysLow = f"Low. {allInformation[5].get_text()}."
    todaysInfo = f"Forecast. {allInformation[3].get_text()}."
    
    tomorrowsDate = f"For {allInformation[6].get_text()}."
    tomorrowsHigh = f"High. {allInformation[8].get_text()}."
    tomorrowsLow = f"Low. {allInformation[9].get_text()}."
    tomorrowsInfo = f"Forecast. {allInformation[7].get_text()}."

    day3Date = f"For {allInformation[10].get_text()}."
    day3High = f"High. {allInformation[12].get_text()}."
    day3Low = f"Low. {allInformation[13].get_text()}."
    day3Info = f"Forecast. {allInformation[11].get_text()}."

    if period == 'Today':
        weatherInfo = f"{todaysDate} {warning} {todaysHigh} {todaysLow} {todaysInfo}"
    elif period == 'Tomorrow':
        weatherInfo = f"{tomorrowsDate} {warning} {tomorrowsHigh} {tomorrowsLow} {tomorrowsInfo}"
    else:
        weatherInfo = f"{day3Date} {warning} {day3High} {day3Low} {day3Info}"
        
    
    return f"{weatherInfo}. Would you like another day ?"


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        if (datetime.now(pytz.timezone('Pacific/Auckland')).hour >= 15):
            welcome = "Bon Soir"
        else:
            welcome = "Bon jour"
        speak_output = f"{welcome}, Gayathri ! you can say Today, Tomorrow or Day After Tomorrow. Which forecast do you want?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# Start custom handlers

class TodaysWeatherHandler(AbstractRequestHandler):
    def can_handle(self,handler_input):
        return ask_utils.is_intent_name("TodaysWeather")(handler_input)
        
    def handle(self, handler_input):
        logger.info(f"Return from function : {getWeather('Today')}")
        
        speak_output = f"{getWeather('Today')}"
        
        return(
            handler_input.response_builder
                .speak(speak_output)
                .ask("Would you like to know more weather, Gayathri ?")
                .response
            )

class TomorrowsWeatherHandler(AbstractRequestHandler):
    def can_handle(self,handler_input):
        return ask_utils.is_intent_name("TomorrowsWeather")(handler_input)
        
    def handle(self, handler_input):
        logger.info(f"Return from function : {getWeather('Tomorrow')}")
        
        speak_output = f"{getWeather('Tomorrow')}"
        
        return(
            handler_input.response_builder
                .speak(speak_output)
                .ask("Would you like to know more weather, Gayathri ?")
                .response
            )

class DayAfterTomorrowsWeatherHandler(AbstractRequestHandler):
    def can_handle(self,handler_input):
        return ask_utils.is_intent_name("DayAfterTomorrowsWeather")(handler_input)
        
    def handle(self, handler_input):
        logger.info(f"Return from function : {getWeather('DayAfterTomorrow')}")
        
        speak_output = f"{getWeather('DayAfterTomorrow')}"
        
        return(
            handler_input.response_builder
                .speak(speak_output)
                .ask("Would you like to know more weather, Gayathri ?")
                .response
            )

# End custom handlers

class HelloWorldIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("HelloWorldIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        # speak_output = "Hello World!"
        if (datetime.now(pytz.timezone('Pacific/Auckland')).hour >= 15):
            welcome = "Bon Soir"
        else:
            welcome = "Bon jour"
        speak_output = f"{welcome}, Gayathri ! you can say Today, Tomorrow or Day After Tomorrow. Which forecast do you want?"
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "you can say Today for today's weather, Tomorrow for tomorrow's weather or All for 3 days weather! How can I help?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Have a wonderful  day , Gayathri !"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(TodaysWeatherHandler())
sb.add_request_handler(TomorrowsWeatherHandler())
sb.add_request_handler(DayAfterTomorrowsWeatherHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(HelloWorldIntentHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
