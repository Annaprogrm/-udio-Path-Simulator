#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  7 10:00:31 2026

@author: user
"""

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

"""
PROJECT: Audio Propagation Simulator
TOPIC: Shortest Path Algorithms & Statistical Modelling of Audio
DESCRIPTION: This script simulates how sound waves travel in a discretized 2D space.
It uses Dijkstra's Algorithm to find the acoustic path and applies 
statistical models to calculate signal attenuation (dB loss).
"""
def generate_statistical_analysis(G, source_pos, grid_size):
    """
    SECTION 2B: Statistical Analysis of characteristics.
    Generates a dataset of sound intensity across the entire room.
    """
    data_grid = np.zeros((grid_size, grid_size))
    
    for x in range(grid_size):
        for y in range(grid_size):
            try:
                # Calculate path to every single point in the room
                p_len = nx.shortest_path_length(G, source=source_pos, target=(x, y), weight='weight')
                # Statistical model for dB intensity
                intensity = 100 - (20 * np.log10(p_len + 1))
                data_grid[y, x] = intensity # Map to grid
            except:
                data_grid[y, x] = 0 # If unreachable

    # Create the Heatmap for the report
    plt.figure(figsize=(10, 8))
    sns.heatmap(data_grid, annot=False, cmap="YlOrRd", cbar_kws={'label': 'Sound Intensity (dB)'})
    plt.title("Statistical Analysis 2B: Acoustic Intensity Heatmap")
    plt.xlabel("X-coordinate (meters)")
    plt.ylabel("Y-coordinate (meters)")
    plt.show()
    return data_grid



def simulate_audio():
    # --- 1. SIMULATION PARAMETERS ---
    # Define the room size (15x15 units/meters)
    grid_size = 15          
    source_pos = (2, 2)     # Speaker location coordinates
    target_pos = (12, 13)   # Microphone/Listener location coordinates
    initial_db = 100        # Sound Pressure Level (SPL) at the source in decibels
    
    # --- 2. ENVIRONMENT MODELING (GRAPH THEORY) ---
    # Create a 2D Grid Graph where each node represents a coordinate in space.
    # Connections (edges) represent the possibility of sound traveling between points.
    G = nx.grid_2d_graph(grid_size, grid_size)
    
    # Initialize all edges with a base weight of 1.0 (representing 1 meter distance)
    for (u, v) in G.edges():
        G.edges[u,v]['weight'] = 1.0

    # --- 3. STATISTICAL MODELLING OF OBSTACLES (ACOUSTIC BARRIERS) ---
    # In real-world acoustics, materials like concrete or wood attenuate sound.
    # We simulate a "Wall" by increasing the edge weights significantly.
    # This forces the Shortest Path algorithm to either find a detour or account for the energy loss.
    wall_x = 7
    wall_y_range = range(4, 12) # Wall spans from y=4 to y=11
    
    for y in wall_y_range:
        wall_node = (wall_x, y)
        if wall_node in G.nodes:
            # Increase weight to 15.0 to simulate high absorption/transmission loss
            # This represents a physical barrier where sound energy is heavily dissipated.
            for neighbor in G.neighbors(wall_node):
                G.edges[wall_node, neighbor]['weight'] = 15.0

    # --- 4. SHORTEST PATH ALGORITHM (DIJKSTRA) ---
    # Fermat's Principle states that sound follows the path that takes the least time.
    # Dijkstra's algorithm perfectly models this behavior in a discretized graph.
    try:
        # Calculate the path and the 'Acoustic Distance' (weighted path length)
        shortest_path = nx.shortest_path(G, source=source_pos, target=target_pos, weight='weight')
        path_length = nx.shortest_path_length(G, source=source_pos, target=target_pos, weight='weight')
    except nx.NetworkXNoPath:
        print("Error: No acoustic path found between source and receiver!")
        return

    # --- 5. STATISTICAL AUDIO MODELLING (ATTENUATION) ---
    # We apply the Inverse Square Law modeled in the logarithmic Decibel scale.
    # Formula: L_received = L_source - 20 * log10(Distance)
    # We also include a 'Medium Absorption Coefficient' for air humidity/temperature effects.
    air_absorption_coeff = 0.05 
    
    # Logarithmic attenuation (Geometric spreading loss)
    geometric_loss = 20 * np.log10(path_length + 1)
    
    # Statistical absorption loss (Medium interaction)
    absorption_loss = air_absorption_coeff * path_length
    
    # Final received signal strength
    received_db = initial_db - geometric_loss - absorption_loss

    # --- 6. DATA OUTPUT & LOGGING ---
    print(f"--- ACOUSTIC SIMULATION RESULTS ---")
    print(f"Source Coordinates: {source_pos}")
    print(f"Receiver Coordinates: {target_pos}")
    print(f"Computed Acoustic Path Length: {path_length:.2f} meters")
    print(f"Source Intensity: {initial_db} dB")
    print(f"Received Intensity: {received_db:.2f} dB")
    print(f"Total Transmission Loss: {initial_db - received_db:.2f} dB")

    # --- 7. VISUALIZATION (FOR PRESENTATION SLIDES) ---
    plt.figure(figsize=(12, 9))
    pos = {node: node for node in G.nodes()}
    
    # Draw the background grid nodes
    nx.draw_networkx_nodes(G, pos, node_size=25, node_color='lightgray', alpha=0.4)
    
    # Highlight the obstacle (The Wall)
    wall_nodes = [(wall_x, y) for y in wall_y_range]
    nx.draw_networkx_nodes(G, pos, nodelist=wall_nodes, node_color='black', node_size=60, label='Acoustic Barrier (Wall)')
    
    # Plot the calculated path taken by the sound wave
    path_edges = list(zip(shortest_path, shortest_path[1:]))
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=3, label='Sound Wave Propagation Path')
    
    # Mark Source and Receiver
    nx.draw_networkx_nodes(G, pos, nodelist=[source_pos], node_color='green', node_size=200, label='Audio Source')
    nx.draw_networkx_nodes(G, pos, nodelist=[target_pos], node_color='blue', node_size=200, label='Receiver')

    plt.title(f"Acoustic Pathfinding Simulation\nFinal Signal Intensity: {received_db:.2f} dB", fontsize=14)
    plt.xlabel("X-coordinate (meters)")
    plt.ylabel("Y-coordinate (meters)")
    plt.legend(loc='upper right', scatterpoints=1)
    plt.grid(True, linestyle=':', alpha=0.5)
    plt.show()

# Entry point of the script
if __name__ == "__main__":
    simulate_audio()