# Codebase Overview

This repository contains a simple Telegram bot that performs sentiment analysis in Indonesian.
Below is a high-level description of the main components and some pointers for further exploration.

## Main Components

1. **Bot runner** – `main.py` imports the Telegram bot module and starts it:
   ```python
   from bot_ecosystem import bot_telegram
   bot_telegram.run()
   ```

2. **Telegram bot logic** – `bot_ecosystem/bot_telegram.py` handles connection to Telegram using Telethon and defines command handlers. The `/sentimen` command processes user text and returns the sentiment label:
   ```python
   @bot.on(events.NewMessage(pattern='/sentimen'))
   async def echo(event):
       data = event.text.split()
       data.pop(0)
       data = ' '.join(data)
       response = predict_sentiment('model', data)
       response = f'sentimennya adalah {response}'
       await event.respond(response)
   ```

3. **Sentiment prediction** – `bot_ecosystem/ai_system.py` loads a fine-tuned model from disk using HuggingFace Transformers and returns the predicted sentiment:
   ```python
   def predict_sentiment(model_path, text):
       model = AutoModelForSequenceClassification.from_pretrained(model_path)
       tokenizer = AutoTokenizer.from_pretrained(model_path)
       device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
       model.to(device)
       inputs = tokenizer(text, padding=True, truncation=True,
                          max_length=128, return_tensors="pt")
       inputs = {key: value.to(device) for key, value in inputs.items()}

       with torch.no_grad():
           logits = model(**inputs).logits

       probabilities = torch.nn.functional.softmax(logits, dim=-1)
       predicted_class = torch.argmax(probabilities, dim=-1).item()
       label_dict = {1: 'positif', 0: 'netral', 2: 'negatif'}
       predicted_class = label_dict[predicted_class]
       return predicted_class
   ```

4. **Model and dataset**
   - The `model/` directory stores the pre-trained and fine-tuned model files.
   - The `dataset/indonlu_smsa.tsv` file contains the Indonesian sentiment dataset used for training.

5. **Training notebook** – `machine_training.ipynb` details how the dataset is loaded, tokenized, and used to fine-tune the model with `Trainer` from HuggingFace.

6. **Environment configuration** – `.env.templete` lists the required variables:
   ```
   API_ID=
   API_HASH=''
   BOT_TOKEN=''
   TELEGRAM_TOKEN=''
   MODEL_PATH='model'
   DATASET_PATH='dataset/indonlu_smsa.tsv'
   ```

## Important Points

- The bot uses Telethon for Telegram communication. Copy `.env.templete` to `.env` and fill in your credentials before running `main.py`.
- The sentiment model is loaded each time `predict_sentiment` is called, which could be optimized by loading the model once and reusing it.
- The dataset and model are in Indonesian. The notebook provides a reproducible training process.

## Suggestions for Further Learning

1. **Telethon** – Learn the basics of Telethon to customize bot behavior.
2. **HuggingFace Transformers** – Understand `AutoModelForSequenceClassification` and how to fine-tune models.
3. **Environment management** – Explore how environment variables configure the bot.
4. **Model deployment** – Consider ways to keep the model in memory or deploy it via an external service for better performance.
5. **Dataset expansion** – Experiment with collecting more Indonesian text or adding new sentiment categories.

