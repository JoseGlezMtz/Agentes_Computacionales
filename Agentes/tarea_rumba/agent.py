from mesa import Agent

class RandomAgent(Agent):
    """
    Agent that moves randomly.
    Attributes:
        unique_id: Agent's ID 
        direction: Randomly chosen direction chosen from one of eight directions
    """
    def __init__(self, unique_id, model,pos):
        """
        Creates a new random agent.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
        """
        super().__init__(unique_id, model)
        self.steps_taken = 0
        self.pos = pos
        self.next_pos=[]
        self.Trash_moves=[]

    def move(self):
        """ 
        Determines if the agent can move in the direction that was chosen
        """

        empty_moves = []
       
        # next_move = self.random.choice(next_moves)
        
        for neighbor in self.model.grid.iter_neighborhood(self.pos, moore=True):
            print(neighbor)
            get_cont = self.model.grid.get_cell_list_contents(neighbor)
            if not get_cont:
                empty_moves.append(neighbor)
                
            elif isinstance(get_cont[0],Trash):
                self.Trash_moves.append(neighbor)

        # Now move:
        if self.Trash_moves:
            self.model.grid.move_agent(self, self.random.choice(self.Trash_moves))
        else:
            self.model.grid.move_agent(self, self.random.choice(empty_moves))

    def step(self):
        """ 
        Determines the new direction it will take, and then moves
        """
        this_cell=self.model.grid.get_cell_list_contents([self.pos])
        trash_cell=[obj for obj in this_cell if isinstance(obj,Trash)]
        
        if len(trash_cell)>0:
            delete_trash=self.random.choice(trash_cell)
            
            self.model.grid.remove_agent(delete_trash)
            self.model.schedule.remove(delete_trash)
            
        else: 
            self.move()

class ObstacleAgent(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass  
    
class Trash(Agent):
    
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        
    def step(self):
        pass