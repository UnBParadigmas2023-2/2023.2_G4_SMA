from mesa import Agent
import random

class Disease:
    def __init__(self, name, transmission_rate, incubation_period, severity):
        self.name = name
        self.transmission_rate = transmission_rate
        self.incubation_period = incubation_period
        self.severity = severity

class Person(Agent):
    def __init__(self, unique_id, model, disease=None):
        super().__init__(unique_id, model)
        self.age = random.randint(0, 100)
        self.health = random.choice(["Boa", "Média", "Ruim"])
        self.mobility = random.choice(["High", "Medium", "Low"])
        self.occupation = random.choice(["Student", "Worker", "Retired"])
        self.vaccinated = random.choice([True, False])
        self.social_behaviour = random.choice(["Social", "Reserved"])
        self.disease = disease  # Adicionando a referência à doença

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,   # Considera todas as 8 direções
            include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def step(self):
        self.move()  # Movimentação do agente a cada etapa
        

class LandAnimal(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.species = random.choice(["Deer", "Fox", "Rabbit"])
        self.speed = random.randint(1, 10)
        self.food_search = random.choice(["Active", "Passive"])
        self.habitat_preference = random.choice(["Forest", "Field", "Urban"])
        self.health_status = random.choice(["Healthy", "Carrier", "Sick"])
        self.interaction_rate = random.randint(1, 5)

    def move(self):
            # Define probabilidades de movimento com base no estado de saúde
            move_to_urban = 0.1 if self.health_status in ["Healthy", "Carrier"] else 0.3

            possible_steps = self.model.grid.get_neighborhood(
                self.pos,
                moore=True,
                include_center=False)

            # Probabilidade maior de mover-se para áreas urbanas se o animal estiver doente
            urban_steps = [step for step in possible_steps if self.model.is_urban_area(step)]
            non_urban_steps = [step for step in possible_steps if not self.model.is_urban_area(step)]

            if random.random() < move_to_urban and urban_steps:
                new_position = self.random.choice(urban_steps)
            else:
                new_position = self.random.choice(non_urban_steps)

            self.model.grid.move_agent(self, new_position)

    def step(self):
        self.move()  # Movimentação do agente a cada etapa


class FlyingAnimal(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.species = random.choice(["Eagle", "Sparrow", "Bat"])
        self.wing_span = random.uniform(0.5, 2.0)  # Em metros
        self.altitude_preference = random.choice(["Low", "Medium", "High"])
        self.health_status = random.choice(["Healthy", "Carrier", "Sick"])
        self.migration_pattern = random.choice(["Nomadic", "Seasonal", "Stationary"])
        self.social_behavior = random.choice(["Solitary", "Flock", "Occasional Groups"])

    def move(self):
        # Define probabilidades de movimento com base na altitude e saúde
        lower_altitude_move = 0.2 if self.health_status == "Healthy" else 0.5

        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)

        # Movimento mais frequente em altitudes baixas para agentes doentes
        if self.altitude_preference == "Low" or (self.health_status == "Sick" and random.random() < lower_altitude_move):
            new_position = self.choose_low_altitude_move(possible_steps)
        else:
            new_position = self.choose_high_altitude_move(possible_steps)

        self.model.grid.move_agent(self, new_position)

    def choose_low_altitude_move(self, possible_steps):
            # Em baixa altitude, foco em interações - escolhe célula com mais vizinhos
            most_populated_step = None
            max_neighbors = -1

            for step in possible_steps:
                neighbors = self.model.grid.get_cell_list_contents(step)
                if len(neighbors) > max_neighbors:
                    max_neighbors = len(neighbors)
                    most_populated_step = step

            # Se houver uma célula claramente mais povoada, mova-se para lá, senão escolha aleatoriamente
            return most_populated_step if most_populated_step is not None else self.random.choice(possible_steps)

    def choose_high_altitude_move(self, possible_steps):
        # Em altas altitudes, o movimento depende do padrão migratório
        if self.migration_pattern == "Nomadic":
            # Para nômades, movimento aleatório
            return self.random.choice(possible_steps)
        elif self.migration_pattern == "Seasonal":
            # Para migração sazonal, movimento direcionado (simplificado para movimento aleatório aqui)
            return self.random.choice(possible_steps)
        else:  # Stationary
            # Para estacionários, movimento próximo à posição atual
            if possible_steps:
                return min(possible_steps, key=lambda step: self.distance_from_current(step))
            else:
                return self.pos

    def distance_from_current(self, step):
        # Calcula a distância Manhattan da posição atual
        return abs(step[0] - self.pos[0]) + abs(step[1] - self.pos[1])

    def step(self):
        self.move()  # Movimentação do agente a cada etapa

        
class AquaticAnimal(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.species = random.choice(["Fish", "Frog", "Turtle"])
        self.swim_speed = random.randint(1, 10)
        self.depth_preference = random.choice(["Shallow", "Medium", "Deep"])
        self.health_status = random.choice(["Healthy", "Carrier", "Sick"])
        self.social_behavior = random.choice(["Solitary", "Group", "School"])
        self.water_quality_preference = random.choice(["Clean", "Murky", "Polluted"])

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)

        preferred_steps = self.filter_steps_by_preferences(possible_steps)
        if preferred_steps:  # Certifique-se de que há passos preferidos disponíveis
            new_position = self.random.choice(preferred_steps)
            self.model.grid.move_agent(self, new_position)

    def filter_steps_by_preferences(self, possible_steps):
        # Filtrar os passos com base na preferência de profundidade e qualidade da água
        filtered_steps = []
        for step in possible_steps:
            depth, water_quality = self.model.get_cell_info(step)  # Assumindo que esta função retorna informações da célula

            # Verificar se a célula corresponde às preferências do agente
            if depth == self.depth_preference and water_quality == self.water_quality_preference:
                filtered_steps.append(step)

        return filtered_steps

    def step(self):
        self.move()  # Movimentação do agente a cada etapa
covid19 = Disease(name="COVID-19", transmission_rate=0.3, incubation_period=14, severity="Severe")
influenza = Disease(name="Influenza", transmission_rate=0.2, incubation_period=7, severity="Moderate")
common_cold = Disease(name="Gripe", transmission_rate=0.1, incubation_period=5, severity="Mild")
