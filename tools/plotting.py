import matplotlib.pyplot as plt
import seaborn as sns
import io

# Set a default theme for consistent styling and improved aesthetics
sns.set_theme(style="whitegrid", context="talk", palette="deep")

def _save_plot():
    """
    Helper function to save the current matplotlib figure to a BytesIO buffer.
    
    Returns:
        BytesIO: Buffer containing the plot image data.
    """
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    return buf

def plot_histogram(df, column, bins=30, title="Histogram", xlabel=None, ylabel="Frequency"):
    """
    Plots a histogram for the specified DataFrame column with improved styling.
    
    Args:
        df (pandas.DataFrame): DataFrame containing the data.
        column (str): Column name to plot the histogram.
        bins (int): Number of bins for the histogram.
        title (str): Title of the plot.
        xlabel (str): Label for the x-axis. Defaults to the column name.
        ylabel (str): Label for the y-axis.
        
    Returns:
        BytesIO: Buffer containing the plot image.
    """
    plt.figure(figsize=(12, 8))
    sns.histplot(data=df, x=column, bins=bins, kde=True)
    if title:
        plt.title(title)
    if xlabel is None:
        xlabel = column
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    return _save_plot()

def plot_scatter(df, x, y, title="Scatter Plot", xlabel=None, ylabel=None, hue=None):
    """
    Creates a scatter plot from the DataFrame with improved aesthetics.
    
    Args:
        df (pandas.DataFrame): DataFrame containing the data.
        x (str): Column name for the x-axis.
        y (str): Column name for the y-axis.
        title (str): Title of the plot.
        xlabel (str): Label for the x-axis. Defaults to the x column name.
        ylabel (str): Label for the y-axis. Defaults to the y column name.
        hue (str, optional): Column name to color the data points based on.
        
    Returns:
        BytesIO: Buffer containing the plot image.
    """
    plt.figure(figsize=(12, 8))
    if hue:
        sns.scatterplot(data=df, x=x, y=y, hue=hue, s=100)
    else:
        sns.scatterplot(data=df, x=x, y=y, s=100)
    if title:
        plt.title(title)
    if xlabel is None:
        xlabel = x
    plt.xlabel(xlabel)
    if ylabel is None:
        ylabel = y
    plt.ylabel(ylabel)
    return _save_plot()

def plot_line(df, x, y, title="Line Plot", xlabel=None, ylabel=None, hue=None):
    """
    Creates a line plot from the DataFrame with improved styling.
    
    Args:
        df (pandas.DataFrame): DataFrame containing the data.
        x (str): Column name for the x-axis.
        y (str): Column name for the y-axis.
        title (str): Title of the plot.
        xlabel (str): Label for the x-axis. Defaults to the x column name.
        ylabel (str): Label for the y-axis. Defaults to the y column name.
        hue (str, optional): Column name to group the lines by color.
        
    Returns:
        BytesIO: Buffer containing the plot image.
    """
    plt.figure(figsize=(12, 8))
    if hue:
        sns.lineplot(data=df, x=x, y=y, hue=hue, marker='o')
    else:
        sns.lineplot(data=df, x=x, y=y, marker='o')
    if title:
        plt.title(title)
    if xlabel is None:
        xlabel = x
    plt.xlabel(xlabel)
    if ylabel is None:
        ylabel = y
    plt.ylabel(ylabel)
    return _save_plot()

def plot_boxplot(df, x, y, title="Box Plot", xlabel=None, ylabel=None):
    """
    Creates a box plot from the DataFrame with improved aesthetics.
    
    Args:
        df (pandas.DataFrame): DataFrame containing the data.
        x (str): Column name representing categorical data.
        y (str): Column name for numerical data.
        title (str): Title of the plot.
        xlabel (str): Label for the x-axis. Defaults to the x column name.
        ylabel (str): Label for the y-axis. Defaults to the y column name.
        
    Returns:
        BytesIO: Buffer containing the plot image.
    """
    plt.figure(figsize=(12, 8))
    sns.boxplot(data=df, x=x, y=y)
    if title:
        plt.title(title)
    if xlabel is None:
        xlabel = x
    plt.xlabel(xlabel)
    if ylabel is None:
        ylabel = y
    plt.ylabel(ylabel)
    return _save_plot()

def plot_bar(df, x, y, title="Bar Plot", xlabel=None, ylabel=None, hue=None):
    """
    Creates a bar plot from the DataFrame with enhanced styling.
    
    Args:
        df (pandas.DataFrame): DataFrame containing the data.
        x (str): Column name for categories.
        y (str): Column name for values.
        title (str): Title of the plot.
        xlabel (str): Label for the x-axis. Defaults to the x column name.
        ylabel (str): Label for the y-axis. Defaults to the y column name.
        hue (str, optional): Column name to separate bars by color.
        
    Returns:
        BytesIO: Buffer containing the plot image.
    """
    plt.figure(figsize=(12, 8))
    if hue:
        sns.barplot(data=df, x=x, y=y, hue=hue)
    else:
        sns.barplot(data=df, x=x, y=y)
    if title:
        plt.title(title)
    if xlabel is None:
        xlabel = x
    plt.xlabel(xlabel)
    if ylabel is None:
        ylabel = y
    plt.ylabel(ylabel)
    return _save_plot()

def plot_pie(df, column, title="Pie Chart"):
    """
    Creates a pie chart depicting the distribution of values in the specified column.
    
    Args:
        df (pandas.DataFrame): DataFrame containing the data.
        column (str): Column name for which to plot the pie chart.
        title (str): Title of the plot.
        
    Returns:
        BytesIO: Buffer containing the plot image.
    """
    plt.figure(figsize=(12, 8))
    counts = df[column].value_counts()
    counts.plot.pie(autopct='%1.1f%%', startangle=90, counterclock=False)
    plt.title(title)
    plt.ylabel('')  # Remove the ylabel for a cleaner look
    return _save_plot()

