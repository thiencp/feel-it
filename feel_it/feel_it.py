from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from feel_it.dataset import TextDataset

class SentimentClassifier:

    def __init__(self):

        self.sentiment_map = {0: "negative", 1: "positive"}
        self.tokenizer = AutoTokenizer.from_pretrained("MilaNLProc/feel-it-italian-sentiment")
        self.model = AutoModelForSequenceClassification.from_pretrained("MilaNLProc/feel-it-italian-sentiment")
        self.model.eval()
        self.device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')

    def predict(self, sentences, batch_size=32):
        train_encodings = self.tokenizer(sentences,
                                    truncation=True,
                                    padding=True,
                                    max_length=500)

        train_dataset = TextDataset(train_encodings)

        loader = torch.utils.data.DataLoader(train_dataset, batch_size=batch_size)
        collect_outputs = []
        with torch.no_grad():
            for batch in loader:
                input_ids = batch['input_ids']
                attention_mask = batch['attention_mask']

                outputs = self.model(input_ids, attention_mask=attention_mask)
                collect_outputs.extend(torch.argmax(outputs["logits"], axis=1).cpu().numpy().tolist())

        return [self.sentiment_map[k] for k in collect_outputs]

class EmotionClassifier:

    def __init__(self):

        self.emotion_map = {0: "anger", 1: "fear", 2 : "joy", 3: "sadness"}
        self.tokenizer = AutoTokenizer.from_pretrained("MilaNLProc/feel-it-italian-emotion")
        self.model = AutoModelForSequenceClassification.from_pretrained("MilaNLProc/feel-it-italian-emotion")
        self.model.eval()
        self.device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')

    def predict(self, sentences, batch_size=32):
        train_encodings = self.tokenizer(sentences,
                                    truncation=True,
                                    padding=True,
                                    max_length=500)

        train_dataset = TextDataset(train_encodings)

        loader = torch.utils.data.DataLoader(train_dataset, batch_size=batch_size)
        collect_outputs = []

        with torch.no_grad():
            for batch in loader:
                input_ids = batch['input_ids']
                attention_mask = batch['attention_mask']

                outputs = self.model(input_ids, attention_mask=attention_mask)
                collect_outputs.extend(torch.argmax(outputs["logits"], axis=1).cpu().numpy().tolist())

        return [self.emotion_map[k] for k in collect_outputs]
