#!/usr/bin/env python3 
from flask import Flask
from ask_sdk_core.skill_builder import SkillBuilder
from flask_ask_sdk.skill_adapter import SkillAdapter
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from ask_sdk_model.ui import SimpleCard
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from robotic_msgs.action import YaskawaTasks
import threading
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
import time

threading.Thread(target=lambda: rclpy.init()).start()

action_client = ActionClient(Node("alexa_interface"), YaskawaTasks, "task_server")

app = Flask(__name__)

class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Welcome to the 4DiVision's Robotic Systems, how can help you!"
        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Hello HUMAN being?? ", speech_text)).set_should_end_session(
            False)
        # goal = YaskawaTasks.Goal()
        # goal.task_number = 0
        # action_client.send_goal_async(goal)
        return handler_input.response_builder.response


# startintend 
# commands:

# Hi robot 
# Hi yaskawa
# wake up
# start yaskawa


class GraspIntendHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("graspIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Okey, I am grasping the object now. wait a little bit"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("it is a YASKAWA ROBOT ARM", speech_text)).set_should_end_session(
            True)
        
        goal = YaskawaTasks.Goal()
        goal.task_number = 2
        action_client.send_goal_async(goal)
        return handler_input.response_builder.response 
    



# pickup the object
# lift up
# lift up the object
# pickup


class PickIntendHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("pickIntend")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Okey, I am moving to pick the object"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Pick", speech_text)).set_should_end_session(
            True)
        goal = YaskawaTasks.Goal()
        goal.task_number = 2.0
        print("", goal)
        action_client.send_goal_async(goal)
        return handler_input.response_builder.response 


class PlaceIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("placeIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Okay, i am placing the object into different location. wait a second. "

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Sleep", speech_text)).set_should_end_session(
            True)
        goal = YaskawaTasks.Goal()
        goal.task_number = 3
        action_client.send_goal_async(goal)
        return handler_input.response_builder.response 

class WakeIntendHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("WakepIntend")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Ok, I am ready"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Wake", speech_text)).set_should_end_session(
            True)
        goal = YaskawaTasks.Goal()
        goal.task_number = 0
        action_client.send_goal_async(goal)
        return handler_input.response_builder.response 


class AllExceptionHandler(AbstractExceptionHandler):

    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        # Log the exception in CloudWatch Logs
        print(exception)

        speech = "Sorry, I didn't get it. could you repeat! it is 4Division Robotic System"
        handler_input.response_builder.speak(speech).ask(speech)
        return handler_input.response_builder.response


skill_builder = SkillBuilder()
skill_builder.add_request_handler(LaunchRequestHandler())
skill_builder.add_request_handler(GraspIntendHandler())
skill_builder.add_request_handler(PickIntendHandler())
skill_builder.add_request_handler(PlaceIntentHandler())
skill_builder.add_exception_handler(AllExceptionHandler())
# Register your intent handlers to the skill_builder object

skill_adapter = SkillAdapter(
    skill=skill_builder.create(), skill_id="amzn1.ask.skill.e9863545-84fb-4434-bec8-7fd238c75279", app=app)

@app.route("/")
def invoke_skill():
    return skill_adapter.dispatch_request()



skill_adapter.register(app=app,route="/")

if __name__ == "__main__":
    app.run(host= "0.0.0.0", port=8080)