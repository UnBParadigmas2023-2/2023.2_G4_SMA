from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid
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

server = ModularServer(DiseaseModel,
                       [grid],
                       "Disease Spread Simulation",
                       {"num_people": 50, "num_land_animals": 30, "num_flying_animals": 20, "num_aquatic_animals": 10, "width": 10, "height": 10})
server.port = 8000

server.launch()
