Below is an **updated plan** for the EDA Agent architecture, revised to use **multiple specialized agents** rather than a single agent. We will keep using the **smolagents** framework and tool-based design, but divide responsibilities among three agents:

1. **Planner** – inspects the DataFrame and decides which visualizations or analyses would be insightful.
2. **Executor** – implements the Planner’s instructions (plots, transforms, etc.).
3. **Reporter** – reviews all prior outputs (stats, plots, transformations) and composes a final report in Markdown.

---

## 1. Purpose

We still want an interactive environment to:
- **Load and inspect** a dataset.
- **Compute statistics** and generate summaries.
- **Generate visualizations** (histograms, scatter plots, correlation matrices, etc.).
- **Iterate** based on user prompts, refining or augmenting the analysis.

However, in this revised plan, we explicitly **split** the EDA workflow across three specialized agents (Planner, Executor, Reporter) to improve modularity and clarity.

---

## 2. Multi-Agent Architecture

### 2.1 Planner Agent

- **Role**: Receives an overview of the data (e.g., DataFrame info, column types, preliminary stats) and decides on a series of EDA tasks (e.g., “create a histogram of X,” “plot correlation heatmap,” “check for missing values”).
- **Implementation**: 
  - Could be a `CodeAgent` or standard “LLM Agent” that **does not** directly execute code but **generates instructions** or code blocks for the Executor to run.
  - Has access to: 
    - Basic summary of the DataFrame (columns, dtypes, size, missing values).
    - Output from any prior steps (or user queries).
  - **Memory**: Remembers which columns or stats were already explored to avoid duplication.  

### 2.2 Executor Agent

- **Role**: Implements the Planner’s instructions by calling appropriate EDA tools.
- **Implementation**: 
  - Likely a `CodeAgent` that can generate and run Python code for data manipulation, plotting, etc.
  - Has direct access to the environment with `pandas`, `matplotlib`/`seaborn`, etc.
  - Tools might include:
    1. **`load_data_tool`** – Load data from CSV, Excel, etc.  
    2. **`summary_stats_tool`** – Return numeric or textual stats.  
    3. **`plot_tool`** – Create plots (histograms, scatter plots, heatmaps).  
    4. **`feature_transform_tool`** (optional) – Clean or engineer features.  
  - **Memory**: 
    - Tracks references to the DataFrame object.
    - Maintains a list of generated plots (file paths or object references).  

### 2.3 Reporter Agent

- **Role**: Consumes the outputs (stats, images, transformations) from the Planner and Executor, then writes a cohesive EDA report in Markdown.
- **Implementation**: 
  - Could be a simpler `LLM Agent` or `CodeAgent` that produces text with Markdown references to any images.
  - Integrates results from all steps into a final narrative, e.g.:
    - Summaries of each variable
    - Observed distributions
    - Plots and discovered insights
    - Potential next steps or recommendations
  - **Memory**: 
    - Has access to a final summary of all prior steps (stats, plot paths) and the conversation context.

---

## 3. Tools & Inter-Agent Communication

### 3.1 Tooling Layer

As before, we maintain a library of **EDA tools**. However, now:
- **Planner** might call a tool like `get_df_info` or `get_summary_stats` to know the data shape before planning.
- **Executor** is the main user of plotting and transformation tools.
- **Reporter** does not necessarily call these tools (unless needed for final textual transformations). Instead, it references the results from the Executor’s calls.

### 3.2 Communication Flow

1. **User** → **Planner**  
   - The user starts by asking something like:  
     > “Load `data/customers.csv` and perform a quick analysis.”  
   - The Planner requests initial data info from the Executor (e.g., `load_data_tool` and `summary_stats_tool`).
2. **Planner** → **Executor**  
   - Once the Planner sees the DataFrame columns, it decides on a set of visualizations (e.g., “Plot histogram of Age,” “Plot correlation matrix,” etc.).
   - It passes these instructions to the Executor.
3. **Executor**  
   - Runs each requested tool (plots, transformations).
   - Stores references to the resulting figures or numeric outputs.
   - Returns a “completion” message or an object describing the results (plot file paths, numeric output, etc.) to the Planner.
4. **Planner** → **Reporter**  
   - After obtaining or reviewing the Executor outputs, the Planner can pass everything to the Reporter (or the user might manually instruct the Reporter to finalize the analysis).
5. **Reporter**  
   - Gathers the final set of outputs (stats, images, transformations).
   - Composes a Markdown-based summary or full EDA report referencing the images.

**Note**: In practice, this can be a chain of back-and-forth calls:
- The Planner might ask for new stats or new plots if initial results suggest deeper analysis.
- The user can also prompt the Planner at any time for further exploration.

---

## 4. Example Interaction

1. **User**:  
   > “Load `customers.csv`. Give me a quick overview and then create some visualizations for age, income distribution, and relationships among columns.”

2. **Planner**:  
   - Requests `load_data_tool` from the Executor.
   - Receives DataFrame info & summary stats.
   - Decides on a plan:
     - “Plot a histogram of Age”  
     - “Plot a histogram of Income”  
     - “Plot a correlation heatmap of numeric columns”  
   - Sends instructions to Executor.

3. **Executor**:  
   - Calls `plot_tool` with the DataFrame, columns = ‘Age’, etc.
   - Returns references to plot images (e.g., `hist_age.png`, `hist_income.png`, `corr_heatmap.png`).

4. **Planner**:  
   - Receives references from Executor.
   - Satisfied with the coverage or might add more tasks (like box plots for outliers).
   - Finally, it triggers the Reporter or the user requests the final summary.

5. **Reporter**:  
   - Takes all numeric stats (e.g., average age/income) plus the paths `hist_age.png`, `hist_income.png`, `corr_heatmap.png`.
   - Composes a Markdown report that references those images:
     ```
     ## EDA Report
     - **Summary Stats**: Mean age = 45, ...
     - **Age Distribution**:
       ![](hist_age.png)
     - **Income Distribution**:
       ![](hist_income.png)
     - **Correlation Heatmap**:
       ![](corr_heatmap.png)
     ```
   - Returns the final Markdown to the user.

---

## 5. Implementation Details

1. **smolagents Setup**  
   - Each agent can be a separate `CodeAgent` or `LLM Agent`.
   - For example:
     ```python
     planner = LlmAgent(model=..., tools=[get_df_info, get_summary_stats]) 
     executor = CodeAgent(model=..., tools=[load_data_tool, plot_tool, feature_transform_tool]) 
     reporter = LlmAgent(model=...)
     ```
2. **Tool Decorators**  
   - We can define the standard EDA tools as Python functions decorated with `@tool` so they can be called from any agent that has them in its `tools` list.
   - Tools should produce consistent, structured outputs (e.g., a dictionary with references to plot paths).
3. **Memory Sharing**  
   - Each agent might keep its own short-term memory. 
   - For broader context (e.g., sharing DataFrame references or plot paths), consider storing shared state in a persistent place accessible to all agents (e.g., an in-memory dictionary or a lightweight database if needed).
4. **Error Handling & Iteration**  
   - If a tool fails (file not found, plot error), the agent’s “thought process” (ReAct pattern) can decide to fix the code or request a new path.

---

## 6. Summary

By introducing **Planner**, **Executor**, and **Reporter** agents, we separate concerns:

- **Planner**: Chooses which EDA steps to perform next, based on data structure, columns, and user requests.  
- **Executor**: Runs actual code for stats, transformations, and plotting.  
- **Reporter**: Summarizes the entire process and outputs a final, user-friendly report in Markdown.
