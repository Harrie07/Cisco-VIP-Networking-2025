#!/usr/bin/env python3
# test_project.py - Comprehensive Testing Suite

import sys
import os
import json
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def setup_test_environment():
    """Set up test environment"""
    # Create output directory if it doesn't exist
    Path('output').mkdir(exist_ok=True)
    Path('config_files').mkdir(exist_ok=True)
    
    print("🔧 Test environment setup complete")

def test_config_parser():
    """Test configuration parser"""
    print("🔍 Testing Configuration Parser...")
    try:
        from config_parser import ConfigParser
        parser = ConfigParser()
        
        # Check if config files exist
        config_files = list(Path('config_files').glob('*.txt'))
        if not config_files:
            print("⚠️  No config files found in config_files/ directory")
            return False
        
        # Test with first available config file
        config_file = config_files[0]
        result = parser.parse_config_file(str(config_file))
        
        if result and result.get('device_name'):
            print(f"✅ Config Parser working! Found device: {result['device_name']}")
            print(f"   - Device type: {result.get('device_type', 'Unknown')}")
            print(f"   - Interfaces: {len(result.get('interfaces', []))}")
            print(f"   - Routing protocols: {len(result.get('routing_protocols', []))}")
            return True
        else:
            print("❌ Config Parser failed - no valid data returned")
            return False
            
    except Exception as e:
        print(f"❌ Config Parser error: {str(e)}")
        return False

def test_topology_builder():
    """Test topology builder"""
    print("\n🌐 Testing Topology Builder...")
    try:
        from network_topology import NetworkTopology
        topology = NetworkTopology()
        
        topology.build_topology_from_configs("config_files")
        summary = topology.get_topology_summary()
        
        if summary['total_devices'] > 0:
            print(f"✅ Topology Builder working!")
            print(f"   - Total devices: {summary['total_devices']}")
            print(f"   - Routers: {summary['routers']}")
            print(f"   - Switches: {summary['switches']}")
            print(f"   - Endpoints: {summary['endpoints']}")
            print(f"   - Links: {summary['total_links']}")
            
            # Export for other tests
            topology.export_to_json('output/network_topology.json')
            return True
        else:
            print("❌ Topology Builder failed - no devices found")
            return False
            
    except Exception as e:
        print(f"❌ Topology Builder error: {str(e)}")
        return False

def test_traffic_analyzer():
    """Test traffic analyzer"""
    print("\n📊 Testing Traffic Analyzer...")
    try:
        from traffic_analyzer import TrafficAnalyzer
        
        # Check if topology file exists
        if not Path('output/network_topology.json').exists():
            print("❌ Network topology file not found")
            return False
        
        # Load topology data
        with open('output/network_topology.json', 'r') as f:
            topology_data = json.load(f)
        
        analyzer = TrafficAnalyzer()
        analysis = analyzer.analyze_network_traffic(topology_data)
        
        if analysis and 'link_utilization' in analysis:
            print(f"✅ Traffic Analyzer working!")
            print(f"   - Links analyzed: {len(analysis['link_utilization'])}")
            print(f"   - Bottlenecks found: {len(analysis['bottlenecks'])}")
            print(f"   - Recommendations: {len(analysis['recommendations'])}")
            
            # Export for other tests
            analyzer.generate_traffic_report(topology_data, 'output/traffic_analysis.json')
            return True
        else:
            print("❌ Traffic Analyzer failed")
            return False
            
    except Exception as e:
        print(f"❌ Traffic Analyzer error: {str(e)}")
        return False

def test_load_balancer():
    """Test load balancer"""
    print("\n⚖️  Testing Load Balancer...")
    try:
        from load_balancer import LoadBalancer
        
        # Check required files
        required_files = ['output/network_topology.json', 'output/traffic_analysis.json']
        for file_path in required_files:
            if not Path(file_path).exists():
                print(f"❌ Required file {file_path} not found")
                return False
        
        # Load data
        with open('output/network_topology.json', 'r') as f:
            topology_data = json.load(f)
        
        with open('output/traffic_analysis.json', 'r') as f:
            traffic_data = json.load(f)
            traffic_analysis = traffic_data['detailed_analysis']
        
        load_balancer = LoadBalancer()
        analysis = load_balancer.analyze_load_balancing_opportunities(topology_data, traffic_analysis)
        
        print(f"✅ Load Balancer working!")
        print(f"   - Overloaded links: {len(analysis['overloaded_links'])}")
        print(f"   - Alternative paths found: {len(analysis['alternative_paths'])}")
        print(f"   - Recommendations: {len(analysis['recommendations'])}")
        
        return True
            
    except Exception as e:
        print(f"❌ Load Balancer error: {str(e)}")
        return False

def test_validator():
    """Test network validator"""
    print("\n🔍 Testing Network Validator...")
    try:
        from validator import NetworkValidator
        
        # Check required files
        if not Path('output/network_topology.json').exists():
            print("❌ Network topology file not found")
            return False
        
        # Load data
        with open('output/network_topology.json', 'r') as f:
            topology_data = json.load(f)
        
        # Try to load traffic analysis (optional)
        traffic_analysis = None
        if Path('output/traffic_analysis.json').exists():
            with open('output/traffic_analysis.json', 'r') as f:
                traffic_data = json.load(f)
                traffic_analysis = traffic_data['detailed_analysis']
        
        validator = NetworkValidator()
        results = validator.validate_network_configuration(topology_data, traffic_analysis)
        
        print(f"✅ Network Validator working!")
        print(f"   - Overall score: {results['overall_score']:.1f}%")
        print(f"   - Passed checks: {results['passed_checks']}")
        print(f"   - Failed checks: {results['failed_checks']}")
        print(f"   - Warnings: {results['warnings']}")
        print(f"   - Critical issues: {len(results['critical_issues'])}")
        
        return True
            
    except Exception as e:
        print(f"❌ Network Validator error: {str(e)}")
        return False

def run_complete_test():
    """Run complete system test"""
    print("🚀 Cisco VIP 2025 - Network Analysis Tool")
    print("=" * 50)
    print("Starting Comprehensive System Test...\n")
    
    # Setup test environment
    setup_test_environment()
    
    # Define test sequence
    tests = [
        ("Configuration Parser", test_config_parser),
        ("Topology Builder", test_topology_builder),
        ("Traffic Analyzer", test_traffic_analyzer),
        ("Load Balancer", test_load_balancer),
        ("Network Validator", test_validator)
    ]
    
    passed = 0
    total = len(tests)
    failed_tests = []
    
    # Run tests
    for test_name, test_function in tests:
        try:
            if test_function():
                passed += 1
            else:
                failed_tests.append(test_name)
        except Exception as e:
            print(f"❌ {test_name} crashed: {str(e)}")
            failed_tests.append(test_name)
    
    # Results summary
    print("\n" + "=" * 50)
    print("📋 TEST RESULTS SUMMARY")
    print("=" * 50)
    print(f"Total Tests: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")
    print(f"Success Rate: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Your system is working perfectly!")
        print("✅ Ready for production use")
    elif passed > total // 2:
        print(f"\n✅ Most tests passed! {passed}/{total} components working")
        if failed_tests:
            print(f"⚠️  Failed components: {', '.join(failed_tests)}")
    else:
        print(f"\n❌ Multiple failures detected. Failed components:")
        for test in failed_tests:
            print(f"   - {test}")
    
    print("\n📁 Generated files:")
    output_files = list(Path('output').glob('*.json'))
    for file_path in output_files:
        print(f"   - {file_path}")

if __name__ == "__main__":
    run_complete_test()
