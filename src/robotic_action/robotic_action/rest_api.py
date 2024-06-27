#!/usr/bin/env python3 
from flask import Flask, request, jsonify, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from robotic_msgs.action import RoboticTasks
import rclpy
from rclpy.node import Node
import threading
import os
threading.Thread(target=lambda: rclpy.init()).start()
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient

# Implementation of Pytorch
import robotic_action.robotic_transformer_pytorch.pytorch_launch as pytorchLaunch

import numpy as np




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
# UPLOAD_FOLDER

@app.route("/task", methods=["POST"])
def activate_task():
    try:

        
        task_command = request.json.get('task_command') 
        # Create a goal message with the received task number
        # goal = RoboticTasks.Goal()
        result_action = pytorchLaunch.launchPytorch(
            sampleVideo=video,
            instructionText=task_command
        )
        print(task_command)
        
        # goal.task_sequences = task_command
        # Send the goal asynchronously to the task server using the action client
        # action_client.send_goal_async(goal)
        response_msg = {'message': task_command}
        return jsonify(result_action), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


host_ip = "192.168.253.180"
if __name__ == "__main__":
    app.run(host=host_ip, debug=True)
