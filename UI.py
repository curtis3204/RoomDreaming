import gradio as gr
import os
import cv2
import PIL
import numpy as np




def Generate(Roomtype, UserNumber, RoomImage, ResultController):
    selectnumber = int(ResultController)
    #read all images in the file
    allimgspath, selectimgspath = ReadallImages("RoomDreaming_System/RoomImages", selectnumber)
    text = "Room Type: " + Roomtype + "\n" + "Number of Users: " + str(UserNumber)  + "\n" + "Result Number Controller: " + str(ResultController)    
    
    outputs = [text]+selectimgspath
    
    return outputs


#read all images in the file
def ReadallImages(path, SelectNumber):
    # Allimages = []
    Allimagespath = []
    for file in os.listdir(path):
        if file.endswith(".png"):
            # img = cv2.imread(os.path.join(path, file))
            Allimagespath.append(os.path.join(path, file))
            # Allimages.append(img)
    
    # only select the SelectNumber of images
    SelectImagespath = []
    for i in range(SelectNumber):
        SelectImagespath.append(Allimagespath[i])
    
    return Allimagespath, SelectImagespath







with gr.Blocks() as demo:
    
    gr.Markdown(
    """
    # RoomDreaming Testing UI/UX
    ### This is a test UI for RoomDreaming System!!
    """)
    with gr.Tab("Developer"):
        with gr.Row():
            with gr.Column():
                Model = gr.inputs.Dropdown(["TestModel1", "TestModel2"], label="Model")
                SamplingStep = gr.inputs.Slider(minimum=1, maximum=20, step=1, default=1, label="Sampling Step")
                SamplingMethod = gr.inputs.Dropdown(["Euler a", "Euler", "LMS", "DPM++2Sa", "DPM++ 2M"], label="Sampling Method")
            with gr.Column():
                Batchcount = gr.inputs.Slider(minimum=1, maximum=10, step=1, default=1, label="Batch Count")
                BatchSize = gr.inputs.Slider(minimum=1, maximum=10, step=1, default=1, label="Batch Size")
                Seed = gr.inputs.Slider(minimum=1, maximum=10, step=1, default=1, label="Seed")
                CN_bool = gr.inputs.Checkbox(label="ControlNet")
        
        with gr.Accordion("Open for More!"):
            gr.Markdown("Look at me...")


    with gr.Tab("User"):
        gr.Markdown("## User Requirements")
        with gr.Row():
            with gr.Column():
                gr.Markdown("Basic Information")
                Roomtype = gr.inputs.Dropdown(["Workshop","Office","Bedroom", "Livingroom", "Kitchen", "Bathroom", "Balcony", "Diningroom", "Studyroom", "Toilet", "Others"], label="Room Type")
                UserNumber = gr.inputs.Slider(minimum=1, maximum=10, step=1, default=1, label="Number of Users")
                AdditionalRequirements = gr.inputs.Textbox(label="Additional Requirements")

            with gr.Column():
                gr.Markdown("Room Image")
                RoomImage = gr.inputs.Image(shape=(224, 224), label="Room Image")
                with gr.Row():
                    gr.Markdown("Result Number Control!!")
                    ResultController = gr.Slider(minimum=1, maximum=50, step=1, default=50, label="Result Number Controller")
                    Confirm = gr.Button("Confirm")
                GenerateButton = gr.Button("Start Iteration")
                
        
        gr.Markdown("## Iteration Results")
        Banner = gr.outputs.Textbox(label="Output")
        
        with gr.Row():
            NextIteration = gr.Button("Next Iteration")
            StopIteration = gr.Button("Finish!")


        resultimgs = []

        def GenerateLayout(resultnumber):
            for i in range(resultnumber//5):
                with gr.Row():
                    for i in range(5):
                        img = gr.outputs.Image(type= "filepath", label="Result Image")
                        resultimgs.append(img)
            if resultnumber % 5 != 0:
                with gr.Row():
                    for i in range(resultnumber % 5):
                        img = gr.outputs.Image(type= "filepath", label="Result Image")
                        resultimgs.append(img)
            return resultimgs

        GenerateLayout(50)        
        ResultController.change(GenerateLayout, ResultController, resultimgs)
        

        GenerateButton.click(fn = Generate, inputs=[Roomtype, UserNumber, RoomImage, ResultController], outputs=[Banner]+resultimgs)
        
        

        
        


if __name__ == "__main__":
    demo.launch()
