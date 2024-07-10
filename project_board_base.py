import json
import os
from datetime import datetime

DB_DIR = 'db'

if not os.path.exists(DB_DIR):
    os.makedirs(DB_DIR)

# Helper functions
def load_data(file_name):
    file_path = os.path.join(DB_DIR, file_name)
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    return {}

def save_data(file_name, data):
    file_path = os.path.join(DB_DIR, file_name)
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

# ProjectBoardBase class
class ProjectBoardBase:
    """
    A project board is a unit of delivery for a project. Each board will have a set of tasks assigned to a user.
    """

    # create a board
    def create_board(self, request: str):
        """
        :param request: A json string with the board details.
        {
            "name" : "<board_name>",
            "description" : "<description>",
            "team_id" : "<team id>"
            "creation_time" : "<date:time when board was created>"
        }
        :return: A json string with the response {"id" : "<board_id>"}

        Constraint:
         * board name must be unique for a team
         * board name can be max 64 characters
         * description can be max 128 characters
        """
        pass

    # close a board
    def close_board(self, request: str) -> str:
        """
        :param request: A json string with the user details
        {
          "id" : "<board_id>"
        }

        :return:

        Constraint:
          * Set the board status to CLOSED and record the end_time date:time
          * You can only close boards with all tasks marked as COMPLETE
        """
        pass

    # add task to board
    def add_task(self, request: str) -> str:
        """
        :param request: A json string with the task details. Task is assigned to a user_id who works on the task
        {
            "title" : "<task_title>",
            "description" : "<description>",
            "user_id" : "<user_id>"
            "creation_time" : "<date:time when task was created>"
        }
        :return: A json string with the response {"id" : "<task_id>"}

        Constraint:
         * task title must be unique for a board
         * title name can be max 64 characters
         * description can be max 128 characters

        Constraints:
        * Can only add task to an OPEN board
        """
        pass

    # update the status of a task
    def update_task_status(self, request: str):
        """
        :param request: A json string with the user details
        {
            "id" : "<task_id>",
            "status" : "OPEN | IN_PROGRESS | COMPLETE"
        }
        """
        pass

    # list all open boards for a team
    def list_boards(self, request: str) -> str:
        """
        :param request: A json string with the team identifier
        {
          "id" : "<team_id>"
        }

        :return:
        [
          {
            "id" : "<board_id>",
            "name" : "<board_name>"
          }
        ]
        """
        pass

    def export_board(self, request: str) -> str:
        """
        Export a board in the out folder. The output will be a txt file.
        We want you to be creative. Output a presentable view of the board and its tasks with the available data.
        :param request:
        {
          "id" : "<board_id>"
        }
        :return:
        {
          "out_file" : "<name of the file created>"
        }
        """
        pass

# ProjectBoardManager class
class ProjectBoardManager(ProjectBoardBase):
    def __init__(self):
        self.boards_file = 'boards.json'
        self.boards = load_data(self.boards_file)

    def create_board(self, request: str) -> str:
        board_data = json.loads(request)
        board_id = str(len(self.boards) + 1)
        for board in self.boards.values():
            if board_data['name'] == board['name'] and board_data['team_id'] == board['team_id']:
                raise ValueError("Board name must be unique for the team")
        if len(board_data['name']) > 64 or len(board_data['description']) > 128:
            raise ValueError("Board name or description exceeds max length")
        self.boards[board_id] = {
            "name": board_data['name'],
            "description": board_data['description'],
            "team_id": board_data['team_id'],
            "creation_time": board_data['creation_time'],
            "tasks": []
        }
        save_data(self.boards_file, self.boards)
        return json.dumps({"id": board_id})

    def close_board(self, request: str) -> str:
        board_id = json.loads(request)['id']
        board = self.boards.get(board_id)
        if board:
            # Check if all tasks are marked as COMPLETE
            if all(task.get('status') == 'COMPLETE' for task in board['tasks']):
                board['status'] = 'CLOSED'
                board['end_time'] = datetime.now().isoformat()
                save_data(self.boards_file, self.boards)
                return json.dumps({"status": "Board closed"})
            else:
                return json.dumps({"error": "Cannot close board, some tasks are not complete"})
        else:
            return json.dumps({"error": "Board not found"})

    def add_task(self, request: str) -> str:
        task_data = json.loads(request)
        board_id = task_data['board_id']
        task_id = str(len(self.boards[board_id]['tasks']) + 1)
        # Check if task title is unique for the board
        if any(task['title'] == task_data['title'] for task in self.boards[board_id]['tasks']):
            raise ValueError("Task title must be unique for the board")
        if len(task_data['title']) > 64 or len(task_data['description']) > 128:
            raise ValueError("Task title or description exceeds max length")
        self.boards[board_id]['tasks'].append({
            "id": task_id,
            "title": task_data['title'],
            "description": task_data['description'],
            "user_id": task_data['user_id'],
            "creation_time": task_data['creation_time'],
            "status": "OPEN"
        })
        save_data(self.boards_file, self.boards)
        return json.dumps({"id": task_id})

    def update_task_status(self, request: str):
        task_data = json.loads(request)
        board_id = task_data['board_id']
        task_id = task_data['task_id']
        status = task_data['status']
        task = next((t for t in self.boards[board_id]['tasks'] if t['id'] == task_id), None)
        if task:
            task['status'] = status
            save_data(self.boards_file, self.boards)
            return json.dumps({"status": "Task status updated"})
        else:
            return json.dumps({"error": "Task not found"})

    def list_boards(self, request: str) -> str:
        team_id = json.loads(request)['id']
        team_boards = [{"id": board_id, "name": board['name']} for board_id, board in self.boards.items() if board['team_id'] == team_id]
        return json.dumps(team_boards, indent=4)

    def export_board(self, request: str) -> str:
        board_id = json.loads(request)['id']
        board = self.boards.get(board_id)
        if board:
            out_file_name = f"board_{board_id}.txt"
            with open(os.path.join("out", out_file_name), 'w') as out_file:
                out_file.write(f"Board Name: {board['name']}\n")
                out_file.write(f"Board Description: {board['description']}\n")
                out_file.write(f"Team ID: {board['team_id']}\n")
                out_file.write("Tasks:\n")
                for task in board['tasks']:
                    out_file.write(f"- Task ID: {task['id']}\n")
                    out_file.write(f"  Title: {task['title']}\n")
                    out_file.write(f"  Description: {task['description']}\n")
                    out_file.write(f"  Assigned User ID: {task['user_id']}\n")
                    out_file.write(f"  Creation Time: {task['creation_time']}\n")
                    out_file.write(f"  Status: {task['status']}\n\n")
            return json.dumps({"out_file": out_file_name})
        else:
            return json.dumps({"error": "Board not found"})

# Usage Example
if __name__ == "__main__":
    board_manager = ProjectBoardManager()

    # Create a board
    board1 = {
        "name": "Project Board 1",
        "description": "This is the first project board",
        "team_id": "1",
        "creation_time": datetime.now().isoformat()
    }
    print(board_manager.create_board(json.dumps(board1)))

    # Add tasks to the board
    task1 = {
        "board_id": "1",
        "title": "Task 1",
        "description": "Description for Task 1",
        "user_id": "1",
        "creation_time": datetime.now().isoformat()
    }
    print(board_manager.add_task(json.dumps(task1)))

    task2 = {
        "board_id": "1",
        "title": "Task 2",
        "description": "Description for Task 2",
        "user_id": "2",
        "creation_time": datetime.now().isoformat()
    }
    print(board_manager.add_task(json.dumps(task2)))

    # List boards for a team
    print(board_manager.list_boards(json.dumps({"id": "1"})))

    # Update task status
    update_task_data = {
        "board_id": "1",
        "task_id": "1",
        "status": "IN_PROGRESS"
    }
    print(board_manager.update_task_status(json.dumps(update_task_data)))

    # Close a board
    close_board_data = {
        "id": "1"
    }
    print(board_manager.close_board(json.dumps(close_board_data)))

    # Export a board
    export_board_data = {
        "id": "1"
    }
    print(board_manager.export_board(json.dumps(export_board_data)))
