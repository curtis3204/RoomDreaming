import gradio as gr
import os
import sys
import inspect


from candidate_module import Candidate_Container, Candidate


current_module = sys.modules[__name__]

container = Candidate_Container()
# c1 = Candidate("imgpath", 1, 1)
# c2 = Candidate("imgpath", 1, 2)

container.addCandidate("imgpath", 1, 1)
container.addCandidate("imgpath", 1, 2)

print(container.candidate_num)
print(container.callCandidate(1, 1).name)
print(container.callCandidate(1, 2).name)


container.callCandidate(1, 1).setPrompts("TESTTEST")
print(container.callCandidate(1, 1).prompts)

print("\n")
def print_classes():
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if inspect.isclass(obj):
            print(name)
            print(obj)
        if obj == container:
            print(obj.candidates)
            print(obj.candidates[0].name)


print_classes()


