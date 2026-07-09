import torch
from transformers import pipeline

_generator = None


def get_generator():
    global _generator

    if _generator is None:
        _generator = pipeline(
            "text-generation",
            model="HuggingFaceTB/SmolLM2-360M-Instruct",
            torch_dtype=torch.float32,
        )

    return _generator


SYSTEM_PROMPT = """
You are SmartToDo AI.

Analyze the task.

Explain:
- why the priority is high or low;
- what the biggest risk is;
- give one recommendation.

Maximum 3 short sentences.
"""


def ask_ai(prompt: str) -> str:
    generator = get_generator()

    full_prompt = f"""
{SYSTEM_PROMPT}

Task:

{prompt}

Answer:
"""

    response = generator(
        full_prompt,
        max_new_tokens=80,
        do_sample=False,
        return_full_text=False,
        pad_token_id=generator.tokenizer.eos_token_id,
    )

    return response[0]["generated_text"].strip()