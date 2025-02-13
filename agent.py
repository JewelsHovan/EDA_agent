import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from smolagents import CodeAgent, OpenAIServerModel
import config
from tools.eda_tools import get_dataframe_info, save_figure, create_report, ensure_directory
from tools.vision_tools import analyze_image
import io
from memory import Memory  # Import your custom memory manager

SYSTEM_PROMPT = """
You are an exploratory data analysis (EDA) assistant powered by smolagents.
Guidelines:
1. Generate concise, correct, and executable Python code.
2. Only use the available tools:
   - get_dataframe_info: Get basic statistics about the dataset
   - save_figure: Save generated plots to disk
   - create_report: Generate and save a final analysis report
   - ensure_directory: Create a directory for saving figures (ensures it exists)
   - analyze_image: Analyze an image and return a description of the image (use for analyzing the generated plots)

3. IMPORTANT: To access the DataFrame and libraries, use the following variables directly:
   - df: The pandas DataFrame to analyze
   - pd: pandas library
   - np: numpy library
   - plt: matplotlib.pyplot
   - sns: seaborn
   - io: io module

   To access any of the libraries, access from the state dictionary.
   state['pd']
   state['np']
   state['plt']
   state['sns']
   state['io']

   Do NOT try to use globals() or any other method to access these variables.
4. Begin your analysis by using get_dataframe_info(df) to understand the dataset structure.
5. All plotting functions return a BytesIO stream containing the plot image. Do NOT use plt.show() to display plots; instead, call save_figure to store the image on disk. Save all visualizations to the 'output/visualizations' directory.
6. Create expressive and effective visualizations using matplotlib and seaborn:
   - Always set clear, descriptive titles that explain the visualization's purpose
   - Label x and y axes with meaningful names and units where applicable
   - Use appropriate color schemes that enhance readability
   - Add legends when multiple data series are present
   - Include gridlines where they aid interpretation
   - Set appropriate figure sizes for clarity
   - Use proper font sizes for readability
   - Add annotations or text to highlight key points when relevant

7. Choose appropriate visualization types based on the data:
   - Use histograms with KDE for numeric distributions
   - Use pie charts or bar plots (with error bars if applicable) for categorical data
   - Use scatter plots with regression lines for relationships between numeric variables
   - Use box plots or violin plots for categorical vs numeric analysis
   - Use line plots with markers for time series or ordered data
   - Consider using faceted plots (sns.FacetGrid) for multi-variable analysis
   - Use heatmaps for correlation analysis

8. Example tool usage with proper visualization styling:
   ```python
   # Initialize the DataFrame                                                                                              
   df = state['df']
   plt = state['plt']
   sns = state['sns']
                     
   # Get DataFrame info
   info = get_dataframe_info(df=df)
   
   # Create and save a styled histogram
   plt.figure(figsize=(10, 6))
   sns.histplot(data=df, x="numeric_column", kde=True)
   plt.title("Distribution of Numeric Values", pad=20)
   plt.xlabel("Value Range")
   plt.ylabel("Frequency")
   plt.grid(True, alpha=0.3)
   
   # Save the styled plot
   buf = io.BytesIO()
   plt.savefig(buf, format='png', bbox_inches='tight')
   buf.seek(0)
   saved_path = save_figure(buf, "histogram.png")
   state['visualization_paths'].append(saved_path)
   plt.close()
   ```
9. Analyze the generated visualizations to identify key insights or patterns in the dataset.
10. Finally, use create_report to generate a markdown report summarizing your analysis and save it to 'output/report.md'. Include links to the saved visualization images within the report.
11. Explain your analysis succinctly and provide commentary alongside code if needed within the report.
12. Ensure that all generated files are placed in the 'output/' directory, with visualizations in 'output/visualizations/'.

NOTE: You can look at visualizations paths list using state['visualization_paths'] to look at the generated plots and their respective plots

IMPORTANT: After saving any visualization using save_figure, ALWAYS add the returned path to state['visualization_paths'] list to keep track of all generated visualizations.
"""

class EDAAgent:
    def __init__(self, dataframe: pd.DataFrame):
        self.df = dataframe
        
        # Set plot style
        plt.style.use(config.PLOT_STYLE)
        plt.rcParams['figure.figsize'] = config.FIGURE_SIZE
        plt.rcParams['figure.dpi'] = config.DPI
        
        # Initialize OpenAIServerModel model
        self.model = OpenAIServerModel(
            model_id=config.MODEL_NAME,
            api_key=config.OPENAI_API_KEY
        )
        
        # Create tools list (without execute_analysis)
        self.tools = [
            get_dataframe_info,
            save_figure,
            create_report,
            ensure_directory,
            analyze_image
        ]
        
        # Initialize persistent memory using our Memory class
        self.memory = Memory()
        
        # Initialize CodeAgent
        self.agent = CodeAgent(
            tools=self.tools,
            model=self.model,
            max_steps=config.MAX_STEPS,
            planning_interval=config.PLANNING_INTERVAL,
            additional_authorized_imports=[
                "pandas",
                "numpy",
                "matplotlib.pyplot",
                "seaborn",
                "io"
            ]
        )

    def run(self, query: str = None, reset: bool = False):
        """
        Run the EDA process based on a user query or default analysis.
        
        Args:
            query: Optional user query for specific analysis.
            reset: If False, the agent retains its previous memory and context.
        """
        if query is None:
            query = (
                "Please perform an initial exploratory data analysis on this dataset. "
                "Start with basic statistics and create relevant visualizations for numeric columns."
            )
        
        # Create execution context with DataFrame, libraries, and persistent memory
        execution_context = {
            "df": self.df.copy(),
            "visualization_paths": [],
            "pd": pd,
            "np": np,
            "plt": plt,
            "sns": sns,
            "io": io,
            "memory": self.memory.get_history()
        }
        
        if execution_context["df"] is None:
            raise ValueError("DataFrame not initialized in execution context")

        # Run the agent; by setting reset=False, the agent builds on previous memory
        result = self.agent.run(
            task=query,
            reset=reset,
            additional_args={
                "state": execution_context,
                "system_prompt": SYSTEM_PROMPT
            }
        )
        
        # Optionally, update our persistent memory with new logs from the agent's run
        # (Here we simply append all new log messages; you could also filter or summarize them.)
        for log in self.agent.logs:
            self.memory.add(str(log))
        
        return result

    def ask(self, query: str):
        """
        Ask the agent to perform a specific analysis.
        
        Args:
            query: The analysis request from the user.
        """
        return self.run(query, reset=False)
