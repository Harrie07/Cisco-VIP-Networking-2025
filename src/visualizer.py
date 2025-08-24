import json
import matplotlib.pyplot as plt
import networkx as nx
import os

class NetworkVisualizer:
    def __init__(self):
        self.devices = {}
        self.links = {}

    def _build_connections(self) -> None:
        """Enhanced connection building for switches"""
        
        # Existing subnet-based connections (for routers/endpoints)
        for device_id, device_config in self.devices.items():
            if device_config.get('device_type') == 'switch':
                # Connect switches to devices in same physical segment
                self._connect_switch_to_local_devices(device_id, device_config)

    def _connect_switch_to_local_devices(self, switch_id, switch_config):
        """Connect switch to devices in same network segment"""
        
        # Find devices that should connect to this switch
        # Based on VLAN membership or physical proximity
        vlans_on_switch = [vlan.get('id') for vlan in switch_config.get('vlans', [])]
        
        for other_device_id, other_device_config in self.devices.items():
            if other_device_id != switch_id:
                # Connect if devices share VLANs or are in same segment
                if self._should_connect_to_switch(other_device_config, vlans_on_switch):
                    self._add_switch_link(switch_id, other_device_id)

    def _should_connect_to_switch(self, device_config, vlans_on_switch):
        """Determine if device should connect to switch"""
        # Check VLAN membership
        device_vlans = []
        for interface in device_config.get('interfaces', []):
            if interface.get('vlan'):
                device_vlans.append(interface['vlan'])
        
        return bool(set(device_vlans) & set(vlans_on_switch))

    def _add_switch_link(self, switch_id, device_id):
        """Add a link between switch and device"""
        link_id = f"{switch_id}-{device_id}"
        self.links[link_id] = {
            'device1': {'device_id': switch_id},
            'device2': {'device_id': device_id}
        }

def create_topology_image():
    # Load your topology data
    with open('output/network_topology.json', 'r') as f:
        data = json.load(f)
    
    # Create network graph
    G = nx.Graph()
    node_colors = []
    color_map = {'router': 'red', 'switch': 'blue', 'endpoint': 'green'}
    
    # Add nodes
    for device_id, device in data['devices'].items():
        G.add_node(device_id)
        device_type = device.get('device_type', 'endpoint')
        node_colors.append(color_map.get(device_type, 'gray'))
    
    # Add edges  
    for link_id, link in data['links'].items():
        src = link['device1']['device_id']
        dst = link['device2']['device_id']
        G.add_edge(src, dst)
    
    # Create and save visualization
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G, seed=42, k=3)
    nx.draw(G, pos, with_labels=True, node_color=node_colors, 
            node_size=1000, font_size=8, font_weight='bold')
    
    # Add legend
    import matplotlib.patches as mpatches
    router_patch = mpatches.Patch(color='red', label='Routers')
    switch_patch = mpatches.Patch(color='blue', label='Switches')
    endpoint_patch = mpatches.Patch(color='green', label='Endpoints')
    plt.legend(handles=[router_patch, switch_patch, endpoint_patch])
    
    plt.title("Network Topology - 12 Devices Generated Automatically", fontsize=14)
    
    # Save image
    os.makedirs('output/diagrams', exist_ok=True)
    plt.savefig('output/diagrams/network_topology.png', dpi=300, bbox_inches='tight')
    print("✅ Network topology image saved to: output/diagrams/network_topology.png")
    
    # Try to open the image
    try:
        plt.show()  # This will open in default image viewer
    except:
        print("📌 To view image: Open 'output/diagrams/network_topology.png' in VS Code or image viewer")

if __name__ == "__main__":
    create_topology_image()