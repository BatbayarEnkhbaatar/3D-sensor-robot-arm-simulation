#!/usr/bin/env python3
from flask import Flask, request, jsonify
import logging
import load_policy
import json
import ast
import numpy as np
# Initialize Flask application
app = Flask(__name__)




@app.route("/welcome", methods=["GET"])
def welcome():
    response_msg = "Welcome to the 4DiVision's Yaskawa Robot Arm Simulation!"
    logging.info("Welcome message sent")
    return jsonify({'message': response_msg}), 200

@app.route("/command", methods=["POST"])
def activate_task():

    input_data = request.get_json()

    command_intext = input_data.get("text") 
    frames_path_str = input_data.get("frames_path")

    # terminate_episode = [0,0,0]
    # while not np.array_equal(terminate_episode, np.array([1, 1, 1])):
        
    frames_path_list = ast.literal_eval(frames_path_str)
    # print("Instruction: ",command_intext)
    # print("Observed Frames from the sensor:")
    [print(path) for path in frames_path_list]  
    actions = load_policy.main(policy, embed, frames_path_list, command_intext)
    action_six_dim = np.concatenate((actions['world_vector'],actions['rotation_delta']))
    terminal_episode = actions["terminate_episode"]
    # print("actions_6dof:= ", action_six_dim)
    # print("terminate_episode:= ", terminal_eposide)
    # Prepare JSON-serializable data
    data_serializable =  [
        {"action_six_dim": action_six_dim.tolist()},
        {"gripper_action": " "},
        {"ter_ep_val": terminal_episode.tolist()}
        ]
    
    return jsonify(data_serializable)

if __name__ == "__main__":
    # Run Flask application on localhost with debug mode enabled
    policy, embed = load_policy.load_check_points()
    app.run(host="127.0.0.1", port=5000, debug=True)
