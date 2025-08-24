# src/validator.py
import json
import re
import networkx as nx
from typing import Dict, List, Any, Set, Tuple
from collections import defaultdict

class NetworkValidator:
    def __init__(self):
        self.validation_rules = {
            'ip_conflicts': self.check_ip_conflicts,
            'vlan_consistency': self.check_vlan_consistency,
            'gateway_validation': self.check_gateway_configuration,
            'mtu_mismatches': self.check_mtu_mismatches,
            'network_loops': self.check_network_loops,
            'missing_components': self.check_missing_components,
            'routing_optimization': self.check_routing_protocol_optimization,
            'security_zones': self.check_security_zones,
            'redundancy_analysis': self.check_redundancy,
            'capacity_validation': self.check_capacity_adequacy
        }
    
    def validate_network_configuration(self, topology_data: Dict, traffic_analysis: Dict = None) -> Dict[str, Any]:
        """Run comprehensive network validation"""
        validation_results = {
            'overall_score': 0,
            'total_checks': len(self.validation_rules),
            'passed_checks': 0,
            'failed_checks': 0,
            'warnings': 0,
            'critical_issues': [],
            'warnings_list': [],
            'optimization_suggestions': [],
            'detailed_results': {}
        }
        
        for rule_name, rule_function in self.validation_rules.items():
            try:
                if rule_name == 'capacity_validation' and traffic_analysis:
                    result = rule_function(topology_data, traffic_analysis)
                else:
                    result = rule_function(topology_data)
                
                validation_results['detailed_results'][rule_name] = result
                
                if result['status'] == 'pass':
                    validation_results['passed_checks'] += 1
                elif result['status'] == 'fail':
                    validation_results['failed_checks'] += 1
                    validation_results['critical_issues'].extend(result.get('issues', []))
                elif result['status'] == 'warning':
                    validation_results['warnings'] += 1
                    validation_results['warnings_list'].extend(result.get('issues', []))
                
                validation_results['optimization_suggestions'].extend(result.get('suggestions', []))
                
            except Exception as e:
                validation_results['detailed_results'][rule_name] = {
                    'status': 'error',
                    'error': str(e)
                }
        
        # Calculate overall score
        total_checks = validation_results['passed_checks'] + validation_results['failed_checks'] + validation_results['warnings']
        if total_checks > 0:
            validation_results['overall_score'] = (
                (validation_results['passed_checks'] * 100 + validation_results['warnings'] * 50) / 
                (total_checks * 100) * 100
            )
        
        return validation_results
    
    def check_ip_conflicts(self, topology_data: Dict) -> Dict[str, Any]:
        """Check for duplicate IP addresses within the same VLAN/subnet"""
        ip_usage = defaultdict(list)
        conflicts = []
        
        for device_id, device_config in topology_data['devices'].items():
            for interface in device_config.get('interfaces', []):
                ip_address = interface.get('ip_address')
                vlan = interface.get('vlan', 'default')
                
                if ip_address:
                    ip_usage[(ip_address, vlan)].append({
                        'device': device_id,
                        'interface': interface['name'],
                        'vlan': vlan
                    })
        
        for (ip, vlan), devices in ip_usage.items():
            if len(devices) > 1:
                conflicts.append({
                    'ip_address': ip,
                    'vlan': vlan,
                    'conflicting_devices': devices,
                    'severity': 'critical'
                })
        
        return {
            'status': 'fail' if conflicts else 'pass',
            'issues': conflicts,
            'suggestions': [f"Resolve IP conflict for {conflict['ip_address']} in VLAN {conflict['vlan']}" 
                           for conflict in conflicts]
        }
    
    def check_vlan_consistency(self, topology_data: Dict) -> Dict[str, Any]:
        """Check VLAN configuration consistency"""
        vlan_configs = defaultdict(set)
        vlan_issues = []
        
        for device_id, device_config in topology_data['devices'].items():
            # Check VLAN definitions
            for vlan in device_config.get('vlans', []):
                vlan_id = vlan.get('id')
                vlan_name = vlan.get('name')
                
                if vlan_id:
                    vlan_configs[vlan_id].add(vlan_name)
            
            # Check interface VLAN assignments
            for interface in device_config.get('interfaces', []):
                vlan = interface.get('vlan')
                if vlan and vlan not in [v.get('id') for v in device_config.get('vlans', [])]:
                    vlan_issues.append({
                        'device': device_id,
                        'interface': interface['name'],
                        'issue': f'Interface assigned to undefined VLAN {vlan}',
                        'severity': 'warning'
                    })
        
        # Check for VLAN name inconsistencies
        for vlan_id, names in vlan_configs.items():
            if len(names) > 1:
                vlan_issues.append({
                    'vlan_id': vlan_id,
                    'issue': f'VLAN {vlan_id} has inconsistent names: {", ".join(names)}',
                    'severity': 'warning'
                })
        
        return {
            'status': 'warning' if vlan_issues else 'pass',
            'issues': vlan_issues,
            'suggestions': ['Standardize VLAN naming conventions across all devices']
        }
    
    def check_gateway_configuration(self, topology_data: Dict) -> Dict[str, Any]:
        """Validate gateway configurations"""
        gateway_issues = []
        subnet_gateways = defaultdict(list)
        
        # Collect all gateway configurations
        for device_id, device_config in topology_data['devices'].items():
            for interface in device_config.get('interfaces', []):
                ip_address = interface.get('ip_address')
                subnet_mask = interface.get('subnet_mask')
                
                if ip_address and subnet_mask:
                    subnet = self._calculate_subnet(ip_address, subnet_mask)
                    
                    if device_config['device_type'] == 'router':
                        subnet_gateways[subnet].append({
                            'device': device_id,
                            'interface': interface['name'],
                            'ip': ip_address
                        })
        
        # Check for missing gateways
        for link_id, link_info in topology_data['links'].items():
            subnet = link_info.get('subnet')
            if subnet and subnet not in subnet_gateways:
                gateway_issues.append({
                    'subnet': subnet,
                    'issue': f'No router gateway found for subnet {subnet}',
                    'severity': 'critical',
                    'link_id': link_id
                })
        
        # Check for multiple gateways in same subnet
        for subnet, gateways in subnet_gateways.items():
            if len(gateways) > 1:
                gateway_issues.append({
                    'subnet': subnet,
                    'issue': f'Multiple gateways detected in subnet {subnet}',
                    'gateways': gateways,
                    'severity': 'warning',
                    'suggestion': 'Consider implementing HSRP/VRRP for gateway redundancy'
                })
        
        return {
            'status': 'fail' if any(issue['severity'] == 'critical' for issue in gateway_issues) else 'warning' if gateway_issues else 'pass',
            'issues': gateway_issues,
            'suggestions': ['Verify default gateway configuration on all subnets']
        }
    
    def check_mtu_mismatches(self, topology_data: Dict) -> Dict[str, Any]:
        """Check for MTU mismatches between connected interfaces"""
        mtu_issues = []
        
        for link_id, link_info in topology_data['links'].items():
            device1_interfaces = self._get_device_interfaces(topology_data, link_info['device1']['device_id'])
            device2_interfaces = self._get_device_interfaces(topology_data, link_info['device2']['device_id'])
            
            # Find interfaces on the same subnet
            subnet = link_info.get('subnet')
            device1_mtu = self._get_interface_mtu_for_subnet(device1_interfaces, subnet)
            device2_mtu = self._get_interface_mtu_for_subnet(device2_interfaces, subnet)
            
            if device1_mtu and device2_mtu and device1_mtu != device2_mtu:
                mtu_issues.append({
                    'link_id': link_id,
                    'device1': link_info['device1']['device_id'],
                    'device1_mtu': device1_mtu,
                    'device2': link_info['device2']['device_id'],
                    'device2_mtu': device2_mtu,
                    'severity': 'warning'
                })
        
        return {
            'status': 'warning' if mtu_issues else 'pass',
            'issues': mtu_issues,
            'suggestions': [f'Standardize MTU settings on link {issue["link_id"]}' for issue in mtu_issues]
        }
    
    def check_network_loops(self, topology_data: Dict) -> Dict[str, Any]:
        """Detect potential network loops"""
        # Build graph for loop detection
        graph = nx.Graph()
        
        for device_id, device_config in topology_data['devices'].items():
            if device_config['device_type'] in ['router', 'switch']:
                graph.add_node(device_id, device_type=device_config['device_type'])
        
        for link_id, link_info in topology_data['links'].items():
            device1 = link_info['device1']['device_id']
            device2 = link_info['device2']['device_id']
            
            if device1 in graph and device2 in graph:
                graph.add_edge(device1, device2, link_id=link_id)
        
        # Find cycles (potential loops)
        loops = []
        try:
            cycles = list(nx.simple_cycles(nx.DiGraph(graph)))
            for cycle in cycles:
                if len(cycle) > 2:  # Ignore direct back-and-forth connections
                    loops.append({
                        'devices_in_loop': cycle,
                        'loop_length': len(cycle),
                        'severity': 'warning',
                        'recommendation': 'Verify spanning-tree protocol configuration'
                    })
        except:
            # NetworkX might not find cycles in undirected graph, use alternative method
            pass
        
        # Check for spanning tree configuration in switches
        stp_issues = []
        for device_id, device_config in topology_data['devices'].items():
            if device_config['device_type'] == 'switch':
                # This is a simplified check - in reality, you'd parse the actual config
                device_str = str(device_config)
                if 'spanning-tree' not in device_str.lower():
                    stp_issues.append({
                        'device': device_id,
                        'issue': 'No spanning-tree configuration detected',
                        'severity': 'warning'
                    })
        
        all_issues = loops + stp_issues
        
        return {
            'status': 'warning' if all_issues else 'pass',
            'issues': all_issues,
            'suggestions': ['Enable and configure spanning-tree protocol on all switches', 
                           'Consider implementing rapid spanning-tree (RSTP) for faster convergence']
        }
    
    def check_missing_components(self, topology_data: Dict) -> Dict[str, Any]:
        """Check for missing network components"""
        missing_components = []
        
        # Check for isolated endpoints (no path to router)
        graph = nx.Graph()
        routers = []
        endpoints = []
        
        for device_id, device_config in topology_data['devices'].items():
            graph.add_node(device_id)
            if device_config['device_type'] == 'router':
                routers.append(device_id)
            elif device_config['device_type'] == 'endpoint':
                endpoints.append(device_id)
        
        for link_id, link_info in topology_data['links'].items():
            device1 = link_info['device1']['device_id']
            device2 = link_info['device2']['device_id']
            graph.add_edge(device1, device2)
        
        # Check connectivity from endpoints to routers
        for endpoint in endpoints:
            connected_to_router = False
            for router in routers:
                if nx.has_path(graph, endpoint, router):
                    connected_to_router = True
                    break
            
            if not connected_to_router:
                missing_components.append({
                    'endpoint': endpoint,
                    'issue': f'Endpoint {endpoint} has no path to any router',
                    'severity': 'critical',
                    'suggestion': f'Add switch/router configuration for {endpoint} connectivity'
                })
        
        # Check for subnets without DHCP servers (simplified check)
        subnets = set()
        dhcp_servers = set()
        
        for link_id, link_info in topology_data['links'].items():
            subnet = link_info.get('subnet')
            if subnet:
                subnets.add(subnet)
        
        # In a real implementation, you'd check for DHCP server configurations
        # For now, assume routers can provide DHCP
        for subnet in subnets:
            # This is a simplified check
            if len(routers) == 0:
                missing_components.append({
                    'subnet': subnet,
                    'issue': f'No DHCP server configuration found for subnet {subnet}',
                    'severity': 'warning',
                    'suggestion': 'Configure DHCP server or DHCP relay agent'
                })
        
        return {
            'status': 'fail' if any(issue['severity'] == 'critical' for issue in missing_components) else 'warning' if missing_components else 'pass',
            'issues': missing_components,
            'suggestions': ['Ensure all endpoints have connectivity to network infrastructure']
        }
    
    def check_routing_protocol_optimization(self, topology_data: Dict) -> Dict[str, Any]:
        """Check routing protocol configuration and suggest optimizations"""
        routing_issues = []
        router_count = len([d for d in topology_data['devices'].values() if d['device_type'] == 'router'])
        
        # Analyze current routing protocols
        protocol_usage = defaultdict(int)
        for device_id, device_config in topology_data['devices'].items():
            if device_config['device_type'] == 'router':
                for protocol in device_config.get('routing_protocols', []):
                    protocol_name = protocol.get('protocol', 'unknown')
                    protocol_usage[protocol_name] += 1
        
        # Recommend BGP for large networks
        if router_count > 20 and protocol_usage.get('OSPF', 0) > protocol_usage.get('BGP', 0):
            routing_issues.append({
                'issue': f'Network with {router_count} routers using primarily OSPF',
                'recommendation': 'Consider migrating to BGP for better scalability',
                'severity': 'suggestion',
                'router_count': router_count
            })
        
        # Check for mixed routing protocols
        if len(protocol_usage) > 1:
            routing_issues.append({
                'issue': f'Multiple routing protocols detected: {list(protocol_usage.keys())}',
                'recommendation': 'Consider standardizing on a single routing protocol',
                'severity': 'warning',
                'protocols': dict(protocol_usage)
            })
        
        # Check for single points of failure in routing
        if router_count == 1:
            routing_issues.append({
                'issue': 'Single router detected - no routing redundancy',
                'recommendation': 'Add redundant routers for high availability',
                'severity': 'warning'
            })
        
        return {
            'status': 'pass' if not routing_issues else 'warning',
            'issues': routing_issues,
            'suggestions': ['Optimize routing protocol selection based on network size and requirements']
        }
    
    def check_security_zones(self, topology_data: Dict) -> Dict[str, Any]:
        """Check network segmentation and security zones"""
        security_issues = []
        
        # Check VLAN segmentation
        vlan_count = len(set(
            interface.get('vlan')
            for device_config in topology_data['devices'].values()
            for interface in device_config.get('interfaces', [])
            if interface.get('vlan')
        ))
        
        device_count = len(topology_data['devices'])
        
        if device_count > 10 and vlan_count < 3:
            security_issues.append({
                'issue': f'Network with {device_count} devices using only {vlan_count} VLANs',
                'recommendation': 'Implement network segmentation with additional VLANs',
                'severity': 'suggestion'
            })
        
        # Check for default VLAN usage
        default_vlan_devices = []
        for device_id, device_config in topology_data['devices'].items():
            for interface in device_config.get('interfaces', []):
                if interface.get('vlan') == 1:  # Default VLAN
                    default_vlan_devices.append(device_id)
        
        if default_vlan_devices:
            security_issues.append({
                'issue': f'Devices using default VLAN 1: {default_vlan_devices}',
                'recommendation': 'Avoid using default VLAN for production traffic',
                'severity': 'warning'
            })
        
        return {
            'status': 'warning' if security_issues else 'pass',
            'issues': security_issues,
            'suggestions': ['Implement proper network segmentation and security zones']
        }
    
    def check_redundancy(self, topology_data: Dict) -> Dict[str, Any]:
        """Check network redundancy and single points of failure"""
        redundancy_issues = []
        
        # Build graph for connectivity analysis
        graph = nx.Graph()
        for device_id in topology_data['devices'].keys():
            graph.add_node(device_id)
        
        for link_id, link_info in topology_data['links'].items():
            device1 = link_info['device1']['device_id']
            device2 = link_info['device2']['device_id']
            graph.add_edge(device1, device2)
        
        # Find articulation points (single points of failure)
        articulation_points = list(nx.articulation_points(graph))
        
        for node in articulation_points:
            device_type = topology_data['devices'][node]['device_type']
            redundancy_issues.append({
                'device': node,
                'device_type': device_type,
                'issue': f'{device_type} {node} is a single point of failure',
                'recommendation': f'Add redundant paths around {node}',
                'severity': 'critical' if device_type == 'router' else 'warning'
            })
        
        # Check bridge connectivity (links whose removal would disconnect the network)
        bridges = list(nx.bridges(graph))
        for bridge in bridges:
            device1, device2 = bridge
            redundancy_issues.append({
                'link': f'{device1}-{device2}',
                'issue': f'Link between {device1} and {device2} is a single point of failure',
                'recommendation': 'Add redundant links or alternative paths',
                'severity': 'warning'
            })
        
        return {
            'status': 'fail' if any(issue['severity'] == 'critical' for issue in redundancy_issues) else 'warning' if redundancy_issues else 'pass',
            'issues': redundancy_issues,
            'suggestions': ['Implement redundant paths and eliminate single points of failure']
        }
    
    def check_capacity_adequacy(self, topology_data: Dict, traffic_analysis: Dict) -> Dict[str, Any]:
        """Check if network capacity is adequate for current and projected traffic"""
        capacity_issues = []
        
        if not traffic_analysis:
            return {'status': 'pass', 'issues': [], 'suggestions': []}
        
        link_utilization = traffic_analysis.get('link_utilization', {})
        
        for link_id, utilization_info in link_utilization.items():
            utilization_percent = utilization_info.get('utilization_percent', 0)
            
            if utilization_percent > 90:
                capacity_issues.append({
                    'link_id': link_id,
                    'utilization': utilization_percent,
                    'issue': f'Link {link_id} critically overloaded at {utilization_percent:.1f}%',
                    'recommendation': f'Immediate capacity upgrade required',
                    'severity': 'critical'
                })
            elif utilization_percent > 75:
                capacity_issues.append({
                    'link_id': link_id,
                    'utilization': utilization_percent,
                    'issue': f'Link {link_id} approaching capacity at {utilization_percent:.1f}%',
                    'recommendation': f'Plan capacity upgrade or load balancing',
                    'severity': 'warning'
                })
        
        return {
            'status': 'fail' if any(issue['severity'] == 'critical' for issue in capacity_issues) else 'warning' if capacity_issues else 'pass',
            'issues': capacity_issues,
            'suggestions': ['Monitor link utilization and plan capacity upgrades proactively']
        }
    
    # Helper methods
    def _calculate_subnet(self, ip_address: str, subnet_mask: str) -> str:
        """Calculate subnet from IP address and mask"""
        try:
            ip_parts = [int(x) for x in ip_address.split('.')]
            mask_parts = [int(x) for x in subnet_mask.split('.')]
            subnet_parts = [ip_parts[i] & mask_parts[i] for i in range(4)]
            return '.'.join(map(str, subnet_parts))
        except:
            return ip_address
    
    def _get_device_interfaces(self, topology_data: Dict, device_id: str) -> List[Dict]:
        """Get all interfaces for a device"""
        device_config = topology_data['devices'].get(device_id, {})
        return device_config.get('interfaces', [])
    
    def _get_interface_mtu_for_subnet(self, interfaces: List[Dict], subnet: str) -> int:
        """Get MTU for interface in specific subnet"""
        for interface in interfaces:
            ip_address = interface.get('ip_address')
            subnet_mask = interface.get('subnet_mask')
            
            if ip_address and subnet_mask:
                interface_subnet = self._calculate_subnet(ip_address, subnet_mask)
                if interface_subnet == subnet:
                    return interface.get('mtu', 1500)
        
        return None
    
    def generate_validation_report(self, topology_data: Dict, traffic_analysis: Dict, output_file: str) -> None:
        """Generate comprehensive validation report"""
        validation_results = self.validate_network_configuration(topology_data, traffic_analysis)
        
        report = {
            'timestamp': json.dumps(dict(), default=str),
            'validation_summary': {
                'overall_score': validation_results['overall_score'],
                'total_checks': validation_results['total_checks'],
                'passed_checks': validation_results['passed_checks'],
                'failed_checks': validation_results['failed_checks'],
                'warnings': validation_results['warnings'],
                'critical_issues_count': len(validation_results['critical_issues']),
                'optimization_opportunities': len(validation_results['optimization_suggestions'])
            },
            'detailed_results': validation_results
        }
        
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"Network validation report saved to {output_file}")

# Test the validator
if __name__ == "__main__":
    # Load required data
    with open('output/network_topology.json', 'r') as f:
        topology_data = json.load(f)
    
    try:
        with open('output/traffic_analysis.json', 'r') as f:
            traffic_data = json.load(f)
            traffic_analysis = traffic_data['detailed_analysis']
    except:
        traffic_analysis = None
    
    validator = NetworkValidator()
    validator.generate_validation_report(topology_data, traffic_analysis, 'output/validation_report.json')
