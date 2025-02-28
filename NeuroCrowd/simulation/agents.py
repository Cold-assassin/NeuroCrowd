import numpy as np
from mesa import Agent

class AdvancedPilgrim(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.speed = np.clip(np.random.normal(1.0, 0.3), 0.5, 2.0)
        self.panic = 0
        self.pos = (np.random.randint(0, 49), np.random.randint(0, 49))
        
        # Personality matrix
        self.personality = {
            'neuroticism': np.random.uniform(0, 1),
            'compliance': np.random.uniform(0.5, 1)
        }

    def step(self):
        # Simplified movement for demo
        new_x = self.pos[0] + np.random.choice([-1, 0, 1])
        new_y = self.pos[1] + np.random.choice([-1, 0, 1])
        new_pos = (new_x % 50, new_y % 50)
        self.model.grid.move_agent(self, new_pos)
        
        # Update panic
        neighbors = self.model.grid.get_neighbors(self.pos, moore=True, radius=2)
        self.panic = min(100, len(neighbors) * 5 * self.personality['neuroticism'])