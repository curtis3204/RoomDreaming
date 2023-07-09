import gradio as gr


def initialize():
    global GenerateNum
    global DisplayNum
    global ConfirmDisplay
    
    GenerateNum = gr.Slider(minimum=1, maximum=50, step=1, value=50, label="Result Generate Number Controller")
    DisplayNum = gr.Slider(minimum=1, maximum=50, step=1, value=50, label="Result Display Number Controller")
    ConfirmDisplay = gr.Button("Confirm Display Number")