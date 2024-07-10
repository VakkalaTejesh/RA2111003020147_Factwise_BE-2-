from bca import BCA,
abstractmethod

class UserBase(BCA):
    """
    Base interface implementation for API's to manage users.
    """

    # create a user
    @abstractmethod
    def create_user(self, user_data) -> str:
        """
        Creates a new user

        Input JSON: 
        {
          "name" : "Mark",
          "display_name" : "Mark Hendry"
        }
        
        Output JSON:
        {
          "user_id":"456"
        }

        Constraint:
            * user name must be unique
            * name can be max 64 characters
            * display name can be max 64 characters
        """
        pass

    # list all users
    @abstractmethod
    def list_users(self, user_data) -> str:
        """
        List the users
        
        Input JSON:
          {
            "name" : "Mark",
            "display_name" : "Mark Hendry",
            "creation_time" : "<24:15:30>"
          }
        
        Output JSON:
        {
          "user_id":"456"
        }
        
        """
        pass

    # describe user
    @abstractmethod
    def describe_user(self, request:user_data) -> str:
        """
        Describes the user
        Input JSON:
        {
          "id" : "456"
        }
        
        Output JSON:
        {
          "name" : "Mark",
          "description" : "A very good developer ",
          "creation_time" : "<24:15:30>"
        }

        """
        pass

    # update user
    @abstractmethod
    def update_user(self, request: user_data) -> str:
        """
        Input JSON:
        {
          "id" : "456",
          "user" : {
            "name" : "Mark",
            "display_name" : "Mark Hendry"
          }
        }

        :return:

        Constraint:
            * user name cannot be updated
            * name can be max 64 characters
            * display name can be max 128 characters
        """
        pass
    @abstractmethod
    def get_user_teams(self, user_id) -> str:
        """
        Retrieves User details
        {
          "user_id" : "456"
        }

        Output JSON:
        [
          {
            "name" : "Computators",
            "description" : "This team objective is to develop a planner tool without any errors",
            "creation_time" : "<24:15:30>"
          }
        ]
        """
        pass

