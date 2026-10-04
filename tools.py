from database import (
    initialize_database,
    save_memory,
    save_task,
    save_event,
    get_memories,
    get_tasks,
    get_events
)


USER_ID = "jay"


def process_ai_result(result):
    """
    Save the AI's extracted tasks, events and memories
    into the MEMORA database.
    """

    initialize_database()

    # Save tasks
    for task in result.get("tasks", []):
        save_task(
            user_id=USER_ID,
            title=task.get("title", ""),
            description=task.get("description"),
            deadline=task.get("deadline")
        )

    # Save events
    for event in result.get("events", []):
        save_event(
            user_id=USER_ID,
            title=event.get("title", ""),
            date=event.get("date"),
            description=event.get("description")
        )

    # Save memories
    for memory in result.get("memories", []):
        if isinstance(memory, dict):
            content = memory.get("content", "")
            category = memory.get("category")
        else:
            content = str(memory)
            category = None

        if content:
            save_memory(
                user_id=USER_ID,
                content=content,
                category=category
            )

    return {
        "tasks_saved": len(result.get("tasks", [])),
        "events_saved": len(result.get("events", [])),
        "memories_saved": len(result.get("memories", []))
    }


def show_memora_data():
    initialize_database()

    print("\n========== TASKS ==========")
    for task in get_tasks(USER_ID):
        print(task)

    print("\n========== EVENTS ==========")
    for event in get_events(USER_ID):
        print(event)

    print("\n========== MEMORIES ==========")
    for memory in get_memories(USER_ID):
        print(memory)