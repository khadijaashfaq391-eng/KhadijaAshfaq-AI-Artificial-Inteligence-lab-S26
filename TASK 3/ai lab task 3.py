class ModelBasedReflexAgent:

    def __init__(self, desired_temperature):
        self.desired_temperature = desired_temperature
        self.previous_action = {}   

    def perceive(self, current_temperature):
        return current_temperature

    def act(self, room, current_temperature):

        if current_temperature < self.desired_temperature:
            action = "Turn on heater"
        else:
            action = "Turn off heater"

        
        if room in self.previous_action:
            if self.previous_action[room] == action:
                return "No change needed"


        self.previous_action[room] = action
        return action


rooms = {
    "Living Room": 18,
    "Bedroom": 22,
    "Kitchen": 20,
    "Bathroom": 24
}

desired_temperature = 22
agent = ModelBasedReflexAgent(desired_temperature)

for room, temperature in rooms.items():
    action = agent.act(room, temperature)
    print(f"{room}: Current temperature = {temperature}°C. {action}.")