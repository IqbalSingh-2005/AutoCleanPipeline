import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend for web
import io
import base64

def visual(df: pd.DataFrame):
    """Legacy function for backward compatibility"""
    x = df[df.columns[0]]
    y = df[df.columns[1]]

    fig, axes = plt.subplots(3, 1, figsize=(8, 12))

    # Line plot
    axes[0].plot(x, y)
    axes[0].set_title("Line Plot")

    # Scatter plot
    axes[1].scatter(x, y)
    axes[1].set_title("Scatter Plot")

    # Bar plot
    axes[2].bar(x, y)
    axes[2].set_title("Bar Plot")

    plt.tight_layout()
    plt.show()


def generate_chart(df: pd.DataFrame, x_col: str, y_col: str, chart_type: str = 'line'):
    """
    Generate a chart and return as base64 encoded image

    Args:
        df: DataFrame containing the data
        x_col: Column name for X axis
        y_col: Column name for Y axis
        chart_type: Type of chart (line, scatter, bar, histogram, box, area)

    Returns:
        Base64 encoded image string
    """
    plt.figure(figsize=(10, 6))

    try:
        x = df[x_col]
        y = df[y_col]

        if chart_type == 'line':
            plt.plot(x, y, linewidth=2, marker='o', markersize=4)
            plt.title(f'Line Chart: {y_col} vs {x_col}')

        elif chart_type == 'scatter':
            plt.scatter(x, y, alpha=0.6, s=50)
            plt.title(f'Scatter Plot: {y_col} vs {x_col}')

        elif chart_type == 'bar':
            plt.bar(x, y, color='steelblue', alpha=0.7)
            plt.title(f'Bar Chart: {y_col} vs {x_col}')
            plt.xticks(rotation=45, ha='right')

        elif chart_type == 'histogram':
            plt.hist(y, bins=20, color='coral', alpha=0.7, edgecolor='black')
            plt.title(f'Histogram: {y_col}')
            plt.xlabel(y_col)
            plt.ylabel('Frequency')

        elif chart_type == 'box':
            plt.boxplot([y], labels=[y_col])
            plt.title(f'Box Plot: {y_col}')
            plt.ylabel('Values')

        elif chart_type == 'area':
            plt.fill_between(x, y, alpha=0.5)
            plt.plot(x, y, linewidth=2)
            plt.title(f'Area Chart: {y_col} vs {x_col}')

        else:
            plt.plot(x, y)
            plt.title(f'Chart: {y_col} vs {x_col}')

        if chart_type not in ['histogram', 'box']:
            plt.xlabel(x_col)
            plt.ylabel(y_col)

        plt.grid(True, alpha=0.3)
        plt.tight_layout()

        # Convert to base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode()
        plt.close()

        return image_base64

    except Exception as e:
        plt.close()
        raise Exception(f"Error generating chart: {str(e)}")


def get_numeric_columns(df: pd.DataFrame):
    """Get list of numeric columns from dataframe"""
    return df.select_dtypes(include=['int64', 'float64']).columns.tolist()


def get_all_columns(df: pd.DataFrame):
    """Get list of all columns from dataframe"""
    return df.columns.tolist()