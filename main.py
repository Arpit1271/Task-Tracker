import json
from datetime import datetime
from pathlib import Path
import sys

file = "data.json"
if not Path(file).exists():
    with open(file, "w") as f:
        json.dump([], f)


def load_task():
    with open(file, "r") as f:
        return json.load(f)


def save_task(tasks):
    with open(file, "w") as f:
        json.dump(tasks, f, indent=4)


def add_task(description):
    tasks = load_task()

    task_id = len(tasks) + 1

    new_task = {
        "id": task_id,
        "description": description,
        "status": "todo",
        "createdAt": datetime.now().strftime("%Y-%m-%d"),
        "updatedAt": datetime.now().strftime("%Y-%m-%d"),
    }

    tasks.append(new_task)
    save_task(tasks)

    print(f"Task added successfully (ID:{task_id})")


def update_task(task_id, description):
    tasks = load_task()

    i = 0
    while i < len(tasks):
        if tasks[i]["id"] == task_id:
            tasks[i]["description"] = description
            tasks[i]["updatedAt"] = datetime.now().strftime("%Y-%m-%d")
            print("Task updated.")
            break
        i += 1

    save_task(tasks)


def delete_task(task_id):
    tasks = load_task()

    new_tasks = []

    for task in tasks:
        if task["id"] != task_id:
            new_tasks.append(task)

    save_task(new_tasks)

    print("Task deleted.")


def mark_task(task_id, status):
    tasks = load_task()

    for task in tasks:
        if task["id"] == task_id:
            task["status"] = status
            task["updatedAt"] = datetime.now().strftime("%Y-%m-%d")
            print(f"Task marked as {status}")

    save_task(tasks)


def list_tasks(filter_status=None):
    tasks = load_task()

    if not tasks:
        print("No tasks found.")
        return

    for task in tasks:
        if filter_status and task["status"] != filter_status:
            continue

        print(f'{task["id"]} - {task["description"]} [{task["status"]}]')


# Check command input
if len(sys.argv) < 2:
    print("Usage: python task.py <command>")
    sys.exit()

command = sys.argv[1]

if command == "add":
    add_task(sys.argv[2])

elif command == "update":
    update_task(int(sys.argv[2]), sys.argv[3])

elif command == "delete":
    delete_task(int(sys.argv[2]))

elif command == "mark-in-progress":
    mark_task(int(sys.argv[2]), "in-progress")

elif command == "mark-done":
    mark_task(int(sys.argv[2]), "done")

elif command == "list":

    if len(sys.argv) == 2:
        list_tasks()

    elif sys.argv[2] == "done":
        list_tasks("done")

    elif sys.argv[2] == "todo":
        list_tasks("todo")

    elif sys.argv[2] == "in-progress":
        list_tasks("in-progress")

else:
    print("Unknown command")
