from mesa import Model
from mesa.datacollection import DataCollector
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from agents import *
import random

# Começo das funções de DataCollector

def get_total_num_person(model):
    # Checa quantas pessoas existem no total
    num_people = sum(1 for a in model.schedule.agents if isinstance(a, Person))
    return num_people

def get_total_num_land_animal(model):
    # Checa quantos animais terrestres existem no total
    num_land_animals = sum(1 for a in model.schedule.agents if isinstance(a, LandAnimal))
    return num_land_animals

def get_total_num_flying_animals(model):
    # Checa quantos animais voadores existem no total
    num_flying_animals = sum(1 for a in model.schedule.agents if isinstance(a, FlyingAnimal))
    return num_flying_animals

def get_total_num_aquatic_animals(model):
    # Checa quantos animais aquáticos existem no total
    num_aquatic_animals = sum(1 for a in model.schedule.agents if isinstance(a, AquaticAnimal))
    return num_aquatic_animals

def get_num_infected_person(model):
    # Checa quantas pessoas estão infectadas por qualquer doença
    infected_agents = [a for a in model.schedule.agents if isinstance(a, Person) and a.disease]
    return len(infected_agents)

class DiseaseModel(Model):
    def __init__(self, num_people, num_land_animals, num_flying_animals, num_aquatic_animals, width, height):
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)

        # Inicializa um mapa de áreas urbanas
        self.urban_areas = self.initialize_urban_areas(width, height)
        self.cell_info = self.initialize_cell_info()

        start_unique_id = 0
        start_unique_id = self.initial_infected_people(num_people, covid19, 0.15, start_unique_id)
        start_unique_id = self.initial_infected_people(num_people, influenza, 0.1, start_unique_id)
        start_unique_id = self.initial_infected_people(num_people, common_cold, 0.3, start_unique_id)
        start_unique_id = self.initial_infected_people(num_people, coqueluche, 0.01, start_unique_id)
        start_unique_id = self.initial_infected_people(num_people, hanseniase, 0.03, start_unique_id)
        start_unique_id = self.initial_infected_people(num_people, conjuntivite, 0.05, start_unique_id)

        # Cria animais terrestres
        for i in range(num_people, num_people + num_land_animals):
            a = LandAnimal(start_unique_id, self)
            start_unique_id += 1
            self.place_agent_randomly(a)

        # Cria animais voadores
        for i in range(num_people + num_land_animals, num_people + num_land_animals + num_flying_animals):
            a = FlyingAnimal(start_unique_id, self)
            start_unique_id += 1
            self.place_agent_randomly(a)

        # Cria animais aquáticos
        for i in range(num_people + num_land_animals + num_flying_animals, num_people + num_land_animals + num_flying_animals + num_aquatic_animals):
            a = AquaticAnimal(start_unique_id, self)
            start_unique_id += 1
            self.place_agent_randomly(a)

        # Inicializa um Data Collector
        self.datacollector = DataCollector(
            model_reporters={
                "Total de Infectados": get_num_infected_person
            },
        )

        self.agents_datacollector = DataCollector(
            model_reporters={
                "Total de Pessoas": get_total_num_person,
                "Total de Animais Terrestres": get_total_num_land_animal,
                "Total de Animais Voadores": get_total_num_flying_animals,
                "Total de Animais Aquáticos": get_total_num_aquatic_animals,
            },
        )

    def initial_infected_people(self, num_people, name_disease, percent_initial, start_unique_id):
        for x in range(num_people):
            unique_id = start_unique_id
            start_unique_id += 1
            if x < num_people * percent_initial:
                a = Person(unique_id, self, disease=name_disease)
            else:
                a = Person(unique_id, self)
            self.place_agent_randomly(a)

        return start_unique_id

    def place_agent_randomly(self, agent):
        x = self.random.randrange(self.grid.width)
        y = self.random.randrange(self.grid.height)
        if self.grid.is_cell_empty((x, y)):
            self.grid.place_agent(agent, (x, y))
            self.schedule.add(agent)

        

    def initialize_urban_areas(self, width, height):
        # Aqui você pode definir as áreas urbanas
        # Por exemplo, você pode definir uma porcentagem das células como urbanas
        urban_area_percentage = 0.2  # 20% das células
        total_cells = width * height
        num_urban_cells = int(total_cells * urban_area_percentage)

        urban_cells = set()
        while len(urban_cells) < num_urban_cells:
            x = random.randrange(width)
            y = random.randrange(height)
            urban_cells.add((x, y))

        return urban_cells

    def is_urban_area(self, pos):
        return pos in self.urban_areas
    
    def initialize_cell_info(self):
        # Define as informações para cada célula
        info = {}
        for x in range(self.grid.width):
            for y in range(self.grid.height):
                # Define a profundidade e qualidade da água para cada célula
                # Exemplo: profundidade varia de 1 a 3 e qualidade da água varia entre "Clean", "Murky" e "Polluted"
                depth = random.choice(["Shallow", "Medium", "Deep"])
                water_quality = random.choice(["Clean", "Murky", "Polluted"])
                info[(x, y)] = (depth, water_quality)
        return info

    def get_cell_info(self, pos):
        # Retorna as informações da célula para a posição dada
        return self.cell_info.get(pos, (None, None))
    
    def step(self):
        self.datacollector.collect(self)
        self.agents_datacollector.collect(self)
        self.schedule.step()
