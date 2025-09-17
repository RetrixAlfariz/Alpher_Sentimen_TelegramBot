import os
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch

_MODEL_PATH = os.getenv("MODEL_PATH", "model")
_DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
_TOKENIZER = AutoTokenizer.from_pretrained(_MODEL_PATH)
_MODEL = AutoModelForSequenceClassification.from_pretrained(_MODEL_PATH)
_MODEL.to(_DEVICE)
_MODEL.eval()
_LABEL_DICT = {1: "positif", 0: "netral", 2: "negatif"}

def predict_sentiment(text: str) -> str:
    inputs = _TOKENIZER(text, padding=True, truncation=True, max_length=128, return_tensors="pt")
    inputs = {key: value.to(_DEVICE) for key, value in inputs.items()}
    with torch.no_grad():
        logits = _MODEL(**inputs).logits
    probabilities = torch.nn.functional.softmax(logits, dim=-1)
    predicted_class = torch.argmax(probabilities, dim=-1).item()
    return _LABEL_DICT.get(predicted_class, "tidak diketahui")
