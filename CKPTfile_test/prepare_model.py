
from transformers import DistilBertForSequenceClassification
import torch

print(" CUDA Testing!!!!!")
print(torch.__version__)
print(torch.version.cuda)
print(torch.cuda.is_available())

# pt_model = DistilBertForSequenceClassification.from_pretrained("xsarchitectural_v11.ckpt", from_tf=True)
# pt_model.save_pretrained("xsarchitectural_v11.ckpt")