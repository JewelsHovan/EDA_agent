import argparse
from agent import EDAAgent
from tools.file_io import load_csv, load_parquet

def main():
    parser = argparse.ArgumentParser(description="Autonomous EDA Agent")
    parser.add_argument("--path", type=str, help="Path to the dataset (CSV/Parquet)")
    parser.add_argument("--interactive", action="store_true", help="Run in interactive mode")
    args = parser.parse_args()

    if args.path.endswith(".csv"):
        df = load_csv(args.path)
    elif args.path.endswith(".parquet"):
        df = load_parquet(args.path)
    else:
        raise ValueError("Unsupported file format. Please provide .csv or .parquet.")

    # Create the EDA agent
    agent = EDAAgent(dataframe=df)
    
    if args.interactive:
        print("\nEntering interactive mode. Type 'exit' to quit.")
        print("You can ask questions about the data or request specific analyses.")
        
        while True:
            query = input("\nWhat would you like to know about the data? > ")
            if query.lower() == 'exit':
                break
                
            try:
                result = agent.ask(query)
                print("\nAgent Response:")
                print(result)
            except Exception as e:
                print(f"\nError: {str(e)}")
    else:
        # Run default analysis

        query = """
        Please perform an initial exploratory data analysis on this dataset. It is a dataset of car thefts in India. Think of some interesting questions after initila analysis and create some interesting plots.
        """

        result = agent.run(query)
        print(result)

if __name__ == "__main__":
    main()
