from mesa import Model, agent
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa import DataCollector
from agent2 import RandomAgent, ObstacleAgent, Trash, Charger

class RandomModel(Model):
    """ 
    Creates a new model with random agents.
    Args:
        N: Number of agents in the simulation
        height, width: The size of the grid to model
    """
    def __init__(self, Numero_de_agentes,densidad_basura, densidad_obstaculos, width=30, height=30):
        self.num_agents = Numero_de_agentes
        self.densidad_basura=densidad_basura
        self.densidad_obstaculos=densidad_obstaculos
        self.steps = 0
        self.grid = MultiGrid(width,height,torus = False) 

        
        self.schedule = RandomActivation(self)
        
        self.running = True 

        self.datacollector = DataCollector( 
        agent_reporters={"Steps": lambda a: a.steps_taken if isinstance(a, RandomAgent) else 0})

        # Creates the border of the grid
       

        # Add obstacles to the grid
        # for pos in border:
        #     obs = ObstacleAgent(pos, self)
        #     self.grid.place_agent(obs, pos)
        
        for contents, (x, y) in self.grid.coord_iter():
            
            if self.random.random() < self.densidad_obstaculos and self.grid.is_cell_empty((x,y)):
                Obs = ObstacleAgent(self.random.randint(0, 1000)+10000, self)
                self.grid.place_agent(Obs, (x,y))

        # Function to generate random positions and IDs
        pos_gen = lambda w, h: (self.random.randrange(w), self.random.randrange(h))
        
        
        # Add trash to the grid
        for contents, (x, y) in self.grid.coord_iter():
            
            if self.random.random() < self.densidad_basura and self.grid.is_cell_empty((x,y)):
                trash = Trash(self.random.randint(0, 1000)+20000, self)
                self.grid.place_agent(trash, (x,y))

        # Add the agent to a random empty grid cell
        for i in range(self.num_agents):
            pos= pos_gen(self.grid.width, self.grid.height)
            while (not self.grid.is_cell_empty(pos)):
                pos = pos_gen(self.grid.width, self.grid.height)
            print(pos)
            a = RandomAgent(i+1000, self, pos)
            C = Charger(i+2000, self, pos) 
            self.schedule.add(a)
            self.schedule.add(C)

            self.grid.place_agent(a, pos)
            self.grid.place_agent(C, pos)
        
        self.datacollector.collect(self)

    def count_trash(self):
        '''Tally the number of trash agents in the grid.'''
        trash_agents = [a for a in self.schedule.agents if isinstance(a, Trash)]
        return len(trash_agents)
    
    

    def step(self):
        '''Advance the model by one step.'''
        self.steps += 1
        self.schedule.step()
        self.datacollector.collect(self)
        
        if self.steps>400:
            self.running = False
        