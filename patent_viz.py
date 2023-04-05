from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule
from patent_model import PatentModel, Licensor, Licensee  # Assuming your model is in a file named `patent_model.py`
from mesa.visualization.UserParam import UserSettableParameter


def agent_portrayal(agent):
    portrayal = {"Shape": "circle", "Filled": "true", "r": 0.5}

    if isinstance(agent, Licensor):
        portrayal["Color"] = "red"
        portrayal["Layer"] = 0
    elif isinstance(agent, Licensee):
        portrayal["Color"] = "blue"
        portrayal["Layer"] = 1

    return portrayal

# Set up the grid dimensions
grid_width, grid_height = 10, 10

# Set up the visualization components
grid = CanvasGrid(agent_portrayal, grid_width, grid_height, 500, 500)
chart = ChartModule([{"Label": "Patents", "Color": "red"},
                     {"Label": "Licenses", "Color": "blue"}],
                     data_collector_name='datacollector')

licensee_money_slider = UserSettableParameter(
    "slider", "Initial Licensee Money", 15, 1, 50, 1
)
patent_creation_chance_slider = UserSettableParameter(
    "slider", "Patent Creation Chance", 0.6, 0, 1, 0.01, description="Chance of new patent creation by licensor"
)

# Set up the server
server = ModularServer(PatentModel,
                       [grid, chart],
                       "Patent Model",
                       {"num_licensors": 20, "num_licensees": 80, "width": grid_width, "height": grid_height, "initial_licensee_money" : licensee_money_slider, "patent_creation_chance": patent_creation_chance_slider})

server.port = 8521  # Set the port to a custom value to avoid potential conflicts
server.launch()
