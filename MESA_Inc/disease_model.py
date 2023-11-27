from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from agents import Person, LandAnimal, FlyingAnimal, AquaticAnimal
import random

class DiseaseModel(Model):
    def __init__(self, num_people, num_land_animals, num_flying_animals, num_aquatic_animals, width, height):
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)

        # Inicializa um mapa de áreas urbanas
        self.urban_areas = self.initialize_urban_areas(width, height)
        self.cell_info = self.initialize_cell_info()

        # Cria pessoas
        for i in range(num_people):
            a = Person(i, self)
            self.place_agent_randomly(a)

        # Cria animais terrestres
        for i in range(num_people, num_people + num_land_animals):
            a = LandAnimal(i, self)
            self.place_agent_randomly(a)

        # Cria animais voadores
        for i in range(num_people + num_land_animals, num_people + num_land_animals + num_flying_animals):
            a = FlyingAnimal(i, self)
            self.place_agent_randomly(a)

        # Cria animais aquáticos
        for i in range(num_people + num_land_animals + num_flying_animals, num_people + num_land_animals + num_flying_animals + num_aquatic_animals):
            a = AquaticAnimal(i, self)
            self.place_agent_randomly(a)

    def place_agent_randomly(self, agent):
        x = self.random.randrange(self.grid.width)
        y = self.random.randrange(self.grid.height)
        self.grid.place_agent(agent, (x, y))
        self.schedule.add(agent)