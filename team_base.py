from bca import BCA,
abstractmethod

class TeamBase(BCA):
  @abstractmethod
    """
    Base interface implementation for API's to manage teams.
    For simplicity a single team manages a single project. And there is a separate team per project.
    Users can be
    """

    # create a team
    def create_team(self, team_data) -> str:
        """
        Creates a new team.

        Input JSON:
        {
          "team_name" : "Coders",
          "team_description" : "This team objective is to develop a planner tool",
          "team_members":["121","125"]
          "admin": "<1234>"
        }
        Output JSON:
        {
          "team_id":"Coders@234"
        }
        
        Constraint:
            * Team name must be unique
            * Name can be max 64 characters
            * Description can be max 128 characters
        """
        pass

    # list all teams
    @abstractmethod
    def list_teams(self, team_data) -> str:
        """
        
        Input JSON:
        {
          "team_id":"456"
        } 
        Output JSON:
        {
            "name" : "Coders",
            "description" : "This team objective is to develop a planner tool",
            "creation_time" : "<24:15:30>",
            "admin": "1234"
        }
        
        """
        pass

    # describe team
    @abstractmethod
    def describe_team(self, team_data) -> str:
        """
        Input JSON:
        {
          "id" : "456"
        }

        Output JSON:

        {
          "name" : "Coders",
          "description" : "This team objective is to develop a planner tool",
          "creation_time" : "<24:15:30>",
          "admin": "1234"
        }

        """
        pass

    # update team
    @abstractmethod
    def update_team(self, team_data) -> str:
        """
        Input JSON:
        {
          "id" : "456",
          "team" : {
            "name" : "Computators",
            "description" : "This team objective is to develop a planner tool without any errors",
            "admin": "1234@"
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
    @abstractmethod
    def add_users_to_team(self, team_data):
        """
        Input JSON:
        {
          "id" : "456",
          "users" : ["121", "125"]
        }

        :return:

        Constraint:
        * Cap the max users that can be added to 50
        """
        pass

    # add users to team
    @abstractmethod
    def remove_users_from_team(self, team_data):
        """
        Input JSON:
        {
          "id" : "<456>",
          "users" : ["121", "125"]
        }

        :return:

        Constraint:
        * Cap the max users that can be added to 50
        """
        pass

    # list users of a team
    @abstractmethod
    def list_team_users(self, team_data):
        """
        Input JSON:
        {
          "id" : "<456>"
        }

        Output JSON:
        [
          {
            "id" : "125",
            "name" : "Mark",
            "display_name" : "Mark Hendry"
          }
        ]
        """
        pass

