import gradio as gr
import os
import cv2
import PIL
import numpy as np




def Generate(Roomtype, UserNumber, RoomImage, Generatenumber, Displaynumber):
    #read all images in the file
    allimgspath, selectimgspath = ReadallImages("RoomImages", Generatenumber)
    text = "Room Type: " + Roomtype + "\n" \
    + "Number of Users: " + str(UserNumber)  + "\n" \
    + "Generated Result Number : " + str(Generatenumber) + "\n" \
    + "Displayed Result Number : " + str(Displaynumber)  
    
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
    
    #random the order of the images
    np.random.shuffle(SelectImagespath)
    return Allimagespath, SelectImagespath



def GenerateOptions(ResultImgBlock, likebtns, dislikebtns):
    with gr.Group() as group:
        with gr.Column():
            img = gr.outputs.Image(type= "filepath", label="Result Image")
            with gr.Row():
                Like = gr.inputs.Checkbox(label="Like")
                Dislike = gr.inputs.Checkbox(label="Disike")
            ResultImgBlock.append(img)
            likebtns.append(Like)
            dislikebtns.append(Dislike)
    return group




def GenerateLayout(Total = 50, rownum=4):
    ResultImgBlock = []
    likebtns = []
    dislikebtns = []
    Groups = []

    Total = int(Total)
    rownum = int(rownum)

    for i in range(Total//rownum):
        with gr.Row():
            for i in range(rownum):
                group = GenerateOptions(ResultImgBlock, likebtns, dislikebtns)
                Groups.append(group)
    if Total % rownum != 0:
        with gr.Row():
            for i in range(Total % rownum):
                group = GenerateOptions(ResultImgBlock, likebtns, dislikebtns)
                Groups.append(group)
    return ResultImgBlock, likebtns, dislikebtns, Groups





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
        
        with gr.Row():
                    gr.Markdown("Result Number & Display Control!!")
                    GenerateNum = gr.Slider(minimum=1, maximum=50, step=1, default=50, label="Result Generate Number Controller")
                    DisplayNum = gr.Slider(minimum=1, maximum=50, step=1, default=50, label="Result Display Number Controller")
                    ConfirmDisplay = gr.Button("Confirm Display Number")
        
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
                StartIteration = gr.Button("Start Iteration")
                
        
        gr.Markdown("## Iteration Results")
        Banner = gr.outputs.Textbox(label="System Log")
        
        with gr.Row():
            StopIteration = gr.Button("Finish!")
            

        #Tab Number
        TabNum = 1
        Tabs = []
        ResultImgBlock, likebtns, dislikebtns, groups = [], [], [], []


        def generateTab(Tabs, TabNum, ResultImgBlock, likebtns, dislikebtns, groups):
            with gr.Tab("Iteration "+str(TabNum)) as tab:
                with gr.Row():
                    globals()["NextIteration"+str(TabNum)] = gr.Button(str(TabNum)+ " - Next Iteration")
                    globals()["ClearIteration"+str(TabNum)] = gr.Button(str(TabNum)+ " - Clear Iteration")
                ResultImgBlock, likebtns, dislikebtns , groups= GenerateLayout(50, 4)
            print(tab)
            TabNum += 1
            Tabs.append(tab)
            return TabNum , ResultImgBlock, likebtns, dislikebtns, groups

           
        TabNum, ResultImgBlock, likebtns, dislikebtns, groups = generateTab(Tabs, TabNum, ResultImgBlock, likebtns, dislikebtns, groups)
        

        a,b,c,d = [], [], [], []
        e,f, g, h, i = [], [], [], [], []
        e, f, g, h, i  = generateTab(Tabs, TabNum, a, b, c, d)

        
        def Display(DisplayNum):
            DisplayNum = int(DisplayNum)
            return {
                **{ResultImgBlock[i]: gr.update(visible=False) for i in range(len(ResultImgBlock)-1, DisplayNum-1, -1)}, 
                **{likebtns[i]: gr.update(visible=False) for i in range(len(likebtns)-1, DisplayNum-1, -1)},
                **{dislikebtns[i]: gr.update(visible=False) for i in range(len(dislikebtns)-1, DisplayNum-1, -1)}
                }


        ConfirmDisplay.click(fn = Display, inputs=[DisplayNum], outputs=ResultImgBlock+likebtns+dislikebtns)

        StartIteration.click(fn = Generate, inputs=[Roomtype, UserNumber, RoomImage, GenerateNum, DisplayNum], outputs=[Banner]+ResultImgBlock)
        NextIteration1.click(fn = Generate, inputs=[Roomtype, UserNumber, RoomImage, GenerateNum, DisplayNum], outputs=[Banner]+f)

        
        


if __name__ == "__main__":
    demo.launch(share=True)
