import mesa
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule, BarChartModule
from disease_model import DiseaseModel
from agents import Person, LandAnimal, FlyingAnimal, AquaticAnimal  # Importa as classes dos agentes

def agent_portrayal(agent):
    portrayal = {
        "Filled": "true",
        "scale": 0.7,
        "Layer": 1
    }

    # Definir a cor do agente
    if isinstance(agent, Person):
        portrayal["Shape"] = f"./assets/person.png"

        # Adicionar indicação de saúde
        portrayal["Saude"] = agent.health

        # Verificar se o agente está infectado
        if agent.disease:
            portrayal["Shape"] = f"./assets/{agent.disease.name}.png"
            portrayal["Saude"] += f" | Infecção: {agent.disease.name}"
    elif isinstance(agent, LandAnimal):
        portrayal["Shape"] = f"./assets/land.png"
    elif isinstance(agent, FlyingAnimal):
        portrayal["Shape"] = f"./assets/flying.png"
    elif isinstance(agent, AquaticAnimal):
        portrayal["Shape"] = f"./assets/aquatic.png"

    # Verificar se o agente está em uma área urbana ou aquática
    cell_info = agent.model.get_cell_info(agent.pos)
    in_urban_area = agent.model.is_urban_area(agent.pos)

    if in_urban_area:
        portrayal["Shape"] = f"./assets/urban.png"
    elif cell_info and cell_info[0] in ["Shallow", "Medium", "Deep"]:
        portrayal["scale"] = 0.8  # Agentes em ambientes aquáticos são maiores

    return portrayal

grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)

# Define um ChartModule para vizualização
chart = ChartModule([{"Label": "Total de Infectados", "Color": "red"}],
                    data_collector_name='datacollector')

agents_chart = BarChartModule([{"Label": "Total de Pessoas", "Color": "black"},
                            {"Label": "Total de Animais Terrestres", "Color": "brown"},
                            {"Label": "Total de Animais Voadores", "Color": "blue"},
                            {"Label": "Total de Animais Aquáticos", "Color": "orange"}
                            ],
                    data_collector_name='agents_datacollector', canvas_width= 700)

model_params = {
    "num_people": mesa.visualization.Slider(
        name="Número de Pessoas",
        min_value=0,
        max_value=50,
        step=1,
        value=5,
    ),
    "num_land_animals": mesa.visualization.Slider(
        name="Número de Animais Terrestres",
        min_value=0,
        max_value=30,
        step=1,
        value=5,
    ),
    "num_flying_animals": mesa.visualization.Slider(
        name="Número de Animais Voadores",
        min_value=0,
        max_value=20,
        step=1,
        value=5,
    ),
    "num_aquatic_animals": mesa.visualization.Slider(
        name="Número de Animais Aquáticos",
        min_value=0,
        max_value=10,
        step=1,
        value=5,
    ),
    "width": 10,
    "height": 10,
}

server = ModularServer(DiseaseModel,
                       [grid, chart, agents_chart],
                       "Disease Spread Simulation",
                       model_params)
server.port = 8000

server.launch()