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
import requests

action_client = ActionClient(Node("rest_api_interface"), RoboticTasks, "task_server")

UPLOAD_FOLDER = '/home/baggi/ws_ros2/src/point_cloud/resource'
ALLOWED_EXTENSIONS = {'pcd', 'ply'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET','POST'])
def upload_file():
    try:
        if request.method == 'POST':
            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # print("FILE IS BEING UPLOADED TO ", UPLOAD_FOLDER)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return '''
                        <!doctype html>
                        <title>Upload Point Cloud Data</title>
                        <h1>Successfully uploaded.</h1>
                        '''
    except Exception as err:
        return '''
                        <!doctype html>
                        <title>Upload Point Cloud Data</title>
                        <h1>Try again</h1>
                        '''
    return '''
    <!doctype html>
    <title>Upload Point Cloud Data</title>
    <h1>Upload Point Cloud Data</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''



@app.route("/welcome", methods=["GET"])
def welcome():
    #  Create a goal message
    goal = RoboticTasks.Goal()
    # goal.task_commands = "Activate the Robot"
    response_msg = "Welcome to the 4DiVision's Yaskawa Robot Arm Simulation!"
    # print(response_msg)
    return jsonify({'message': response_msg}), 200
UPLOAD_FOLDER

@app.route("/task", methods=["POST"])
def activate_task():
    try:
        # Get the task number from the JSON data sent by the client
        task_command = request.json.get('task_command')
        print(task_command)
        # Create a goal message with the received task number
        goal = RoboticTasks.Goal()
        goal.task_commands = task_command
        # Send the goal asynchronously to the task server using the action client
        action_client.send_goal_async(goal)
        response_msg = f"True"
        return jsonify({'message': response_msg}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


host_ip = "192.168.253.180";
if __name__ == "__main__":
    app.run(host=host_ip, debug=True)
