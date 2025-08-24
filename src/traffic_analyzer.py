# src/traffic_analyzer.py - FIXED VERSION
import json
import os
from typing import Dict, List, Any
from datetime import datetime

class TrafficAnalyzer:
    def __init__(self):
        # Simplified application profiles (in Mbps)
        self.application_profiles = {
            'video_streaming': {'regular': 15, 'peak': 25, 'priority': 'high'},
            'voip': {'regular': 0.3, 'peak': 0.5, 'priority': 'critical'},
            'web_browsing': {'regular': 2, 'peak': 5, 'priority': 'medium'},
            'iot_sensors': {'regular': 0.05, 'peak': 0.1, 'priority': 'low'},
            'file_transfer': {'regular': 20, 'peak': 100, 'priority': 'medium'}
        }
    
    def analyze_network_traffic(self, topology_data: Dict, current_hour: int = 14) -> Dict[str, Any]:
        """Analyze traffic patterns across the network - SIMPLIFIED"""
        try:
            traffic_analysis = {
                'link_utilization': {},
                'device_load': {},
                'bottlenecks': [],
                'recommendations': [],
                'peak_scenarios': {}
            }
            
            # Analyze device loads (simplified)
            for device_id, device_config in topology_data.get('devices', {}).items():
                if device_config.get('device_type') == 'endpoint':
                    device_load = self._calculate_simple_device_load(device_config, current_hour)
                    traffic_analysis['device_load'][device_id] = device_load
            
            # Analyze link utilization (simplified)
            for link_id, link_info in topology_data.get('links', {}).items():
                link_utilization = self._calculate_simple_link_utilization(link_info, traffic_analysis['device_load'])
                traffic_analysis['link_utilization'][link_id] = link_utilization
                
                # Check for bottlenecks
                if link_utilization['utilization_percent'] > 80:
                    traffic_analysis['bottlenecks'].append({
                        'link_id': link_id,
                        'utilization': link_utilization['utilization_percent'],
                        'severity': 'critical' if link_utilization['utilization_percent'] > 90 else 'warning'
                    })
            
            # Generate simple recommendations
            traffic_analysis['recommendations'] = self._generate_simple_recommendations(traffic_analysis)
            
            return traffic_analysis
            
        except Exception as e:
            print(f"Error in traffic analysis: {str(e)}")
            # Return basic structure even if analysis fails
            return {
                'link_utilization': {},
                'device_load': {},
                'bottlenecks': [],
                'recommendations': [],
                'peak_scenarios': {},
                'error': str(e)
            }
    
    def _calculate_simple_device_load(self, device_config: Dict, current_hour: int) -> Dict[str, Any]:
        """Calculate simple device load"""
        device_load = {
            'total_regular_mbps': 0,
            'total_peak_mbps': 0,
            'applications': [],
            'current_load_mbps': 0
        }
        
        # Default to web browsing if no specific applications found
        default_apps = ['web_browsing']
        
        # Check if device config mentions specific applications
        device_str = str(device_config).lower()
        detected_apps = []
        for app_name in self.application_profiles.keys():
            if app_name in device_str:
                detected_apps.append(app_name)
        
        apps_to_analyze = detected_apps if detected_apps else default_apps
        
        for app_name in apps_to_analyze:
            if app_name in self.application_profiles:
                app_profile = self.application_profiles[app_name]
                
                # Simple time-based load calculation
                if 9 <= current_hour <= 17:  # Business hours
                    current_load = app_profile['peak']
                else:
                    current_load = app_profile['regular']
                
                app_load_info = {
                    'application': app_name,
                    'regular_load_mbps': app_profile['regular'],
                    'peak_load_mbps': app_profile['peak'],
                    'current_load_mbps': current_load,
                    'priority': app_profile['priority']
                }
                
                device_load['applications'].append(app_load_info)
                device_load['total_regular_mbps'] += app_profile['regular']
                device_load['total_peak_mbps'] += app_profile['peak']
                device_load['current_load_mbps'] += current_load
        
        return device_load
    
    def _calculate_simple_link_utilization(self, link_info: Dict, device_loads: Dict) -> Dict[str, Any]:
        """Calculate simple link utilization"""
        # Get link bandwidth
        link_bandwidth = link_info.get('bandwidth_mbps', 100)  # Default 100 Mbps
        
        # Calculate total traffic (simplified)
        total_traffic = 0
        
        # Add traffic from endpoints (simplified calculation)
        device1_id = link_info.get('device1', {}).get('device_id', '')
        device2_id = link_info.get('device2', {}).get('device_id', '')
        
        # Simple traffic estimation based on connected devices
        for device_id, load_info in device_loads.items():
            # If this device might use this link, add its traffic
            total_traffic += load_info.get('current_load_mbps', 0) * 0.5  # 50% of device traffic per link
        
        # Calculate utilization
        utilization_percent = min((total_traffic / link_bandwidth) * 100, 100) if link_bandwidth > 0 else 0
        
        return {
            'bandwidth_mbps': link_bandwidth,
            'traffic_mbps': total_traffic,
            'utilization_percent': utilization_percent,
            'status': 'healthy' if utilization_percent < 70 else 'congested' if utilization_percent < 90 else 'critical'
        }
    
    def _generate_simple_recommendations(self, traffic_analysis: Dict) -> List[Dict]:
        """Generate simple recommendations"""
        recommendations = []
        
        # Check for high utilization links
        for link_id, utilization_info in traffic_analysis['link_utilization'].items():
            if utilization_info['utilization_percent'] > 80:
                recommendations.append({
                    'type': 'capacity_upgrade',
                    'link': link_id,
                    'current_utilization': f"{utilization_info['utilization_percent']:.1f}%",
                    'recommendation': f"Consider upgrading link bandwidth from {utilization_info['bandwidth_mbps']} Mbps",
                    'priority': 'high' if utilization_info['utilization_percent'] > 90 else 'medium'
                })
        
        # Add general recommendations
        if len(traffic_analysis['bottlenecks']) > 0:
            recommendations.append({
                'type': 'load_balancing',
                'recommendation': 'Consider implementing load balancing for high-utilization links',
                'priority': 'medium',
                'affected_links': len(traffic_analysis['bottlenecks'])
            })
        
        return recommendations
    
    def generate_traffic_report(self, topology_data: Dict, output_file: str) -> None:
        """Generate traffic analysis report"""
        try:
            analysis_results = self.analyze_network_traffic(topology_data)
            
            report = {
                'timestamp': datetime.now().isoformat(),
                'analysis_summary': {
                    'total_devices_analyzed': len(topology_data.get('devices', {})),
                    'total_links_analyzed': len(topology_data.get('links', {})),
                    'bottlenecks_found': len(analysis_results['bottlenecks']),
                    'recommendations_generated': len(analysis_results['recommendations'])
                },
                'detailed_analysis': analysis_results
            }
            
            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            
            with open(output_file, 'w') as f:
                json.dump(report, f, indent=2)
            
            print(f"✅ Traffic analysis report saved to {output_file}")
            
        except Exception as e:
            print(f"❌ Error generating traffic report: {str(e)}")
            # Create minimal report even if analysis fails
            minimal_report = {
                'timestamp': datetime.now().isoformat(),
                'error': str(e),
                'analysis_summary': {'error': 'Analysis failed'},
                'detailed_analysis': {'error': str(e)}
            }
            
            try:
                os.makedirs(os.path.dirname(output_file), exist_ok=True)
                with open(output_file, 'w') as f:
                    json.dump(minimal_report, f, indent=2)
            except:
                pass

# Test the traffic analyzer
if __name__ == "__main__":
    try:
        # Load topology data
        if os.path.exists('output/network_topology.json'):
            with open('output/network_topology.json', 'r') as f:
                topology_data = json.load(f)
            
            print("🔍 Testing Traffic Analyzer...")
            analyzer = TrafficAnalyzer()
            
            # Test analysis
            analysis = analyzer.analyze_network_traffic(topology_data)
            print(f"✅ Analysis completed!")
            print(f"   - Links analyzed: {len(analysis['link_utilization'])}")
            print(f"   - Device loads calculated: {len(analysis['device_load'])}")
            print(f"   - Bottlenecks found: {len(analysis['bottlenecks'])}")
            print(f"   - Recommendations: {len(analysis['recommendations'])}")
            
            # Generate report
            analyzer.generate_traffic_report(topology_data, 'output/traffic_analysis.json')
            
        else:
            print("❌ Network topology file not found. Run network_topology.py first.")
            
    except Exception as e:
        print(f"❌ Error testing traffic analyzer: {str(e)}")
