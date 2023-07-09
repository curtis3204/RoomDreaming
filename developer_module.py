import gradio as gr
import cv2
import os
import torch


from controlnet_module import create_controlnet_app
from all_model import Model, download_all_controlnet_weights


if torch.cuda.is_available():
    if os.getenv('SYSTEM') == 'spaces':
        download_all_controlnet_weights()


# DEFAULT_MODEL_ID = os.getenv('DEFAULT_MODEL_ID','runwayml/stable-diffusion-v1-5')

# initiate the Model Class
model = Model(base_model_id='runwayml/stable-diffusion-v1-5', task_name='canny')



def create_developer_app():
    with gr.Blocks() as developer_app:
        with gr.Row():
            with gr.Column():
                Model = gr.Dropdown(["TestModel1", "TestModel2"], label="Model")
                SamplingStep = gr.Slider(minimum=1, maximum=20, step=1, value=1, label="Sampling Step")
                SamplingMethod = gr.Dropdown(["Euler a", "Euler", "LMS", "DPM++2Sa", "DPM++ 2M"], label="Sampling Method")
            with gr.Column():
                Batchcount = gr.Slider(minimum=1, maximum=10, step=1, value=1, label="Batch Count")
                BatchSize = gr.Slider(minimum=1, maximum=10, step=1, value=1, label="Batch Size")
                Seed = gr.Slider(minimum=1, maximum=10, step=1, value=1, label="Seed")
                CN_bool = gr.Checkbox(label="ControlNet")
        gr.Markdown("Result Number & Display Control!!")
        with gr.Row():
            import global_components
            global_components.GenerateNum = gr.Slider(minimum=1, maximum=50, step=1, value=50, label="Result Generate Number Controller")
            global_components.DisplayNum = gr.Slider(minimum=1, maximum=50, step=1, value=50, label="Result Display Number Controller")
            global_components.ConfirmDisplay = gr.Button("Confirm Display Number")
            
        
        with gr.Accordion("Open for More!"):
            gr.Markdown("Look at me...")
        
        ################## Stable Diffusion/ControlNet API testing #####################
        gr.Markdown("### Model (Stable Diffusion/ControlNet) API integrate testing")
        # generate the testing app
        create_controlnet_app(model.process_canny)

        print("[Developer App Created Successfully]")
    return developer_app
        


if __name__ == "__main__":
    create_developer_app()