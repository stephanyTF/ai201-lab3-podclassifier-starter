import json
import os
from groq import Groq
from config import GROQ_API_KEY, LLM_MODEL, VALID_LABELS, DATA_PATH, TRAIN_FILE, LABELS_FILE

_client = Groq(api_key=GROQ_API_KEY)


def load_labeled_examples() -> list[dict]:
    """
    Load the training episodes and merge them with the student's labels.

    Returns a list of dicts, each with:
      - "id"          : episode ID
      - "title"       : episode title
      - "podcast"     : podcast name
      - "description" : episode description
      - "label"       : the label from my_labels.json (may be None if not yet annotated)

    Only returns episodes where the label is a valid, non-null string.
    Episodes with null labels are silently skipped.
    """
    train_path = os.path.join(DATA_PATH, TRAIN_FILE)
    labels_path = os.path.join(DATA_PATH, LABELS_FILE)

    with open(train_path, encoding="utf-8") as f:
        episodes = {ep["id"]: ep for ep in json.load(f)}

    with open(labels_path, encoding="utf-8") as f:
        labels = {entry["id"]: entry["label"] for entry in json.load(f)}

    labeled = []
    for ep_id, ep in episodes.items():
        label = labels.get(ep_id)
        if label in VALID_LABELS:
            labeled.append({**ep, "label": label})

    return labeled


def build_few_shot_prompt(labeled_examples: list[dict], description: str) -> str:
    """
    Build a few-shot classification prompt using the student's labeled training examples.

    TODO — Milestone 2:

    Your prompt needs to:
      1. Describe the task and the four valid labels
      2. Show the labeled training examples so the LLM can learn the pattern
      3. Present the new description and ask for a classification

    The LLM should return a single label from VALID_LABELS (exactly as written)
    plus a brief explanation of its reasoning. Think carefully about the output
    format you request — you'll need to parse it in classify_episode().

    Before writing code, complete specs/classifier-spec.md.
    """

    prompt_task = (
        """You are classifying podcast episodes based on the given podcast episode description. \n
        You should assign one of four labels: `interview`, `solo`, `panel`, or `narrative`.\n\n
        The output should match this specific format:\n
        Label: <one of: interview, solo, panel, narrative>\n
        Reasoning: <one or two sentences>\n"""
    )
    examples_block = "\n\n---\n\n".join(
        f"Title: {ex['title']}\n"
        f"Description: {ex['description']}\n"
        f"Label: {ex['label']}"
        for ex in labeled_examples
    )
    new_episode = (
        f"Title: (unknown)\nDescription: {description}\nLabel: ?"
    )

    error_handling = ( """
                      - If the labeled_examples is empty, return {"label": "unknown", "reasoning": "No labeled examples provided."}\n
                      - If the description is short, classify based on what is available."\n
                      """

    )
    return (
        #PART 1: Task description and output format
        f"{prompt_task}\n\n"

        #PART 2: Labeled examples (from load_labeled_examples)
        f"Here are labeled examples:\n\n{examples_block}\n\n---\n\n" 

        #PART 3: New episode to classify (use the description argument)
        f"Now classify this new episode:\n\n{new_episode}" 

        #PART 4: Instructions for handling edge cases
        f"These are how to handle edge cases:\n\n{error_handling}"
    )



def classify_episode(description: str, labeled_examples: list[dict]) -> dict:
    """
    Classify a single podcast episode description using the few-shot LLM classifier.

    TODO — Milestone 2 (complete after build_few_shot_prompt):

    Steps:
      1. Call build_few_shot_prompt() to construct the prompt
      2. Send it to the LLM via _client.chat.completions.create()
      3. Parse the response to extract a label and reasoning
      4. Validate the label — if it's not in VALID_LABELS, set it to "unknown"
      5. Return a dict with "label" and "reasoning" keys

    Handle the case where the LLM returns something unparseable gracefully —
    don't let a bad response crash the whole evaluation.

    Before writing code, complete specs/classifier-spec.md.
    """
    try:
        # 1.Call build_few_shot_prompt() to construct the prompt
        podcast_prompt = build_few_shot_prompt(labeled_examples, description)

        # 2.Send it to the LLM via _client.chat.completions.create()
        llm_response = _client.chat.completions.create(
            model=LLM_MODEL,
            messages=[{"role": "user", "content": podcast_prompt}],
            max_tokens=250)
        
        # 3.Parse the response to extract a label and reasoning
        response_text = llm_response.choices[0].message.content.strip()
    
        reasoning = response_text.text.strip()
        for line in response_text.splitlines():

            cleaned = line.strip().lower().lstrip("*-` ").rstrip("*` .,:")
            if cleaned.startswith("label:"):
                candidate = cleaned.split("label:", 1)[1].strip().strip("*`. ,")
                if candidate in VALID_LABELS:
                    label = candidate
                break    
        
        # 4. Validate the label — if it's not in VALID_LABELS, set it to "unknown"
        if label not in VALID_LABELS:
            label = "unknown"

        # Fallback: if the response doesn't match the expected format,look for any bare words
        if label == "unknown":
            lowered = response_text.lower()
            for valid in VALID_LABELS:
                if valid in lowered:
                    label = valid
                    break


        #5. Return a dict with "label" and "reasoning" keys
        return{
            "label": label,
            "reasoning": reasoning,
        }

    except Exception as e:
            # Handle unparseable response
            return {
                "label": "unknown",
                "reasoning": f"Classification failed: {e}."
            }





    



