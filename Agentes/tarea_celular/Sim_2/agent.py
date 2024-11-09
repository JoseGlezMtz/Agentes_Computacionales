from mesa import Agent

class Cell(Agent):
    """
        A tree cell.
        
        Attributes:
            x, y: Grid coordinates
            condition: Can be "Fine", "On Fire", or "Burned Out"
            unique_id: (x,y) tuple.

            unique_id isn't strictly necessary here, but it's good practice to give one to each agent anyway.
    """

    def __init__(self, pos, model):
        """
        Create a new tree.

        Args:
            pos: The tree's coordinates on the grid.
            model: standard model reference for agent.
        """
        super().__init__(pos, model)
        self.pos = pos
        self.condition = "Death"
        self._next_condition = None
       

    def step(self):
        """
        If the tree is on fire, spread it to fine trees nearby.
        """
        neighbor1=""
        neighbor2=""
        neighbor3=""
        State_map={"AliveAliveAlive": "Death",
                   "AliveAliveDeath": "Alive",
                   "AliveDeathAlive": "Death",
                   "AliveDeathDeath": "Alive",
                   "DeathAliveAlive": "Alive",
                   "DeathAliveDeath": "Death",
                   "DeathDeathAlive": "Alive",
                   "DeathDeathDeath": "Death"}
        
        state_hermanos=[]
        
        print("Posicion actual: ", self.pos)
        
          
        for neighbor in self.model.grid.iter_neighbors(self.pos, True):
            print ("Vecino: ", neighbor.pos) 
            state_hermanos.append(neighbor.condition)
        
        neighbor1=state_hermanos[2]
        neighbor2=state_hermanos[4]
        neighbor3=state_hermanos[7]
        self._next_condition = State_map[neighbor1+neighbor2+neighbor3]    
            
                        
    
    def advance(self):
        """
        Advance the model by one step.
        """
        if (self._next_condition is not None):
            self.condition = self._next_condition