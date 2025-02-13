import pandas as pd
from tools.plotting import plot_histogram, plot_pie, plot_scatter, plot_line, plot_boxplot, plot_bar
from smolagents import tool
import os
import io

@tool
def get_dataframe_info(df: pd.DataFrame) -> str:
    """
    Get basic information about the DataFrame.

    Args:
        df: The pandas DataFrame to analyze
    """
    info_str = []
    info_str.append(f"DataFrame Shape: {df.shape}")
    info_str.append("\nColumns:\n" + ", ".join(df.columns))
    info_str.append("\nDataTypes:\n" + df.dtypes.to_string())
    info_str.append("\nSummary Statistics:\n" + df.describe().to_string())
    info_str.append("\nMissing Values:\n" + df.isnull().sum().to_string())
    return "\n".join(info_str)

@tool
def ensure_directory(directory_path: str) -> str:
    """
    Creates a directory if it doesn't exist, including any necessary parent directories.
    
    Args:
        directory_path: The path of the directory to create (e.g., "output/visualizations")
    
    Returns:
        Confirmation message with the created path
    """
    os.makedirs(directory_path, exist_ok=True)
    return f"Directory created successfully at: {directory_path}"

@tool
def save_figure(fig: io.BytesIO, filename: str) -> str:
    """
    Saves a Matplotlib figure represented in a BytesIO stream to a file.

    Args:
        fig: A BytesIO stream containing the Matplotlib figure to be saved.
                         This object should be created by Matplotlib's `savefig` method.
        filename: The name of the file to which the figure will be saved.

    Returns:
        str: The file path where the figure was saved.
    """
    try:
        # Ensure the 'output/visualizations' directory exists
        ensure_directory("output/visualizations")
        
        # Save the figure
        with open(filename, "wb") as f:
            f.write(fig.getvalue())
        
        print(f"Figure saved to {filename}")

        return filename
    except Exception as e:
        print(f"Error saving figure: {e}")
        return None

@tool
def create_report(report_text: str, image_links: list, output_path: str) -> str:
    """
    Create a final markdown report including analysis commentary and image links, and save it to a file.

    Args:
        report_text: A string containing the analysis and insights.
        image_links: A list of strings representing the paths or URLs of the saved images.
        output_path: The full path to save the markdown report (e.g., "output/report.md").

    Returns:
        A confirmation message indicating where the report was saved.
    """
    # remove the output/ base 
    image_links = [link.replace("output/", "") for link in image_links]
    images_md = "\n".join(f"![Visualization]({link})" for link in image_links)
    report = f"# Exploratory Data Analysis Report\n\n{report_text}\n\n## Visualizations\n{images_md}\n"
    
    with open(output_path, "w") as f:
        f.write(report)
    return f"Report saved successfully to {output_path}"