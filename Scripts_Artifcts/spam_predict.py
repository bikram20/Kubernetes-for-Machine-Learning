import sys
import torch
from transformers import BertTokenizer, BertForSequenceClassification

# Check if GPU is available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(device)

# Load model from saved state
model_path = "./bert_spam_classifier"
model = BertForSequenceClassification.from_pretrained(model_path)

# Load the tokenizer from the Hugging Face model hub
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model.to(device)

# Function for inference
def predict(text):
    inputs = tokenizer(text, return_tensors="pt", padding="max_length", truncation=True, max_length=128).to(device)
    with torch.no_grad():
        logits = model(**inputs).logits
    predicted_class_id = logits.argmax().item()
    return "spam" if predicted_class_id == 1 else "ham"

# Check if an argument is provided
if len(sys.argv) > 1:
    input_text = sys.argv[1]
    prediction = predict(input_text)
    print(f"Prediction for '{input_text}': {prediction}")
else:
    print("No input text provided.")

