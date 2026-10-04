import json

from config import get_client, DEFAULT_MODEL


SYSTEM_PROMPT = """
You are MEMORA, a personal AI memory assistant.

Analyze the user's message and extract useful information.

Return ONLY valid JSON.

Use exactly this structure:

{
    "tasks": [],
    "events": [],
    "memories": []
}

TASKS:
Things the user needs to do.

Each task:
{
    "title": "...",
    "description": "...",
    "deadline": "..."
}

EVENTS:
Things happening at a date or time.

Each event:
{
    "title": "...",
    "date": "...",
    "description": "..."
}

MEMORIES:
Useful personal information, preferences, facts, or ideas.

Each memory:
{
    "content": "...",
    "category": "..."
}

Do not invent information.
Do not explain your reasoning.
Do not use markdown.
Do not write anything before or after the JSON.
"""


def analyze_input(user_text):
    client = get_client()

    response = client.chat.completions.create(
        model=DEFAULT_MODEL,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": user_text
            }
        ],
        max_tokens=700,
        temperature=0
    )

    content = response.choices[0].message.content.strip()

    # Find JSON inside the AI response
    start = content.find("{")
    end = content.rfind("}")

    if start == -1 or end == -1:
        raise ValueError(
            f"AI did not return JSON:\n{content}"
        )

    json_text = content[start:end + 1]

    try:
        return json.loads(json_text)

    except json.JSONDecodeError as error:
        raise ValueError(
            f"Invalid JSON from AI:\n{content}\n\n"
            f"JSON error:\n{error}"
        )


def generate_response(result):
    """
    Create a friendly MEMORA response locally.

    No second NVIDIA API call is needed.
    """

    tasks = result.get("tasks", [])
    events = result.get("events", [])
    memories = result.get("memories", [])

    responses = []

    # -------------------------
    # TASKS
    # -------------------------

    for task in tasks:

        title = task.get("title", "").strip()
        deadline = task.get("deadline", "").strip()

        if not title:
            continue

        if deadline:
            responses.append(
                f'✅ Got it! I added "{title}" to your tasks for {deadline}.'
            )
        else:
            responses.append(
                f'✅ Got it! I added "{title}" to your tasks.'
            )

    # -------------------------
    # EVENTS
    # -------------------------

    for event in events:

        title = event.get("title", "").strip()
        date = event.get("date", "").strip()

        if not title:
            continue

        if date:
            responses.append(
                f'📅 Got it! I saved "{title}" as an event for {date}.'
            )
        else:
            responses.append(
                f'📅 Got it! I saved "{title}" as an event.'
            )

    # -------------------------
    # MEMORIES
    # -------------------------

    for memory in memories:

        if isinstance(memory, dict):

            content = memory.get("content", "").strip()

        else:

            content = str(memory).strip()

        if not content:
            continue

        # Remove a full stop if the AI already added one
        content = content.rstrip(".")

        responses.append(
            f"🧠 Got it! I'll remember that {content}."
        )

    # -------------------------
    # NOTHING FOUND
    # -------------------------

    if not responses:

        return (
            "I understood your message, "
            "but I couldn't find anything specific to save."
        )

    # Join multiple responses
    return " ".join(responses)


# -------------------------
# TEST MEMORA
# -------------------------

if __name__ == "__main__":

    test_input = (
        "Remember that my favorite subject is BCE."
    )

    print("\nUSER:")
    print(test_input)

    # Ask NVIDIA to understand the message
    result = analyze_input(test_input)

    print("\nMEMORA AI RESULT:")
    print(json.dumps(result, indent=4))

    # Generate response locally
    message = generate_response(result)

    print("\nMEMORA RESPONSE:")
    print(message)