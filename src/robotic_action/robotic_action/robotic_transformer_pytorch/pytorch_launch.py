# robotic_transformer_pytorch/pytorch_launch.py
import torch
import numpy as np
from pathlib import Path
from  robotic_transformer_pytorch import MaxViT, RT1
import os
import sys
#################################################################################################3
###############################LAUNCHING THE MODEL#################################################3
###############################LAUNCHING THE MODEL#################################################3
###############################LAUNCHING THE MODEL#################################################3
###############################LAUNCHING THE MODEL#################################################3
#################################################################################################3

def launchPytorch(sampleVideo, instructionText):
    ACTION_LOWER_BOUND = -1
    ACTION_UPPER_BOUND = 1
    MODEL_PATH = os.path.join(sys.path[0])

    print(MODEL_PATH)
    # MODEL_PATH.mkdir(parents=True, exist_ok=True)
    MODEL_NAME = "/tr1_model1.pt"
    MODEL_SAVE_PATH = MODEL_PATH + MODEL_NAME
    print("Currecnt directory is : ", MODEL_PATH)
    print(f"TR-1 Model is loaded from {MODEL_SAVE_PATH}")
    vit = MaxViT(
        num_classes = 1000,
        dim_conv_stem = 64,
        dim = 96,
        dim_head = 32,
        depth = (2, 2, 5, 2),
        window_size = 7,
        mbconv_expansion_rate = 4,
        mbconv_shrinkage_rate = 0.25,
        dropout = 0.1
    )
    pytorchModel = RT1(
        vit = vit,
        num_actions = 6, # action dimension
        action_bins = 256, # action bins for continuous action space
        depth = 6,
        heads = 8,
        dim_head = 64,
        cond_drop_prob = 0.2)
    batch = 2
    frames = 1
    pytorchModel.load_state_dict(torch.load(f=MODEL_SAVE_PATH))
    # after much training
    pytorchModel.eval()
    eval_logits = pytorchModel(sampleVideo, instructionText, cond_scale = 3.) # classifier free guidance with conditional scale of 3
    actions = np.zeros(shape=(batch, frames, 6)) # (batch, frames, num_actions)
    for batch_id in range(batch):
        for frame_no in range(frames):
            current_logits = eval_logits[batch_id][frame_no] # evaluate for the current batch and frame
            action_bins = torch.argmax(current_logits, axis=-1)
            current_actions = np.interp(action_bins, [0,255], [ACTION_LOWER_BOUND,ACTION_UPPER_BOUND]) # convert discretized actions to actual actions
            actions[batch_id][frame_no] = current_actions
    print("HERE IS THE ROBOTIC SEQUENCES, ACCORDINGLY: ")
    print(actions) # (batch, frames)
    action_status = True
    return {'succeed': action_status, 
            "robotic_sequences": actions}


if __name__ == '__main__':
    launchPytorch()