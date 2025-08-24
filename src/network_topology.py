import networkx as nx
import json
from typing import Dict, List, Any
from config_parser import ConfigParser

class NetworkTopology:
    def __init__(self):
        self.graph = nx.Graph()
        self.devices = {}
        self.links = {}
        self.parser = ConfigParser()
    
    def build_topology_from_configs(self, config_directory: str) -> None:
        """Build network topology from configuration files"""
        import os
        
        # Parse all config files
        for filename in os.listdir(config_directory):
            if filename.endswith('.txt'):
                file_path = os.path.join(config_directory, filename)
                device_config = self.parser.parse_config_file(file_path)
                
                if device_config:
                    device_id = device_config['device_name']
                    self.devices[device_id] = device_config
                    self.graph.add_node(device_id, **device_config)
        
        # Build connections based on IP networks
        self._build_connections()
    
    def _build_connections(self) -> None:
        """Enhanced connection building including switches"""
        subnet_devices = {}
        
        # Group devices by subnet
        for device_id, device_config in self.devices.items():
            for interface in device_config.get('interfaces', []):
                ip_address = interface.get('ip_address')
                subnet_mask = interface.get('subnet_mask')
                
                if ip_address and subnet_mask:
                    subnet = self._calculate_subnet(ip_address, subnet_mask)
                    
                    if subnet not in subnet_devices:
                        subnet_devices[subnet] = []
                    
                    subnet_devices[subnet].append({
                        'device_id': device_id,
                        'interface': interface['name'],
                        'ip_address': ip_address,
                        'bandwidth': interface.get('bandwidth', 100)
                    })
        
        # Create subnet-based links
        for subnet, devices_in_subnet in subnet_devices.items():
            if len(devices_in_subnet) > 1:
                for i, device1 in enumerate(devices_in_subnet):
                    for device2 in devices_in_subnet[i+1:]:
                        self._add_link(device1, device2, subnet)
        
        # Connect switches to their logical segments
        self._connect_switches_to_segments()
    
    def _connect_switches_to_segments(self):
        """Connect switches to devices in their network segments"""
        
        switches = [(did, dconfig) for did, dconfig in self.devices.items() 
                    if dconfig.get('device_type') == 'switch']
        
        for switch_id, switch_config in switches:
            # Get VLANs configured on this switch
            switch_vlans = [vlan.get('id') for vlan in switch_config.get('vlans', [])]
            
            # Connect switch to routers and endpoints in same segments
            for other_id, other_config in self.devices.items():
                if other_id != switch_id and switch_id not in [link['device1']['device_id'] 
                                                              for link in self.links.values()]:
                    
                    # Strategy 1: Connect based on VLAN membership
                    if self._shares_vlan_segment(other_config, switch_vlans):
                        self._add_switch_link(switch_id, other_id)
                        
                    # Strategy 2: Connect each switch to one router (hierarchical)
                    elif other_config.get('device_type') == 'router':
                        # Connect S1->R1, S2->R2, S3->R3 pattern
                        switch_num = switch_id[-1]  # Extract number from S1, S2, S3
                        router_num = other_id[-1]   # Extract number from R1, R2, R3
                        
                        if switch_num == router_num:
                            self._add_switch_link(switch_id, other_id)
    
    def _shares_vlan_segment(self, device_config, switch_vlans):
        """Check if device shares VLAN with switch"""
        device_vlans = []
        for interface in device_config.get('interfaces', []):
            if interface.get('vlan'):
                device_vlans.append(interface['vlan'])
        
        return bool(set(device_vlans) & set(switch_vlans))

    def _add_switch_link(self, switch_id, device_id):
        """Add link between switch and device"""
        link_id = f"{switch_id}-{device_id}"
        
        if link_id not in self.links and f"{device_id}-{switch_id}" not in self.links:
            self.links[link_id] = {
                'device1': {'device_id': switch_id, 'interface': 'mgmt'},
                'device2': {'device_id': device_id, 'interface': 'mgmt'},
                'bandwidth_mbps': 1000,  # 1 Gbps management link
                'current_utilization': 0
            }
            print(f"✅ Added switch link: {switch_id} <-> {device_id}")
    
    def _calculate_subnet(self, ip_address: str, subnet_mask: str) -> str:
        """Calculate subnet from IP address and mask"""
        ip_parts = [int(x) for x in ip_address.split('.')]
        mask_parts = [int(x) for x in subnet_mask.split('.')]
        
        subnet_parts = [ip_parts[i] & mask_parts[i] for i in range(4)]
        return '.'.join(map(str, subnet_parts))
    
    def _add_link(self, device1: Dict, device2: Dict, subnet: str) -> None:
        """Add link between two devices"""
        link_id = f"{device1['device_id']}-{device2['device_id']}"
        
        # Use minimum bandwidth as link capacity
        link_bandwidth = min(device1['bandwidth'], device2['bandwidth'])
        
        self.graph.add_edge(
            device1['device_id'], 
            device2['device_id'],
            link_id=link_id,
            subnet=subnet,
            bandwidth_mbps=link_bandwidth,
            utilization=0,
            status='up'
        )
        
        self.links[link_id] = {
            'device1': device1,
            'device2': device2,
            'subnet': subnet,
            'bandwidth_mbps': link_bandwidth,
            'current_utilization': 0
        }
    
    def get_topology_summary(self) -> Dict[str, Any]:
        """Get summary of network topology"""
        return {
            'total_devices': len(self.devices),
            'routers': len([d for d in self.devices.values() if d['device_type'] == 'router']),
            'switches': len([d for d in self.devices.values() if d['device_type'] == 'switch']),
            'endpoints': len([d for d in self.devices.values() if d['device_type'] == 'endpoint']),
            'total_links': len(self.links),
            'subnets': len(set(link['subnet'] for link in self.links.values() if 'subnet' in link))
        }
    
    def export_to_json(self, filename: str) -> None:
        """Export topology to JSON file"""
        topology_data = {
            'devices': self.devices,
            'links': self.links,
            'summary': self.get_topology_summary()
        }
        
        with open(filename, 'w') as f:
            json.dump(topology_data, f, indent=2)
        
        print(f"Topology exported to {filename}")

# Test the topology builder
if __name__ == "__main__":
    topology = NetworkTopology()
    topology.build_topology_from_configs("config_files")
    print("Topology Summary:", topology.get_topology_summary())
    topology.export_to_json("output/network_topology.json")