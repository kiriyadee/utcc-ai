import matplotlib.pyplot as plt
import numpy as np


def calculate_and_plot_vector(vector1, vector2):
    # Convert input vectors to numpy arrays
    v1 = np.array(vector1)
    v2 = np.array(vector2)
    
    # Calculate vector operations
    sum_vector = v1 + v2
    dot_product = np.dot(v1, v2)
    cross_product = np.cross(v1, v2)
    
    # Create plot
    plt.figure(figsize=(10, 10))
    
    # Plot vectors
    plt.quiver(0, 0, v1[0], v1[1], angles='xy', scale_units='xy', scale=1, color='r', label='Vector 1')
    plt.quiver(0, 0, v2[0], v2[1], angles='xy', scale_units='xy', scale=1, color='b', label='Vector 2')
    plt.quiver(0, 0, sum_vector[0], sum_vector[1], angles='xy', scale_units='xy', scale=1, color='g', label='Sum Vector')
    
    # Set plot properties
    plt.xlim(-10, 10)
    plt.ylim(-10, 10)
    plt.grid(True)
    plt.axhline(y=0, color='k')
    plt.axvline(x=0, color='k')
    plt.legend()
    
    # Add text with calculations
    plt.text(-9, 8, f'Dot product: {dot_product}')
    plt.text(-9, 7, f'Cross product: {cross_product}')
    
    plt.title('Vector Calculations and Visualization')
    plt.savefig('vector_plot.png')
    plt.close()

# Example usage
vector1 = [3, 4]
vector2 = [1, 2]
calculate_and_plot_vector(vector1, vector2)