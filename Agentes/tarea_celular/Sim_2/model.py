import mesa
from mesa import Model, DataCollector
from mesa.space import SingleGrid
from mesa.time import SimultaneousActivation 
import random

from agent import Cell

class RandomCells(Model):
    """
        Simple Forest Fire model.

        Attributes:
            height, width: Grid size.
            density: What fraction of grid cells have a tree in them.
    """

    def __init__(self, height=50, width=50, density=0.65):
        """
        Create a new forest fire model.
        
        Args:
            height, width: The size of the grid to model
            density: What fraction of grid cells have a tree in them.
        """

        
        self.schedule = SimultaneousActivation(self)
        self.grid = SingleGrid(height, width, torus=True)
        self.Step_count=0

        
        self.datacollector = DataCollector(
            {
                "Alive": lambda m: self.count_type(m, "Alive"),
                "Death": lambda m: self.count_type(m, "Death"),
            }
        )

        
        for contents, (x, y) in self.grid.coord_iter():
            
            
            new_cell = Cell((x, y), self)
            
            if  random.random() < density:
                new_cell.condition ="Alive"
        
            self.grid.place_agent(new_cell, (x, y))
            self.schedule.add(new_cell)

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        """
        Have the scheduler advance each cell by one step
        """
        self.schedule.step()
        
        self.datacollector.collect(self)

        
        self.Step_count+=1
        if self.Step_count==50:
            self.running = False

    
    @staticmethod
    def count_type(model, tree_condition):
        """
        Helper method to count trees in a given condition in a given model.
        """
        count = 0
        for tree in model.schedule.agents:
            if tree.condition == tree_condition:
                count += 1
        return count