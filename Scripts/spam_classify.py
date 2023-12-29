import torch
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
from datasets import load_dataset
from sklearn.model_selection import train_test_split


# Check if GPU is available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(device)

# Load tokenizer and model
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=2)
model.to(device)

# Load the spam dataset
dataset = load_dataset("sms_spam")

# Print the first 10 lines
for i in range(10):
    print(f"Message {i+1}: {dataset['train'][i]['sms']}")
    print(f"Label: {'Spam' if dataset['train'][i]['label'] == 1 else 'Ham'}")
    print("-" * 50)

#exit()

# Preprocess the data
def tokenize_function(examples):
    return tokenizer(examples["sms"], padding="max_length", truncation=True, max_length=128)

tokenized_datasets = dataset.map(tokenize_function, batched=True)

# Split into train and test
train_test_split_ratio = 0.8  # 80% for training, 20% for testing
train_idx, test_idx = train_test_split(range(len(tokenized_datasets["train"])), test_size=(1 - train_test_split_ratio), random_state=42)

train_dataset = tokenized_datasets["train"].select(train_idx)
test_dataset = tokenized_datasets["train"].select(test_idx)

# Further reduce the size of the datasets if needed
small_train_dataset = train_dataset.shuffle(seed=42).select(range(1000))  # Adjust range as needed
small_eval_dataset = test_dataset.shuffle(seed=42).select(range(500))

# Define training arguments
training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir="./logs",
    logging_steps=10,
)

# Initialize Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=test_dataset
)

# Train the model
trainer.train()

# Save the model
model.save_pretrained("./bert_spam_classifier")

# Function for inference
def predict(text):
    inputs = tokenizer(text, return_tensors="pt", padding="max_length", truncation=True, max_length=128).to(device)
    with torch.no_grad():
        logits = model(**inputs).logits
    predicted_class_id = logits.argmax().item()
    return "spam" if predicted_class_id == 1 else "ham"

# Test the model with a new sentence
print(predict("Free entry in 2 a weekly comp to win FA Cup final tkts 21st May 2005. Text FA to 87121 to receive entry question(std txt rate)"))


