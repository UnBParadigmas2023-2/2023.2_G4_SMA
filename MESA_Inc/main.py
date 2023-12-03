# main.py
from disease_model import DiseaseModel

# Configurar os parâmetros da simulação
num_people = 50
num_land_animals = 30
num_flying_animals = 20
num_aquatic_animals = 10
width, height = 10, 10  # Defina o tamanho da grade (grid) aqui

# Criar o modelo
model = DiseaseModel(num_people, num_land_animals, num_flying_animals, num_aquatic_animals, width, height)

# Executar a simulação por um número específico de passos
for i in range(20):  # Aqui definimos 20 passos, mas você pode ajustar conforme necessário
    model.step()
