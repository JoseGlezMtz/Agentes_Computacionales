from model import RandomModel, ObstacleAgent, Trash, Charger, RandomAgent
from mesa.visualization import CanvasGrid, BarChartModule
from mesa.visualization import ModularServer
import mesa 

def agent_portrayal(agent):
    if agent is None: return
    
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 1,
                 "Color": "red",
                 "r": 0.5
                 }

    if (isinstance(agent, RandomAgent)):
         
         portrayal["text"]= round(agent.energy, 1)
         portrayal["text_color"]= "black"
        
    if (isinstance(agent, ObstacleAgent)):
        portrayal["Color"] = "grey"
        portrayal["Layer"] = 2
        portrayal["r"] = 0.2
    
    elif (isinstance(agent, Trash)):
        portrayal["Color"] = "blue"
        portrayal["Layer"] = 0
        portrayal["r"] = 0.4
    
    elif (isinstance(agent, Charger)):
        portrayal["Color"] = "green"
        portrayal["Layer"] = 0
        portrayal["r"] = 0.4

    return portrayal

model_params = {"N":5, "width":10, "height":10}
canvas_element = mesa.visualization.CanvasGrid(agent_portrayal, 50, 50, 500, 500)
model_params = {
    # The following line is an example to showcase StaticText.
    "title": mesa.visualization.StaticText("Parameters:"),
    "Numero_de_agentes": mesa.visualization.Slider("Numero_de_agentes", 5, 1, 10),
    "densidad_basura": mesa.visualization.Slider("densidad_basura", 0.4, 0.01, 1.0, 0.01),
    "densidad_obstaculos": mesa.visualization.Slider("densidad_obstaculos", 0.2, 0.01, 1.0, 0.01),
}


grid = CanvasGrid(agent_portrayal, 30, 30, 500, 500)

bar_chart = BarChartModule(
    [{"Label":"Steps", "Color":"#AA0000"}], 
    scope="agent", sorting="ascending", sort_by="Steps")

server = ModularServer(RandomModel, [grid, bar_chart], "Random Agents", model_params)
                       
server.port = 8521 # The default
server.launch()