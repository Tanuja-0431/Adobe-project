import numpy as np
import matplotlib.pyplot as plt
import svgwrite
import cairosvg
import os

def read_csv(csv_path):
    """
    Reads a CSV file and returns a list of shapes.
    Each shape is a list of paths, and each path is a numpy array of points.
    """
    print(f"Trying to read CSV file from: {csv_path}")
    np_path_XYs = np.genfromtxt(csv_path, delimiter=',')
    print(f"Data read from {csv_path}:\n{np_path_XYs}")  # Add this line for logging
    
    path_XYs = []
    unique_shapes = np.unique(np_path_XYs[:, 0])
    
    for shape_id in unique_shapes:
        shape_points = np_path_XYs[np_path_XYs[:, 0] == shape_id][:, 1:]
        unique_paths = np.unique(shape_points[:, 0])
        
        paths = []
        for path_id in unique_paths:
            path_points = shape_points[shape_points[:, 0] == path_id][:, 1:]
            paths.append(path_points)
        path_XYs.append(paths)
    return path_XYs

def plot(paths_XYs):
    """
    Plots the shapes and displays them using matplotlib.
    """
    fig, ax = plt.subplots(tight_layout=True, figsize=(8, 8))
    colours = ['r', 'g', 'b', 'c', 'm', 'y', 'k']
    
    for i, paths in enumerate(paths_XYs):
        color = colours[i % len(colours)]
        for path in paths:
            ax.plot(path[:, 0], path[:, 1], c=color, linewidth=2)
    
    ax.set_aspect('equal')
    plt.show()

def polylines2svg(paths_XYs, svg_path):
    """
    Converts a list of shapes into an SVG file and saves it. Also converts the SVG to PNG.
    """
    # Determine the maximum width and height
    max_width, max_height = 0, 0
    for shape in paths_XYs:
        for path in shape:
            max_width = max(max_width, np.max(path[:, 0]))
            max_height = max(max_height, np.max(path[:, 1]))
    
    padding = 0.1
    width = int(max_width + padding * max_width)
    height = int(max_height + padding * max_height)

    # Create a new SVG drawing
    dwg = svgwrite.Drawing(svg_path, profile='tiny', shape_rendering='crispEdges')
    group = dwg.g()
    colours = ['red', 'green', 'blue', 'cyan', 'magenta', 'yellow', 'black']
    
    for i, shape in enumerate(paths_XYs):
        color = colours[i % len(colours)]
        for path in shape:
            path_str = 'M' + ' '.join(f'{x},{y}' for x, y in path) + 'Z'
            dwg.add(dwg.path(d=path_str, fill='none', stroke=color, stroke_width=2))
    
    dwg.add(group)
    dwg.save()

    # Convert SVG to PNG
    png_path = svg_path.replace('.svg', '.png')
    scale_factor = max(1, 1024 // min(height, width))
    cairosvg.svg2png(url=svg_path, write_to=png_path, parent_width=width, parent_height=height, 
                     output_width=scale_factor * width, output_height=scale_factor * height, 
                     background_color='white')
    print(f"SVG and PNG files saved: {svg_path}, {png_path}")

def process_shapes(base_dir, csv_filenames):
    """
    Processes each CSV file to read shapes, plot them, and save them as SVG and PNG files.
    """
    for csv_filename in csv_filenames:
        csv_path = os.path.join(base_dir, csv_filename)
        if os.path.exists(csv_path):
            shapes = read_csv(csv_path)
            plot(shapes)
            polylines2svg(shapes, csv_path.replace('.csv', '.svg'))
        else:
            print(f"CSV file not found: {csv_path}")

# Base directory containing the CSV files
base_dir = os.path.dirname(os.path.abspath(__file__))
print(f"Base directory: {base_dir}")

# List of CSV files to process
csv_filenames = [
    'isolated.csv',
    'frag0.csv',
    'frag1.csv',
    'occlusion1.csv',
    'occlusion2.csv'
]

# Process the CSV files
process_shapes(base_dir, csv_filenames)
