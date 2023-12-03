from mesa import Agent
import random

class Disease:
    def __init__(self, name, transmission_rate, incubation_period, severity, causer):
        self.name = name
        self.transmission_rate = transmission_rate
        self.incubation_period = incubation_period
        self.severity = severity
        self.causer = causer

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
        self.incubation_period = None  # Inicializa com None

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,   # Considera todas as 8 direções
            include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def try_to_infect(self):
            if self.disease is not None:
                cellmates = self.model.grid.get_cell_list_contents([self.pos])
                for other_agent in cellmates:
                    if isinstance(other_agent, Person) and other_agent.disease is None:
                        if random.random() < self.disease.transmission_rate:
                            other_agent.disease = self.disease
                            

    def update_disease_state(self):
        
        if self.disease is not None and self.disease.incubation_period is not None:
                self.disease.incubation_period -= 1

                if self.disease.incubation_period <= 0:
                    if self.disease is not None:
                        # Decrementa o período de incubação
                        self.disease.incubation_period -= 1

                        if self.disease.incubation_period <= 0:
                            # Estado da doença muda para sintomático
                            self.disease_status = "Sintomático"

                            # Decisão sobre a recuperação ou agravamento da doença
                            chance_of_recovery = 0.8  # Exemplo: 80% de chance de recuperação
                            if random.random() < chance_of_recovery:
                                # Recuperação do agente
                                self.disease = None
                                self.disease_status = "Recuperado"
                            else:
                                # Agravamento da doença
                                self.disease_status = "Grave"

    def step(self):
        self.move()
        self.try_to_infect()
        self.update_disease_state()
        

class LandAnimal(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.species = random.choice(["Deer", "Fox", "Rabbit"])
        self.speed = random.randint(1, 10)
        self.food_search = random.choice(["Active", "Passive"])
        self.habitat_preference = random.choice(["Forest", "Field", "Urban"])
        self.health_status = random.choice(["Healthy", "Carrier", "Sick"])
        self.interaction_rate = random.randint(1, 5)
        self.incubation_period = None  # Inicializa com None

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

    def try_to_infect(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        for other_agent in cellmates:
            if isinstance(other_agent, LandAnimal) and other_agent.health_status != "Sick" and self.health_status == "Sick":
                if random.random() < 0.1:  # Exemplo de taxa de transmissão
                    other_agent.health_status = "Sick"
                    # Aqui, você pode definir um período de incubação para o outro agente
                    other_agent.incubation_period = 5  # Exemplo de período de incubação

    def update_disease_state(self):
        
        if self.health_status == "Sick" and self.incubation_period is not None:
            self.incubation_period -= 1

            if self.incubation_period <= 0:
                # Verifica se o animal está doente
                if self.health_status == "Sick":
                    # Decrementa o período de incubação
                    self.incubation_period -= 1

                    if self.incubation_period <= 0:
                        # O animal agora está sintomático
                        self.symptomatic = True

                        # Decidir a recuperação ou agravamento
                        chance_of_recovery = 0.7  # Exemplo: 70% de chance de recuperação
                        if random.random() < chance_of_recovery:
                            # O animal se recupera
                            self.health_status = "Healthy"
                            self.symptomatic = False
                        else:
                            # A doença se agrava
                            self.health_status = "Gravely Sick"

    def step(self):
        self.move()
        self.try_to_infect()
        self.update_disease_state()


class FlyingAnimal(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.species = random.choice(["Eagle", "Sparrow", "Bat"])
        self.wing_span = random.uniform(0.5, 2.0)  # Em metros
        self.altitude_preference = random.choice(["Low", "Medium", "High"])
        self.health_status = random.choice(["Healthy", "Carrier", "Sick"])
        self.migration_pattern = random.choice(["Nomadic", "Seasonal", "Stationary"])
        self.social_behavior = random.choice(["Solitary", "Flock", "Occasional Groups"])
        self.incubation_period = None  # Inicializa com None

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
    
    def try_to_infect(self):
        if self.health_status == "Sick" and self.incubation_period is not None:
            if self.incubation_period > 0:
                self.incubation_period -= 1
            else:
                cellmates = self.model.grid.get_cell_list_contents([self.pos])
                for other_agent in cellmates:
                    if isinstance(other_agent, FlyingAnimal) and other_agent.health_status != "Sick":
                        if random.random() < 0.05:  # Exemplo de taxa de transmissão
                            other_agent.health_status = "Sick"
                            other_agent.incubation_period = 7

    def update_disease_state(self):
        if self.health_status == "Sick" and self.incubation_period is not None:
            self.incubation_period -= 1

            if self.incubation_period <= 0:
                self.symptomatic = True

                # Decidir a recuperação ou agravamento
                chance_of_recovery = 0.6  # Exemplo: 60% de chance de recuperação
                if random.random() < chance_of_recovery:
                    self.health_status = "Healthy"
                    self.symptomatic = False
                else:
                    self.health_status = "Gravely Sick"

    def step(self):
        self.move()
        self.try_to_infect()
        self.update_disease_state()

        
class AquaticAnimal(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.species = random.choice(["Fish", "Frog", "Turtle"])
        self.swim_speed = random.randint(1, 10)
        self.depth_preference = random.choice(["Shallow", "Medium", "Deep"])
        self.health_status = random.choice(["Healthy", "Carrier", "Sick"])
        self.social_behavior = random.choice(["Solitary", "Group", "School"])
        self.water_quality_preference = random.choice(["Clean", "Murky", "Polluted"])
        self.incubation_period = None  # Inicializa com None

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
    
    def try_to_infect(self):
        if self.health_status == "Sick" and self.incubation_period is not None:
            if self.incubation_period > 0:
                self.incubation_period -= 1
            else:
                cellmates = self.model.grid.get_cell_list_contents([self.pos])
                for other_agent in cellmates:
                    if isinstance(other_agent, AquaticAnimal) and other_agent.health_status != "Sick":
                        water_quality = self.model.get_cell_info(self.pos)[1]
                        transmission_rate = 0.05 if water_quality == "Clean" else 0.1
                        if random.random() < transmission_rate:
                            other_agent.health_status = "Sick"
                            other_agent.incubation_period = 5
                        
    def update_disease_state(self):
        if self.health_status == "Sick" and self.incubation_period is not None:
            self.incubation_period -= 1

            if self.incubation_period <= 0:
                self.symptomatic = True

                # Decidir a recuperação ou agravamento
                chance_of_recovery = 0.5  # Exemplo: 50% de chance de recuperação
                if random.random() < chance_of_recovery:
                    self.health_status = "Healthy"
                    self.symptomatic = False
                else:
                    self.health_status = "Gravely Sick"

    def step(self):
        self.move()
        self.try_to_infect()
        self.update_disease_state()
        
        
        
covid19 = Disease(name="COVID-19", transmission_rate=0.3, incubation_period=14, severity="Severe", causer="virus")
influenza = Disease(name="Influenza", transmission_rate=0.2, incubation_period=7, severity="Moderate", causer="virus")
common_cold = Disease(name="Gripe", transmission_rate=0.1, incubation_period=5, severity="Mild", causer="virus")
coqueluche = Disease(name="Coqueluche", transmission_rate=0.8, incubation_period=14, severity="Severe", causer="bacterium")
hanseniase = Disease(name="Hanseníase", transmission_rate=0.24 ,incubation_period=730, severity="Moderate", causer="bacterium")
conjuntivite = Disease(name="conjuntivite", transmission_rate=0.08 ,incubation_period=15, severity="Mild", causer="virus")
