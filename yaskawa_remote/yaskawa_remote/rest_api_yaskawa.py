#!/usr/bin/env python3 
from flask import Flask, request, jsonify
from yaskawa_msgs.action import YaskawaTasks
import rclpy
from rclpy.node import Node
import threading

threading.Thread(target=lambda: rclpy.init()).start()
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
import requests
action_client = ActionClient(Node("rest_api_interface"), YaskawaTasks, "task_server")

app = Flask(__name__)

@app.route("/welcome", methods=["GET"])
def welcome():
    #  Create a goal message
    goal = YaskawaTasks.Goal()
    goal.task_number = 1
    # response_msg= action_client.send_goal_async(goal)
    # print(response_msg)
    response_msg = "Welcome to the 4DiVision's Yaskawa Robot Arm Simulation!"
    # print(task_number)
    return jsonify({'message': response_msg}), 200

@app.route("/activate", methods=["GET"])
def activate():
    #  Create a goal message
    goal = YaskawaTasks.Goal()
    goal.task_number = 1
    response_msg= action_client.send_goal_async(goal)
    print(response_msg)
    response_msg = "Yaskawa Robot is getting ready "
    # print(task_number)
    return jsonify({'message': response_msg}), 200


@app.route("/shutdown", methods=["GET"])
def shutdown():
     #  Create a goal message
    goal = YaskawaTasks.Goal()
    goal.task_number = 1
    # response_msg= action_client.send_goal_async(goal)
    # print(response_msg)
    response_msg = "Robot shutdown successfully"
    # print(task_number)
    return jsonify({'message': response_msg}), 200

@app.route("/task", methods=["POST"])
def activate_task():
    try:
        # Get the task number from the JSON data sent by the client
        task_number = request.json.get('task_number')
        print(task_number)
        # Create a goal message with the received task number
        goal = YaskawaTasks.Goal()
        goal.task_number = task_number

        # Send the goal asynchronously to the task server using the action client
        action_client.send_goal_async(goal)

        response_msg = f"Task {task_number} activated"
        return jsonify({'message': response_msg}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(host="192.168.10.109", debug=True)
