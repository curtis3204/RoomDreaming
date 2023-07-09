import gradio as gr
import os
import PIL
import numpy as np

import sys
import inspect
current_module = sys.modules[__name__]

from candidate_module import Candidate, Candidate_Container, generate_multiple_tab, Generate

import global_components



def create_user_app():
    with gr.Blocks() as user_app:
        gr.Markdown("## User Requirements")
        with gr.Row():
            with gr.Column():
                gr.Markdown("Basic Information")
                Roomtype = gr.Dropdown(["Workshop","Office","Bedroom", "Livingroom", "Kitchen", "Bathroom", "Balcony", "Diningroom", "Studyroom", "Toilet", "Others"], label="Room Type")
                UserNumber = gr.Slider(minimum=1, maximum=10, step=1, value=1, label="Number of Users")
                AdditionalRequirements = gr.Textbox(label="Additional Requirements")

            with gr.Column():
                gr.Markdown("Room Image")
                RoomImage = gr.Image(shape=(224, 224), label="Room Image")
                StartIteration = gr.Button("Start Iteration", variant='primary')
                
        gr.Markdown("## Iteration Results")
        Banner = gr.Textbox(label="System Log")
        with gr.Row():
            StopIteration = gr.Button("Finish!", variant='stop')
            
        # All Images would put here!    
        with gr.Row():
            global c_container
            c_container = Candidate_Container()

            #Tab Parameter
            tab_total_num = 3
            Each_tab_total = 50
            Each_row = 4
            generate_multiple_tab(Candidate_containe= c_container, tab_total_num= tab_total_num, Each_tab_total= Each_tab_total, Each_row= Each_row)
            ResultImgBlock = c_container.imgsblocks
        
    
        StartIteration.click(fn = Generate, inputs=[Roomtype, UserNumber, RoomImage, global_components.GenerateNum, global_components.DisplayNum], outputs=ResultImgBlock.get(1))

        for i in range(tab_total_num):
            c_container.nextbuttons[i].click(fn = Generate, inputs=[Roomtype, UserNumber, RoomImage, global_components.GenerateNum, global_components.DisplayNum], outputs=ResultImgBlock.get(i+2))



        # def Display(DisplayNum):
        #     DisplayNum = int(DisplayNum)
        #     return {
        #         **{ResultImgBlock[i]: gr.update(visible=False) for i in range(len(ResultImgBlock)-1, DisplayNum-1, -1)}, 
        #         **{likebtns[i]: gr.update(visible=False) for i in range(len(likebtns)-1, DisplayNum-1, -1)},
        #         **{dislikebtns[i]: gr.update(visible=False) for i in range(len(dislikebtns)-1, DisplayNum-1, -1)}
        #         }
        # global_components.ConfirmDisplay.click(fn = Display, inputs=[global_components.DisplayNum], outputs=ResultImgBlock+likebtns+dislikebtns)


        print("[User App Created Successfully]")


