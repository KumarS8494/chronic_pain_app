from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Use GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

model_path = "krsuman123/Chronic_Pain_classification"
model = AutoModelForSequenceClassification.from_pretrained(model_path).to(device)
tokenizer = AutoTokenizer.from_pretrained(model_path)

label_map = {
    0: "Facet joint pain",
    1: "Lumbar disc prolapse",
    2: "Myofascial Pain",
    3: "Sacroiliac Joint Pain",
    # etc.
}

def predict_diagnosis(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512).to(device)
    print(f"Input device: {inputs['input_ids'].device}")
    print(f"Model device: {next(model.parameters()).device}")
    with torch.no_grad():
        outputs = model(**inputs)
    probs = torch.nn.functional.softmax(outputs.logits, dim=1)
    pred_label = torch.argmax(probs, dim=1).item()
    confidence = float(probs[0][pred_label])
    return f"Predicted Diagnosis: {label_map[pred_label]} (Confidence: {confidence:.2%})"
