import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import os

def load_materials():
    """
    PRACTICAL FEATURE: Loads material data from an external file.
    Demonstrates file handling and data preprocessing.
    """
    materials = {}
    file_path = os.path.join("data", "materials.txt")
    
    try:
        with open(file_path, "r", encoding="latin-1") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) == 3:
                    m_id, name, weight = parts
                    materials[m_id] = (name, float(weight))
        return materials
    except FileNotFoundError:
        print("Warning: data/materials.txt not found. Using internal defaults.")
        return {"1": ("Air", 1.0), "2": ("Concrete", 20.0)}

def run_interactive_simulation():
    print("--- 🔊 PROFESSIONAL AUDIO PATH SIMULATOR ---")
    
    # Load data from folder
    materials_db = load_materials()
    
    # 1. SETUP ENVIRONMENT
    grid_size = 15
    G = nx.grid_2d_graph(grid_size, grid_size)
    for (u, v) in G.edges():
        G.edges[u,v]['weight'] = 1.0

    # 2. USER INPUT WITH VALIDATION
    try:
        print(f"\n[Step 1] Enter Coordinates (0-{grid_size-1}):")
        src_x = int(input("  Source X: "))
        src_y = int(input("  Source Y: "))
        trg_x = int(input("  Target X: "))
        trg_y = int(input("  Target Y: "))
        
        source, target = (src_x, src_y), (trg_x, trg_y)
        
        # Check if coordinates are within bounds
        if not (0 <= src_x < grid_size and 0 <= trg_x < grid_size):
            raise ValueError("Coordinates out of range!")

        # 3. MATERIAL SELECTION
        print("\n[Step 2] Select Barrier Material from Database:")
        for m_id, (name, w) in materials_db.items():
            print(f"  {m_id}: {name} (Resistance: {w})")
            
        choice = input("Your choice (ID): ")
        mat_name, mat_weight = materials_db.get(choice, ("Air", 1.0))

        # 4. MODELLING THE BARRIER
        wall_x = grid_size // 2
        for y in range(4, 12):
            if (wall_x, y) in G.nodes:
                for n in G.neighbors((wall_x, y)):
                    G.edges[(wall_x, y), n]['weight'] = mat_weight

        # 5. ALGORITHM & STATISTICS
        path = nx.shortest_path(G, source=source, target=target, weight='weight')
        length = nx.shortest_path_length(G, source=source, target=target, weight='weight')
        
        initial_db = 100
        # Scientific formula for attenuation
        received_db = initial_db - (20 * np.log10(length + 1))

        print(f"\n--- SIMULATION SUCCESS ---")
        print(f"Path found via {mat_name} barrier.")
        print(f"Signal at Receiver: {received_db:.2f} dB")

        # 6. VISUALIZATION
        plt.figure(figsize=(10, 6))
        pos = {node: node for node in G.nodes()}
        nx.draw(G, pos, node_size=5, node_color='lightgray', alpha=0.3)
        
        # Draw the wall based on material
        wall_nodes = [(wall_x, y) for y in range(4, 12)]
        nx.draw_networkx_nodes(G, pos, nodelist=wall_nodes, node_color='black', label=f'Barrier: {mat_name}')
        
        # Draw path
        path_edges = list(zip(path, path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2)
        
        plt.title(f"Acoustic Simulation: {mat_name} Wall\nIntensity: {received_db:.2f} dB")
        plt.legend()
        plt.show()

    except Exception as e:
        print(f"\n❌ Simulation Error: {e}")

if __name__ == "__main__":
    run_interactive_simulation()