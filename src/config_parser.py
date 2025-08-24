import re
import json
from typing import Dict, List, Any

class ConfigParser:
    def __init__(self):
        self.supported_formats = ['cisco', 'generic']
        
    def parse_config_file(self, file_path: str) -> Dict[str, Any]:
        """Parse network device configuration file"""
        try:
            with open(file_path, 'r') as file:
                content = file.read()
                
            device_config = {
                'device_name': self._extract_hostname(content),
                'device_type': self._detect_device_type(content),
                'interfaces': self._extract_interfaces(content),
                'vlans': self._extract_vlans(content),
                'routing_protocols': self._extract_routing_protocols(content),
                'ip_addresses': self._extract_ip_addresses(content)
            }
            
            return device_config
            
        except Exception as e:
            print(f"Error parsing config file {file_path}: {str(e)}")
            return {}
    
    def _extract_hostname(self, content: str) -> str:
        """Extract device hostname from config"""
        hostname_match = re.search(r'hostname\s+(\S+)', content)
        return hostname_match.group(1) if hostname_match else "Unknown"
    
    def _detect_device_type(self, content: str) -> str:
        """Detect if device is router, switch, or endpoint"""
        if 'router ospf' in content.lower() or 'router bgp' in content.lower():
            return 'router'
        elif 'spanning-tree' in content.lower() or 'switchport' in content.lower():
            return 'switch'
        else:
            return 'endpoint'
    
    def _extract_interfaces(self, content: str) -> List[Dict]:
        """Extract interface configurations - IMPROVED"""
        interfaces = []
        
        # Better regex to match interface blocks
        interface_pattern = r'interface\s+((?:GigabitEthernet|FastEthernet|Serial|Loopback|Ethernet)\d+(?:\/\d+)*(?:\/\d+)*)\s*(.*?)(?=interface\s+\w+|\Z)'
        interface_blocks = re.findall(interface_pattern, content, re.DOTALL | re.IGNORECASE)
        
        seen_interfaces = set()  # Track processed interfaces to avoid duplicates
        
        for interface_name, interface_config in interface_blocks:
            # Skip if we've already processed this interface
            if interface_name in seen_interfaces:
                continue
            
            seen_interfaces.add(interface_name)
            
            interface_info = {
                'name': interface_name,
                'ip_address': self._extract_ip_from_interface(interface_config),
                'subnet_mask': self._extract_subnet_from_interface(interface_config),
                'vlan': self._extract_vlan_from_interface(interface_config),
                'mtu': self._extract_mtu_from_interface(interface_config),
                'bandwidth': self._extract_bandwidth_from_interface(interface_config),
                'status': self._extract_interface_status(interface_config)
            }
            
            # Only add interfaces with valid names
            if self._is_valid_interface_name(interface_name):
                interfaces.append(interface_info)
        
        return interfaces

    def _is_valid_interface_name(self, interface_name: str) -> bool:
        """Check if interface name is valid"""
        valid_patterns = [
            r'GigabitEthernet\d+\/\d+(?:\/\d+)?',
            r'FastEthernet\d+\/\d+(?:\/\d+)?',
            r'Serial\d+\/\d+\/\d+',
            r'Loopback\d+',
            r'Ethernet\d+(?:\/\d+)*'
        ]
        
        for pattern in valid_patterns:
            if re.match(pattern, interface_name, re.IGNORECASE):
                return True
        
        return False
    
    def _extract_interface_status(self, interface_config: str) -> str:
        """Extract interface status"""
        if 'shutdown' in interface_config.lower():
            return 'down'
        elif 'no shutdown' in interface_config.lower():
            return 'up'
        else:
            return 'unknown'
    
    def _extract_ip_from_interface(self, interface_config: str) -> str:
        """Extract IP address from interface config"""
        ip_match = re.search(r'ip address\s+(\d+\.\d+\.\d+\.\d+)', interface_config)
        return ip_match.group(1) if ip_match else None
    
    def _extract_subnet_from_interface(self, interface_config: str) -> str:
        """Extract subnet mask from interface config"""
        subnet_match = re.search(r'ip address\s+\d+\.\d+\.\d+\.\d+\s+(\d+\.\d+\.\d+\.\d+)', interface_config)
        return subnet_match.group(1) if subnet_match else None
    
    def _extract_vlan_from_interface(self, interface_config: str) -> int:
        """Extract VLAN from interface config"""
        vlan_match = re.search(r'switchport access vlan\s+(\d+)', interface_config)
        return int(vlan_match.group(1)) if vlan_match else None
    
    def _extract_mtu_from_interface(self, interface_config: str) -> int:
        """Extract MTU from interface config"""
        mtu_match = re.search(r'mtu\s+(\d+)', interface_config)
        return int(mtu_match.group(1)) if mtu_match else 1500
    
    def _extract_bandwidth_from_interface(self, interface_config: str) -> int:
        """Extract bandwidth - IMPROVED"""
        bandwidth_match = re.search(r'bandwidth\s+(\d+)', interface_config)
        if bandwidth_match:
            return int(bandwidth_match.group(1))
        
        # Default bandwidth based on interface type in the interface name
        # This is extracted from the calling context, but we'll use a reasonable default
        return 100000  # Default to 100 Mbps
    
    def _extract_vlans(self, content: str) -> List[Dict]:
        """Extract VLAN configurations"""
        vlans = []
        vlan_matches = re.findall(r'vlan\s+(\d+)\s*\n\s*name\s+(\S+)', content)
        
        for vlan_id, vlan_name in vlan_matches:
            vlans.append({
                'id': int(vlan_id),
                'name': vlan_name
            })
        
        return vlans
    
    def _extract_routing_protocols(self, content: str) -> List[Dict]:
        """Extract routing protocol configurations"""
        protocols = []
        
        # OSPF detection
        ospf_match = re.search(r'router ospf\s+(\d+)', content)
        if ospf_match:
            protocols.append({
                'protocol': 'OSPF',
                'process_id': int(ospf_match.group(1))
            })
        
        # BGP detection
        bgp_match = re.search(r'router bgp\s+(\d+)', content)
        if bgp_match:
            protocols.append({
                'protocol': 'BGP',
                'as_number': int(bgp_match.group(1))
            })
        
        return protocols
    
    def _extract_ip_addresses(self, content: str) -> List[str]:
        """Extract all IP addresses from config"""
        ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
        return list(set(re.findall(ip_pattern, content)))

# Test the parser
if __name__ == "__main__":
    parser = ConfigParser()
    # Test with a sample config file
    result = parser.parse_config_file("config_files/R1.txt")
    print(json.dumps(result, indent=2))