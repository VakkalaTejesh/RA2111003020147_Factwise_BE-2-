from bca import BCA,
abstractmethod

class ProjectBoardBase(BCA):
    """
    A project board is a unit of delivery for a project. Each board will have a set of tasks assigned to a user.
    """

    # create a board
    @abstractmethod
    def create_board(self, board_data):
        """
        Input JSON:
        {
            "name" : "Directory",
            "description" : "This Board is to examine the users",
            "team_id" : "456"
            "creation_time" : "<21:12:28>"
        }
        
        Output JSON:
        {
          "board_id":"274"
        }

        Constraint:
         * board name must be unique for a team
         * board name can be max 64 characters
         * description can be max 128 characters
        """
        pass

    # close a board
    @abstractmethod
    def close_board(self, board_data) -> str:
        """
        Input JSON:
        {
          "id" : "274"
        }

        :return:

        Constraint:
          * Set the board status to CLOSED and record the end_time date:time
          * You can only close boards with all tasks marked as COMPLETE
        """
        pass

    # add task to board
    @abstractmethod
    def add_task(self, board_id) -> str:
        """
        Input JSON:
        {
            "title" : "Directory",
            "description" : "This Board is to examine the users",
            "user_id" : "274"
            "creation_time" : "<21:12:48>"
        }
        Output JSON:
        {
          "task_id":"274"
        }

        Constraint:
         * task title must be unique for a board
         * title name can be max 64 characters
         * description can be max 128 characters

        Constraints:
        * Can only add task to an OPEN board
        """
        pass

    # update the status of a task
    @abstractmethod
    def update_task_status(self, board_id):
        """
        Input JSON:
        {
            "id" : "274",
            "status" : "OPEN | IN_PROGRESS | COMPLETE"
        }
        """
        pass

    # list all open boards for a team
    @abstractmethod
    def list_boards(self, board_data) -> str:
        """
        Input JSON:
        {
          "id" : "274"
        }

        Output JSON:
        [
          {
            "id" : "274",
            "name" : "Directory"
          }
        ]
        """
        pass
    @abstractmethod
    def export_board(self, board_data) -> str:
        """
        Export a board in the out folder. The output will be a txt file.
        We want you to be creative. Output a presentable view of the board and its tasks with the available data.
        Input JSON:
        {
          "id" : "274"
        }
        Output JSON
        {
          "out_file" : "Mark's Data"
        }
        """
        pass
