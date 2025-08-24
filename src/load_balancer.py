# src/load_balancer.py - FIXED VERSION
import json
import networkx as nx
from typing import Dict, List, Any, Tuple
from datetime import datetime

class LoadBalancer:
    def __init__(self):
        self.balancing_strategies = {
            'bandwidth_aware': self._bandwidth_aware_balancing,
            'priority_based': self._priority_based_balancing,
            'round_robin': self._round_robin_balancing,
            'least_utilized': self._least_utilized_balancing
        }
    
    def analyze_load_balancing_opportunities(self, topology_data: Dict, traffic_analysis: Dict) -> Dict[str, Any]:
        """Analyze network for load balancing opportunities"""
        
        load_balancing_analysis = {
            'overloaded_links': [],
            'alternative_paths': {},
            'recommendations': [],
            'load_distribution_strategies': {}
        }
        
        try:
            # Identify overloaded links
            for link_id, utilization_info in traffic_analysis.get('link_utilization', {}).items():
                utilization_percent = utilization_info.get('utilization_percent', 0)
                if utilization_percent > 75:
                    load_balancing_analysis['overloaded_links'].append({
                        'link_id': link_id,
                        'utilization': utilization_percent,
                        'bandwidth_mbps': utilization_info.get('bandwidth_mbps', 100),
                        'current_traffic_mbps': utilization_info.get('traffic_mbps', 0)
                    })
            
            # Generate simple recommendations for overloaded links
            for overloaded_link in load_balancing_analysis['overloaded_links']:
                load_balancing_analysis['recommendations'].append({
                    'type': 'load_balancing',
                    'link_id': overloaded_link['link_id'],
                    'current_utilization': f"{overloaded_link['utilization']:.1f}%",
                    'recommendation': 'Consider implementing load balancing or upgrading bandwidth',
                    'priority': 'high' if overloaded_link['utilization'] > 90 else 'medium'
                })
            
            # Add general load balancing strategy
            if len(load_balancing_analysis['overloaded_links']) == 0:
                load_balancing_analysis['recommendations'].append({
                    'type': 'optimization',
                    'recommendation': 'Network utilization is healthy. Consider proactive load balancing for future growth.',
                    'priority': 'low'
                })
            
        except Exception as e:
            print(f"Warning: Load balancing analysis error: {str(e)}")
        
        return load_balancing_analysis
    
    # Define the methods referenced in __init__
    def _bandwidth_aware_balancing(self, link_info: Dict) -> Dict:
        """Bandwidth-aware load balancing strategy"""
        return {
            'strategy': 'bandwidth_aware',
            'description': 'Distribute traffic proportional to link bandwidth capacity'
        }
    
    def _priority_based_balancing(self, traffic_info: Dict) -> Dict:
        """Priority-based load balancing strategy"""
        return {
            'strategy': 'priority_based',
            'description': 'Route high-priority traffic through best available paths'
        }
    
    def _round_robin_balancing(self, available_paths: List) -> Dict:
        """Round-robin load balancing strategy"""
        return {
            'strategy': 'round_robin',
            'description': 'Distribute traffic evenly across all available paths'
        }
    
    def _least_utilized_balancing(self, path_utilization: Dict) -> Dict:
        """Least utilized path balancing strategy"""
        return {
            'strategy': 'least_utilized',
            'description': 'Route traffic through least congested paths'
        }
    
    def generate_load_balancing_report(self, topology_data: Dict, traffic_analysis: Dict, output_file: str) -> None:
        """Generate comprehensive load balancing report"""
        try:
            load_balancing_analysis = self.analyze_load_balancing_opportunities(topology_data, traffic_analysis)
            
            report = {
                'timestamp': datetime.now().isoformat(),
                'summary': {
                    'overloaded_links': len(load_balancing_analysis['overloaded_links']),
                    'alternative_paths_analyzed': len(load_balancing_analysis['alternative_paths']),
                    'recommendations_generated': len(load_balancing_analysis['recommendations']),
                    'load_distribution_strategies': len(load_balancing_analysis['load_distribution_strategies'])
                },
                'detailed_analysis': load_balancing_analysis
            }
            
            with open(output_file, 'w') as f:
                json.dump(report, f, indent=2)
            
            print(f"✅ Load balancing analysis report saved to {output_file}")
            
        except Exception as e:
            print(f"❌ Error generating load balancing report: {str(e)}")

# Test the load balancer
if __name__ == "__main__":
    try:
        # Load required data
        with open('output/network_topology.json', 'r') as f:
            topology_data = json.load(f)
        
        with open('output/traffic_analysis.json', 'r') as f:
            traffic_data = json.load(f)
            traffic_analysis = traffic_data['detailed_analysis']
        
        print("🔍 Testing Load Balancer...")
        load_balancer = LoadBalancer()
        
        # Test analysis
        analysis = load_balancer.analyze_load_balancing_opportunities(topology_data, traffic_analysis)
        print(f"✅ Analysis completed!")
        print(f"   - Overloaded links: {len(analysis['overloaded_links'])}")
        print(f"   - Recommendations: {len(analysis['recommendations'])}")
        
        # Generate report
        load_balancer.generate_load_balancing_report(topology_data, traffic_analysis, 'output/load_balancing_analysis.json')
        
    except FileNotFoundError as e:
        print(f"❌ Required file not found: {str(e)}")
        print("Run traffic_analyzer.py first to generate required files")
    except Exception as e:
        print(f"❌ Error testing load balancer: {str(e)}")
