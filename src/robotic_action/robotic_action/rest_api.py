#!/usr/bin/env python3 
from flask import Flask, request, jsonify, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from robotic_msgs.action import RoboticTasks
import rclpy
from rclpy.node import Node
import threading
import os

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient

# Implementation of Pytorch
from robotic_transformer_pytorch import pytorch_launch as pytorchLaunch
# import robotic_action.robotic_action.robotic_transformer_pytorch.pytorch_launch as pytorchLaunch

threading.Thread(target=lambda: rclpy.init()).start()

#################################################################################################3
###############################LAUNCHING THE MODEL#################################################3
###############################LAUNCHING THE MODEL#################################################3
###############################LAUNCHING THE MODEL#################################################3
###############################LAUNCHING THE MODEL#################################################3
#################################################################################################3


#Dummy Video Data
import torch
batch = 2
frames = 1
video = torch.randn(batch, 3, frames, 224, 224) # (batch, channels, frames, height, width)
action_client = ActionClient(Node("rest_api_interface"), RoboticTasks, "task_server")
app = Flask(__name__)
@app.route("/welcome", methods=["GET"])
def welcome():
    #  Create a goal message
    # goal.task_commands = "Activate the Robot"
    response_msg = "Welcome to the 4DiVision's Yaskawa Robot Arm Simulation!"
    # print(response_msg)
    return jsonify({'message': response_msg}), 200


@app.route("/task", methods=["POST"])
def activate_task():
       
    task_command = request.json.get('task_command') 
    # Create a goal message with the received task number
    goal = RoboticTasks.Goal()
    result_action = pytorchLaunch.launchPytorch(
        sampleVideo=video,
        instructionText=task_command
    )
    print("HERE RT-1 RESULTS: ")
    
    area_result = []
 
    for sublist in result_action:
        area_result.append(sublist[0])
        # print(command)
        # goal.task_number = area_result
    # Send the goal asynchronously to the task server using the action client
    # action_client.send_goal_async(goal)
    # response_msg = {'message': result_action}
    return jsonify(str(area_result)), 200
    # return "succeed"
\


host_ip = "192.168.255.238"
if __name__ == "__main__":
    app.run(host="localhost", debug=True)
