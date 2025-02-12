#!/usr/bin/env python3
"""
test_fibonacci.py

A simple script to test smolagents' CodeAgent by asking it to compute the 20th Fibonacci number.
The agent writes and executes Python code to perform the calculation.
"""

from smolagents import CodeAgent, HfApiModel

def main():
    # Initialize the LLM model via Hugging Face's inference API.
    # You can change the model_id to any other supported model as needed.
    model = HfApiModel(model_id="mistralai/Mistral-7B-Instruct-v0.3")
    
    # Create a CodeAgent. Here, add_base_tools is set to True to include the default Python code executor.
    agent = CodeAgent(
        tools=[],
        model=model,
        add_base_tools=True
    )
    
    # Define a task for the agent: computing the 20th Fibonacci number.
    task = "Compute the 20th Fibonacci number."
    print("Running task:", task)
    
    # Run the agent. The multi-step CodeAgent will generate and execute Python code to solve the task.
    result = agent.run(task)
    
    print("\nAgent Result:\n", result)

if __name__ == "__main__":
    main() 