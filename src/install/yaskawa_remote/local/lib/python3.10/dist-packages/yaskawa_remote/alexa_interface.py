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
from yaskawa_msgs.action import YaskawaTasks
import threading

threading.Thread(target=lambda: rclpy.init()).start()
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient

action_client = ActionClient(Node("alexa_interface"), YaskawaTasks, "task_server")

app = Flask(__name__)

skill_builder = SkillBuilder()

class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Welcome to the 4DiVision's Yaskawa Robot Arm Simulation, how can help you!"
        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Hello World", speech_text)).set_should_end_session(
            False)
        goal = YaskawaTasks.Goal()
        goal.task_number = 0
        action_client.send_goal_async(goal)
        return handler_input.response_builder.response

class PickIntendHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("PickIntend")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Ok, I am moving to take that"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Pick", speech_text)).set_should_end_session(
            True)
        goal = YaskawaTasks.Goal()
        goal.task_number = 1
        action_client.send_goal_async(goal)
        return handler_input.response_builder.response 
    

class SleepIntendHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("SleepIntend")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Ok, See later"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Sleep", speech_text)).set_should_end_session(
            True)
        goal = YaskawaTasks.Goal()
        goal.task_number = 2
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

        speech = "Sorry, I didn't get it. could you repeat!"
        handler_input.response_builder.speak(speech).ask(speech)
        return handler_input.response_builder.response


skill_builder =SkillBuilder()
skill_builder.add_request_handler(LaunchRequestHandler())
skill_builder.add_request_handler(PickIntendHandler())
skill_builder.add_request_handler(SleepIntendHandler())
skill_builder.add_request_handler(WakeIntendHandler())
skill_builder.add_exception_handler(AllExceptionHandler())
# Register your intent handlers to the skill_builder object

skill_adapter = SkillAdapter(
    skill=skill_builder.create(), skill_id="amzn1.ask.skill.b305aa81-f558-483c-8d76-9ef9f4fb991b", app=app)

@app.route("/")
def invoke_skill():
    return skill_adapter.dispatch_request()



skill_adapter.register(app=app,route="/")

if __name__ == "__main__":
    app.run()