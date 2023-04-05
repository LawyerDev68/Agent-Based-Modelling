import random
from mesa import Agent, Model
from mesa.time import RandomActivation
import matplotlib.pyplot as plt
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

class Patent:
    def __init__(self, model, licensor, price):
        self.unique_id = model.next_id()
        self.licensor = licensor
        self.price = price
        
    def step(self):
        pass

class License:
    def __init__(self, patent_id, price):
        self.patent_id = patent_id
        self.price = price


class Licensor(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.money = 0
        self.patents = []

    def step(self):
        if random.random() < self.model.patent_creation_chance:
            price = random.randint(5, 10)
            patent = Patent(self.model, self, price)
            self.patents.append(patent)
            self.model.schedule.add(patent)


class Licensee(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.money = random.randint(1, 2 * self.model.initial_licensee_money)
        self.licenses = []

    def step(self):
        licensor = random.choice(self.model.schedule.agents)
        if self.money > 0 and isinstance(licensor, Licensor):
            available_patents = [patent for patent in licensor.patents]
            if available_patents:
                patent = random.choice(available_patents)
                license_price = min(patent.price, self.money)
                self.money -= license_price
                self.licenses.append(patent)
                licensor.money += license_price
        
        # Add chance of money increase
        if random.random() < 0.5:
            self.money += random.randint(1, 5)

    def __str__(self):
        return f'Licensee {self.unique_id}: money={self.money}, licenses={len(self.licenses)}'
    
def count_patents(model):
    return sum([len(agent.patents) for agent in model.schedule.agents if isinstance(agent, Licensor)])

def count_licenses(model):
    return sum([len(agent.licenses) for agent in model.schedule.agents if isinstance(agent, Licensee)])

class PatentModel(Model):
    def __init__(
        self,
        num_licensors,
        num_licensees,
        width,
        height,
        initial_licensee_money,
        patent_creation_chance,
    ):
        self.num_agents = num_licensors + num_licensees
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.current_id = 0
        self.initial_licensee_money = initial_licensee_money
        self.patent_creation_chance = patent_creation_chance

        # Create and add Licensors and Licensees to the schedule
        for i in range(num_licensors):
            licensor = Licensor(self.next_id(), self)
            self.schedule.add(licensor)

        for i in range(num_licensees):
            licensee = Licensee(self.next_id(), self)
            self.schedule.add(licensee)

        self.datacollector = DataCollector(
            model_reporters={"Patents": count_patents, "Licenses": count_licenses}
        )

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()

    def next_id(self):
        self.current_id += 1
        return self.current_id



# Set the number of licensors and licensees in the simulation
num_licensors = 20
num_licensees = 80






