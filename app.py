import gradio as gr
import os
import PIL
import numpy as np
import torch


from developer_module import create_developer_app
from user_module import create_user_app


def begin():

    print("---------------[Start RoomDreaming]---------------")

    DESCRIPTION = '''# [ControlNet v1.0](https://github.com/lllyasviel/ControlNet)
    <p class="note">New ControlNet v1.1 is available <a href="https://huggingface.co/spaces/hysts/ControlNet-v1-1">here</a>.</p>
    '''
    SPACE_ID = os.getenv('SPACE_ID')
    ALLOW_CHANGING_BASE_MODEL = SPACE_ID != 'hysts/ControlNet'

    if SPACE_ID is not None:
        DESCRIPTION += f'\n<p>For faster inference without waiting in queue, you may duplicate the space and upgrade to GPU in settings. <a href="https://huggingface.co/spaces/{SPACE_ID}?duplicate=true"><img style="display: inline; margin-top: 0em; margin-bottom: 0em" src="https://bit.ly/3gLdBN6" alt="Duplicate Space" /></a></p>'
    if not torch.cuda.is_available():
        DESCRIPTION += '\n<p>Running on CPU 🥶 This demo does not work on CPU.</p>'

    print("[Start Cuda Testing]")
    print("[Torch Version: ", torch.__version__, "]")
    print("[Cuda Version: ", torch.version.cuda, "]")
    print("[Cuda is available: ", torch.cuda.is_available(), "]")




with gr.Blocks() as demo:
    
    print("[RoomDreaming Loading...]")

    gr.Markdown(
    """
    # RoomDreaming Testing UI/UX
    ### This is a test UI for RoomDreaming System!!
    """)

    with gr.Tab(label= "Developer"):
        create_developer_app()

    with gr.Tab(label= "User"):
        
        
        create_user_app()


    print("[Finish Loading RoomDreaming]")
        







if __name__ == "__main__":
    begin()

    import global_components
    global_components.initialize()

    demo.launch()
