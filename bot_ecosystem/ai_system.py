from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
def predict_sentiment(model_path,text):
    model = AutoModelForSequenceClassification.from_pretrained(model_path)
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    # memilih device yang tepat
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    # Tokenisasi teks
    inputs = tokenizer(text, padding=True, truncation=True, max_length=128, return_tensors="pt")
    inputs = {key: value.to(device) for key, value in inputs.items()}

    # Mendapatkan prediksi dari model
    with torch.no_grad():
        logits = model(**inputs).logits

    # Mengubah logits ke probabilitas
    probabilities = torch.nn.functional.softmax(logits, dim=-1)

    # Mengambil kelas dengan probabilitas tertinggi
    predicted_class = torch.argmax(probabilities, dim=-1).item()
    
    # Reverse integer menjadi value
    label_dict = {1:'positif', 0:'netral', 2:'negatif'}
    predicted_class = label_dict[predicted_class]
    return predicted_class