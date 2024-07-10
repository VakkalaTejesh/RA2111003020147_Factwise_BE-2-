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

# UserBase class
class UserBase:
    """
    Base interface implementation for API's to manage users.
    """

    # create a user
    def create_user(self, request: str) -> str:
        """
        :param request: A json string with the user details
        {
          "name" : "<user_name>",
          "display_name" : "<display name>"
        }
        :return: A json string with the response {"id" : "<user_id>"}

        Constraint:
            * user name must be unique
            * name can be max 64 characters
            * display name can be max 64 characters
        """
        pass

    # list all users
    def list_users(self) -> str:
        """
        :return: A json list with the response
        [
          {
            "name" : "<user_name>",
            "display_name" : "<display name>",
            "creation_time" : "<some date:time format>"
          }
        ]
        """
        pass

    # describe user
    def describe_user(self, request: str) -> str:
        """
        :param request: A json string with the user details
        {
          "id" : "<user_id>"
        }

        :return: A json string with the response

        {
          "name" : "<user_name>",
          "description" : "<some description>",
          "creation_time" : "<some date:time format>"
        }

        """
        pass

    # update user
    def update_user(self, request: str) -> str:
        """
        :param request: A json string with the user details
        {
          "id" : "<user_id>",
          "user" : {
            "name" : "<user_name>",
            "display_name" : "<display name>"
          }
        }

        :return:

        Constraint:
            * user name cannot be updated
            * name can be max 64 characters
            * display name can be max 128 characters
        """
        pass

    def get_user_teams(self, request: str) -> str:
        """
        :param request:
        {
          "id" : "<user_id>"
        }

        :return: A json list with the response.
        [
          {
            "name" : "<team_name>",
            "description" : "<some description>",
            "creation_time" : "<some date:time format>"
          }
        ]
        """
        pass

# UserManager class
class UserManager(UserBase):
    def __init__(self):
        self.users_file = 'users.json'
        self.users = load_data(self.users_file)

    def create_user(self, request: str) -> str:
        user_data = json.loads(request)
        user_id = str(len(self.users) + 1)
        if user_data['name'] in [user['name'] for user in self.users.values()]:
            raise ValueError("User name must be unique")
        if len(user_data['name']) > 64 or len(user_data['display_name']) > 64:
            raise ValueError("Name or display name exceeds max length")
        self.users[user_id] = {
            "name": user_data['name'],
            "display_name": user_data['display_name'],
            "creation_time": datetime.now().isoformat()
        }
        save_data(self.users_file, self.users)
        return json.dumps({"id": user_id})

    def list_users(self) -> str:
        return json.dumps(list(self.users.values()), indent=4)

    def describe_user(self, request: str) -> str:
        user_id = json.loads(request)['id']
        user = self.users.get(user_id)
        if user:
            return json.dumps(user, indent=4)
        else:
            return json.dumps({"error": "User not found"}, indent=4)

    def update_user(self, request: str) -> str:
        user_data = json.loads(request)
        user_id = user_data['id']
        if user_id not in self.users:
            return json.dumps({"error": "User not found"}, indent=4)
        if len(user_data['user']['display_name']) > 128:
            raise ValueError("Display name exceeds max length")
        self.users[user_id]['display_name'] = user_data['user']['display_name']
        save_data(self.users_file, self.users)
        return json.dumps({"status": "User updated"}, indent=4)

    def get_user_teams(self, request: str) -> str:
        user_id = json.loads(request)['id']
        user = self.users.get(user_id)
        if user:
            teams_file = 'teams.json'
            teams = load_data(teams_file)
            user_teams = [team for team in teams.values() if user_id in team['users']]
            return json.dumps(user_teams, indent=4)
        else:
            return json.dumps({"error": "User not found"}, indent=4)

# Usage Example
if __name__ == "__main__":
    user_manager = UserManager()

    # Create users
    user1 = {
        "name": "john_doe",
        "display_name": "John Doe"
    }
    print(user_manager.create_user(json.dumps(user1)))

    user2 = {
        "name": "jane_smith",
        "display_name": "Jane Smith"
    }
    print(user_manager.create_user(json.dumps(user2)))

    # List users
    print(user_manager.list_users())

    # Describe a user
    print(user_manager.describe_user(json.dumps({"id": "1"})))

    # Update a user
    update_user_data = {
        "id": "1",
        "user": {
            "display_name": "Johnathan Doe"
        }
    }
    print(user_manager.update_user(json.dumps(update_user_data)))

    # List users again to see the update
    print(user_manager.list_users())

    # Get user teams (assuming some teams have been created and assigned)
    print(user_manager.get_user_teams(json.dumps({"id": "1"})))


