from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
import json
import re

MODEL_PATH = "./enigma-gpt2/riddle_model"

tokenizer = GPT2Tokenizer.from_pretrained(MODEL_PATH)
model = GPT2LMHeadModel.from_pretrained(MODEL_PATH)
model.eval()

def clean_and_parse_output(raw_text):
    try:
        match = re.search(r'\{.*\}', raw_text, re.DOTALL)
        if match:
            json_str = match.group(0)
            json_str = re.sub(r',\s*}', '}', json_str) 
            json_str = re.sub(r',\s*\]', ']', json_str) 
            data = json.loads(json_str)
            return data
    except json.JSONDecodeError:
        pass 

    riddle_match = re.search(r'"riddle"\s*:\s*"([^"]+)"', raw_text, re.IGNORECASE)
    answer_match = re.search(r'"answer"\s*:\s*"([^"]+)"', raw_text, re.IGNORECASE)
    difficulty_match = re.search(r'"difficulty"\s*:\s*"([^"]+)"', raw_text, re.IGNORECASE)

    if riddle_match and answer_match:
        return {
            "riddle": riddle_match.group(1).strip(),
            "answer": answer_match.group(1).strip(),
            "difficulty": difficulty_match.group(1).strip() if difficulty_match else "unknown"
        }

    return {
        "error": "Could not parse riddle or answer from model output",
        "raw_output": raw_text
    }

def generate_enigma(level):
    if level not in ["easy", "hard"]:
        return {"error": "Invalid difficulty level. Use 'easy' or 'hard'."}

    prompt = f"Riddle ({level}): "
    input_ids = tokenizer.encode(prompt, return_tensors="pt")

    output = model.generate(
        input_ids,
        max_length=150 if level == "hard" else 100,
        temperature=0.8,
        top_k=50,
        do_sample=True,
        num_return_sequences=1
    )

    raw_text = tokenizer.decode(output[0], skip_special_tokens=True)

    return clean_and_parse_output(raw_text)
