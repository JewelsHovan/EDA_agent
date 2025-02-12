# A simple memory manager to keep track of agent insights and generated plots
class Memory:
    def __init__(self):
        self.logs = []

    def add(self, message: str):
        """Append a new memory message."""
        self.logs.append(message)

    def get_history(self):
        """Retrieve the entire history as a single string."""
        return "\n".join(self.logs)

    def clear(self):
        """Clear the memory."""
        self.logs.clear()
