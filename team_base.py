import json
import os 
from datetime import datetime

DB_DIR ="db"
if not os.path.exists(DB_DIR):
  os.makedirs(DB_DIR)
def load_data(file_name):
  file_path = os.path.join(DB_DIR,file_name)
  if os.path.exists(file_path):
    with open(file_path,'r') as file:
      return json.load(file)
  return{}
def save_data(file_name):
  file_path = os.path.join(DB_DIR,file_name)
  with open(file_path,'w') as file:
     json.dumps(data,file,indent =4)
class TeamBase:
    """
    Base interface implementation for API's to manage teams.
    For simplicity a single team manages a single project. And there is a separate team per project.
    Users can be
    """

    # create a team
    def create_team(self, request: str) -> str:
        """
        :param request: A json string with the team details
        {
          "name" : "<team_name>",
          "description" : "<some description>",
          "admin": "<id of a user>"
        }
        :return: A json string with the response {"id" : "<team_id>"}

        Constraint:
            * Team name must be unique
            * Name can be max 64 characters
            * Description can be max 128 characters
        """
        pass

    # list all teams
    def list_teams(self) -> str:
        """
        :return: A json list with the response.
        [
          {
            "name" : "<team_name>",
            "description" : "<some description>",
            "creation_time" : "<some date:time format>",
            "admin": "<id of a user>"
          }
        ]
        """
        pass

    # describe team
    def describe_team(self, request: str) -> str:
        """
        :param request: A json string with the team details
        {
          "id" : "<team_id>"
        }

        :return: A json string with the response

        {
          "name" : "<team_name>",
          "description" : "<some description>",
          "creation_time" : "<some date:time format>",
          "admin": "<id of a user>"
        }

        """
        pass

    # update team
    def update_team(self, request: str) -> str:
        """
        :param request: A json string with the team details
        {
          "id" : "<team_id>",
          "team" : {
            "name" : "<team_name>",
            "description" : "<team_description>",
            "admin": "<id of a user>"
          }
        }

        :return:

        Constraint:
            * Team name must be unique
            * Name can be max 64 characters
            * Description can be max 128 characters
        """
        pass

    # add users to team
    def add_users_to_team(self, request: str):
        """
        :param request: A json string with the team details
        {
          "id" : "<team_id>",
          "users" : ["user_id 1", "user_id2"]
        }

        :return:

        Constraint:
        * Cap the max users that can be added to 50
        """
        pass

    # add users to team
    def remove_users_from_team(self, request: str):
        """
        :param request: A json string with the team details
        {
          "id" : "<team_id>",
          "users" : ["user_id 1", "user_id2"]
        }

        :return:

        Constraint:
        * Cap the max users that can be added to 50
        """
        pass

    # list users of a team
    def list_team_users(self, request: str):
        """
        :param request: A json string with the team identifier
        {
          "id" : "<team_id>"
        }

        :return:
        [
          {
            "id" : "<user_id>",
            "name" : "<user_name>",
            "display_name" : "<display name>"
          }
        ]
        """
        pass
class TeamManager(TeamBase):
  def __init__(self):
    self.teams = load_data('teams.json')
    self.users = load_data('users.json')
  def create_team(self,request:str)->str:
    team = json.loads(request)
    team_id = str(len(self.teams)+1)
    team['id']=team_id
    team['creation_time'] = datetime.now().isoformat()
    team['members'] = [team['admin']]
     if any(t['name'] == team['name'] for t in self.teams.values()):
            raise ValueError("Team name must be unique.")
        if len(team['name']) > 64:
            raise ValueError("Name can be max 64 characters.")
        if len(team['description']) > 128:
            raise ValueError("Description can be max 128 characters.")

        self.teams[team_id] = team
        save_data('teams.json', self.teams)
        return json.dumps({"id": team_id})

    def list_teams(self) -> str:
        return json.dumps([
            {
                "name": t['name'],
                "description": t['description'],
                "creation_time": t['creation_time'],
                "admin": t['admin']
            }
            for t in self.teams.values()
        ])

    def describe_team(self, request: str) -> str:
        request_data = json.loads(request)
        team_id = request_data['id']
        if team_id not in self.teams:
            raise ValueError("Team not found.")
        team = self.teams[team_id]
        return json.dumps({
            "name": team['name'],
            "description": team['description'],
            "creation_time": team['creation_time'],
            "admin": team['admin']
        })

    def update_team(self, request: str) -> str:
        request_data = json.loads(request)
        team_id = request_data['id']
        team_data = request_data['team']
        if team_id not in self.teams:
            raise ValueError("Team not found.")
        if any(t['name'] == team_data['name'] and t['id'] != team_id for t in self.teams.values()):
            raise ValueError("Team name must be unique.")
        if len(team_data.get('name', '')) > 64:
            raise ValueError("Name can be max 64 characters.")
        if len(team_data.get('description', '')) > 128:
            raise ValueError("Description can be max 128 characters.")

        self.teams[team_id].update(team_data)
        save_data('teams.json', self.teams)
        return json.dumps({"status": "success"})

    def add_users_to_team(self, request: str):
        request_data = json.loads(request)
        team_id = request_data['id']
        user_ids = request_data['users']
        if team_id not in self.teams:
            raise ValueError("Team not found.")
        team = self.teams[team_id]
        if len(team['members']) + len(user_ids) > 50:
            raise ValueError("Cannot add more than 50 members to a team.")
        
        team['members'].extend(user_ids)
        team['members'] = list(set(team['members']))  # Ensure unique members
        save_data('teams.json', self.teams)
        return json.dumps({"status": "success"})

    def remove_users_from_team(self, request: str):
        request_data = json.loads(request)
        team_id = request_data['id']
        user_ids = request_data['users']
        if team_id not in self.teams:
            raise ValueError("Team not found.")
        team = self.teams[team_id]
        team['members'] = [user for user in team['members'] if user not in user_ids]
        save_data('teams.json', self.teams)
        return json.dumps({"status": "success"})

    def list_team_users(self, request: str):
        request_data = json.loads(request)
        team_id = request_data['id']
        if team_id not in self.teams:
            raise ValueError("Team not found.")
        team = self.teams[team_id]
        return json.dumps([
            {
                "id": user_id,
                "name": self.users[user_id]['name'],
                "display_name": self.users[user_id]['display_name']
            }
            for user_id in team['members']
        ])

# Usage Example
if __name__ == "__main__":
    team_manager = TeamManager()

    # Create a team
    team_data = {
        "name": "Development Team",
        "description": "Team working on the project",
        "admin": "1"
    }
    print(team_manager.create_team(json.dumps(team_data)))

    # List all teams
    print(team_manager.list_teams())

    # Describe a team
    print(team_manager.describe_team(json.dumps({"id": "1"})))

    # Update a team
    update_data = {
        "id": "1",
        "team": {
            "name": "Updated Development Team",
            "description": "Updated description",
            "admin": "1"
        }
    }
    print(team_manager.update_team(json.dumps(update_data)))

    # Add users to a team
    add_users_data = {
        "id": "1",
        "users": ["2", "3"]
    }
    print(team_manager.add_users_to_team(json.dumps(add_users_data)))

    # Remove users from a team
    remove_users_data = {
        "id": "1",
        "users": ["2"]
    }
    print(team_manager.remove_users_from_team(json.dumps(remove_users_data)))

    # List users of a team
    print(team_manager.list_team_users(json.dumps({"id": "1"})))
