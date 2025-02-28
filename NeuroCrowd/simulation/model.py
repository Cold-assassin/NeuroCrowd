from mesa import Model, space, time
from .agents import AdvancedPilgrim
from config.settings import Config

class CrowdModel(Model):
    def __init__(self):
        self.grid = space.MultiGrid(Config.GRID_WIDTH, Config.GRID_HEIGHT, True)
        self.schedule = time.RandomActivation(self)
        
        # Create agents
        for i in range(Config.INITIAL_AGENTS):
            agent = AdvancedPilgrim(i, self)
            self.grid.place_agent(agent, agent.pos)
            self.schedule.add(agent)

    def step(self):
        self.schedule.step()