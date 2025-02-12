#!/usr/bin/env python3
"""
test_web_agent.py

A simple script to test smolagents' CodeAgent with the DuckDuckGoSearchTool.
This agent performs a web search for a given query using a Hugging Face API model.
"""

from smolagents import CodeAgent, HfApiModel, DuckDuckGoSearchTool

def main():
    # Initialize the LLM model via Hugging Face's inference API.
    # Replace the model_id with your preferred model if needed.
    model = HfApiModel(model_id="mistralai/Mistral-7B-Instruct-v0.3")
    
    # Initialize the web search tool.
    web_search_tool = DuckDuckGoSearchTool()
    
    # Create a CodeAgent that has access to the web search tool.
    agent = CodeAgent(
        tools=[web_search_tool],
        model=model
    )
    
    # Define a query to test the web agent tool.
    query = "What is the capital city of Japan?"
    print("Running query:", query)
    
    # The agent's run method will execute multi-step actions if necessary.
    result = agent.run(query)
    
    print("\nAgent Result:\n", result)

if __name__ == "__main__":
    main() 