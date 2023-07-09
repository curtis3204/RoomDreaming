import gradio as gr
import os
import cv2
import PIL
import numpy as np




class Candidate_Container:
    def __init__(self):
        self.candidates = []
        self.candidate_num = 0
        self.imgsblocks = {}
        self.nextbuttons = []
        self.clearbuttons = []

    def addCandidate(self, iteration_num, num):
        x = globals()["Candidate-" + str(iteration_num) + "-" + str(num)] = Candidate(iteration_num, num)
        self.candidates.append(x)
        self.candidate_num += 1

    def callCandidate(self, iteration_num, num):
        return globals()["Candidate-" + str(iteration_num) + "-" + str(num)]

    def removeCandidate(self, iteration_num, num):
        self.candidates.remove(globals()["Candidate-" + str(iteration_num) + "-" + str(num)])
        self.candidate_num -= 1

    def setImagesBlocks(self, iteration_num, num):
        if iteration_num not in self.imgsblocks.keys():
            self.imgsblocks[iteration_num] = []
            self.imgsblocks[iteration_num].append(globals()["Candidate-" + str(iteration_num) + "-" + str(num)].img_component)
        else:
            self.imgsblocks[iteration_num].append(globals()["Candidate-" + str(iteration_num) + "-" + str(num)].img_component)
        
    def setNextButtons(self, button):
        self.nextbuttons.append(button)

    def setClearButtons(self, button):
        self.clearbuttons.append(button)
        


class Candidate:
    def __init__(self, iteration_num, num):
        self.iteration_num = iteration_num
        self.num = num
        self.name = "Candidate-" + str(iteration_num) + "-" + str(num)

    def setComponents(self, block_component, img_component, style_component, layout_component):
        self.block_component = block_component
        self.img_component = img_component
        self.style_component = style_component
        self.layout_component = layout_component

    def setPrompts(self, prompts):
        self.prompts = prompts

    def setParemeters(self, parameters):
        self.parameters = parameters

    def setImagepath(self, imgpath):
        self.imgpath = imgpath

    def getScore(self):
        style_score = int(self.style_component)
        layout_score = int(self.layout_component)
        return style_score, layout_score


def init_Candidate_Container():
    container = Candidate_Container()
    return container








def Generate(Roomtype, UserNumber, RoomImage, Generatenumber, Displaynumber):
    #read all images in the file
    allimgspath, selectimgspath = ReadallImages("RoomImages", Generatenumber)
    text = "Room Type: " + Roomtype + "\n" \
    + "Number of Users: " + str(UserNumber)  + "\n" \
    + "Generated Result Number : " + str(Generatenumber) + "\n" \
    + "Displayed Result Number : " + str(Displaynumber)  
    
    # outputs = [text]+selectimgspath
    
    print("Generate!!!!")
    return selectimgspath



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



def Generate_Candidate(Candidate_container, iteration_num = 1, num = 1):
    
    with gr.Blocks() as block_component:
        with gr.Column():
            img_component = gr.Image(type= "filepath", label="Result Image")
            with gr.Row():
                # Like = gr.Checkbox(label="Like")
                # Dislike = gr.Checkbox(label="Disike")
                with gr.Column():
                    gr.Markdown("### Score of Design Style 設計風格", elem_classes=["test"])
                    StyleSlider = gr.Slider(minimum=0, maximum=10, step=1, value=5, label="Design Style: Score")
                    gr.Markdown("### Score of Design Layout 設計布局")
                    LayoutSlider = gr.Slider(minimum=0, maximum=10, step=1, value=5, label="Design Layout: Score")
            
    
    temp = Candidate_container.callCandidate(iteration_num, num)
    temp.setComponents(block_component, img_component, StyleSlider, LayoutSlider)
    
    Candidate_container.setImagesBlocks(iteration_num, num)
    
    return temp




def GenerateIteration(Candidate_container, tab_num, Total= 50, rownum= 4):
    Total = int(Total)
    rownum = int(rownum)
    num = 0

    for i in range(Total//rownum):
        with gr.Row():
            for i in range(rownum):
                num += 1
                Candidate_container.addCandidate(iteration_num= tab_num, num= num)
                Generate_Candidate(Candidate_container= Candidate_container, 
                                   iteration_num= tab_num, 
                                   num= num)
                
    if Total % rownum != 0:
        with gr.Row():
            for i in range(Total % rownum):
                num += 1
                Candidate_container.addCandidate(iteration_num= tab_num, num= num)
                Generate_Candidate(Candidate_container = Candidate_container, 
                                   iteration_num= tab_num, 
                                   num= num)
    return 



def generateTab(Candidate_container, TabNum, Each_tab_total= 50, Each_row= 4):
    with gr.Tab("Iteration "+str(TabNum)) as tab:
        with gr.Row():

            button1 = globals()["NextIteration"+str(TabNum)] = gr.Button(str(TabNum)+ " - Next Iteration", variant='primary')
            button2 = globals()["ClearIteration"+str(TabNum)] = gr.Button(str(TabNum)+ " - Clear Iteration")
            Candidate_container.setNextButtons(button1)
            Candidate_container.setClearButtons(button2)

        GenerateIteration(Candidate_container, tab_num= TabNum, Total= Each_tab_total, rownum= Each_row)
    return



def generate_multiple_tab(Candidate_containe, tab_total_num, Each_tab_total, Each_row):
    for i in range(tab_total_num):
        generateTab(Candidate_container= Candidate_containe, TabNum= i+1, Each_tab_total= Each_tab_total, Each_row= Each_row)
        # ResultImgBlock = process_imgs_to_block(Candidate_container= Candidate_containe, TabNum= i+1, Each_tab_total= Each_tab_total)
    return





if __name__ == "__main__":
    container = init_Candidate_Container()