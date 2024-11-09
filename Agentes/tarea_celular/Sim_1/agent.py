from mesa import Agent

class Cell(Agent):
    

    def __init__(self, pos, model):
       
        super().__init__(pos, model)
        self.pos = pos
        self.condition = "Death"
        self._next_condition = None
       

    def step(self):
        
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
        
        
        
        if (self.pos[0] < self.model.grid.width-1 and  self.pos[0] > 0) and self.pos[1] != 49:
            
            for neighbor in self.model.grid.iter_neighbors(self.pos, True):
                
                if neighbor.pos[1] == self.pos[1]+1:
                    
                    if neighbor.pos[0] == self.pos[0]-1:
                        neighbor1 = neighbor.condition
                        
                    elif neighbor.pos[0] == self.pos[0]:
                        neighbor2 = neighbor.condition
                        
                    elif neighbor.pos[0] == self.pos[0]+1:
                        neighbor3 = neighbor.condition
            
            
            self._next_condition = State_map[neighbor1+neighbor2+neighbor3]    
            
                        
    
    def advance(self):
        """
        Advance the model by one step.
        """
        if (self._next_condition is not None):
            self.condition = self._next_condition