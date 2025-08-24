#!/usr/bin/env python3
# src/main.py - Main CLI Interface

import sys
import json
import argparse
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress
import time

# Import your modules
from config_parser import ConfigParser
from network_topology import NetworkTopology
from traffic_analyzer import TrafficAnalyzer
from load_balancer import LoadBalancer
from validator import NetworkValidator

console = Console()

class CiscoNetworkAnalyzer:
    def __init__(self):
        self.console = Console()
        self.topology = None
        self.traffic_analysis = None
        
    def run_complete_analysis(self, config_dir: str, output_dir: str = 'output'):
        """Run complete network analysis"""
        
        # Create header
        self.console.print(Panel.fit(
            "🚀 Cisco VIP 2025 - Network Analysis Tool\n"
            "Comprehensive Network Topology & Performance Analysis",
            style="bold blue"
        ))
        
        with Progress() as progress:
            # Task tracking
            parse_task = progress.add_task("[cyan]Parsing configurations...", total=100)
            topology_task = progress.add_task("[green]Building topology...", total=100)
            traffic_task = progress.add_task("[yellow]Analyzing traffic...", total=100)
            balance_task = progress.add_task("[magenta]Load balancing analysis...", total=100)
            validate_task = progress.add_task("[red]Validating configuration...", total=100)
            
            # Step 1: Parse configurations
            progress.update(parse_task, advance=50)
            topology = NetworkTopology()
            topology.build_topology_from_configs(config_dir)
            progress.update(parse_task, completed=100)
            
            # Step 2: Build topology
            progress.update(topology_task, advance=50)
            topology.export_to_json(f'{output_dir}/network_topology.json')
            progress.update(topology_task, completed=100)
            
            # Load topology data
            with open(f'{output_dir}/network_topology.json', 'r') as f:
                topology_data = json.load(f)
            
            # Step 3: Traffic analysis
            progress.update(traffic_task, advance=50)
            analyzer = TrafficAnalyzer()
            analyzer.generate_traffic_report(topology_data, f'{output_dir}/traffic_analysis.json')
            progress.update(traffic_task, completed=100)
            
            # Load traffic data
            with open(f'{output_dir}/traffic_analysis.json', 'r') as f:
                traffic_data = json.load(f)
                traffic_analysis = traffic_data['detailed_analysis']
            
            # Step 4: Load balancing analysis
            progress.update(balance_task, advance=50)
            load_balancer = LoadBalancer()
            load_balancer.generate_load_balancing_report(
                topology_data, traffic_analysis, f'{output_dir}/load_balancing.json'
            )
            progress.update(balance_task, completed=100)
            
            # Step 5: Network validation
            progress.update(validate_task, advance=50)
            validator = NetworkValidator()
            validator.generate_validation_report(
                topology_data, traffic_analysis, f'{output_dir}/validation.json'
            )
            progress.update(validate_task, completed=100)
        
        # Display results
        self._display_results(topology_data, traffic_analysis, f'{output_dir}/validation.json')
    
    def _display_results(self, topology_data, traffic_analysis, validation_file):
        """Display analysis results in a formatted table"""
        
        # Network Summary Table
        summary_table = Table(title="Network Analysis Summary")
        summary_table.add_column("Metric", style="cyan")
        summary_table.add_column("Value", style="green")
        
        summary = topology_data['summary']
        summary_table.add_row("Total Devices", str(summary['total_devices']))
        summary_table.add_row("Routers", str(summary['routers']))
        summary_table.add_row("Switches", str(summary['switches']))
        summary_table.add_row("Endpoints", str(summary['endpoints']))
        summary_table.add_row("Network Links", str(summary['total_links']))
        summary_table.add_row("Subnets", str(summary['subnets']))
        
        self.console.print(summary_table)
        
        # Traffic Analysis Table
        traffic_table = Table(title="Traffic Analysis Results")
        traffic_table.add_column("Link", style="cyan")
        traffic_table.add_column("Bandwidth", style="yellow")
        traffic_table.add_column("Utilization", style="green")
        traffic_table.add_column("Status", style="red")
        
        for link_id, utilization in traffic_analysis['link_utilization'].items():
            status = "🟢 Healthy" if utilization['utilization_percent'] < 70 else "🟡 Warning" if utilization['utilization_percent'] < 90 else "🔴 Critical"
            traffic_table.add_row(
                link_id,
                f"{utilization['bandwidth_mbps']} Mbps",
                f"{utilization['utilization_percent']:.1f}%",
                status
            )
        
        self.console.print(traffic_table)
        
        # Load validation results
        with open(validation_file, 'r') as f:
            validation_data = json.load(f)
        
        validation_summary = validation_data['validation_summary']
        
        # Validation Results
        validation_panel = Panel(
            f"🔍 Validation Score: {validation_summary['overall_score']:.1f}%\n"
            f"✅ Passed Checks: {validation_summary['passed_checks']}\n"
            f"❌ Failed Checks: {validation_summary['failed_checks']}\n"
            f"⚠️  Warnings: {validation_summary['warnings']}\n"
            f"🚨 Critical Issues: {validation_summary['critical_issues_count']}",
            title="Network Validation Results",
            style="bold"
        )
        
        self.console.print(validation_panel)
        
        # Success message
        self.console.print(Panel(
            "✅ Analysis Complete!\n"
            f"📁 Detailed reports saved in output/ directory\n"
            f"📊 Network topology: output/network_topology.json\n"
            f"📈 Traffic analysis: output/traffic_analysis.json\n"
            f"⚖️  Load balancing: output/load_balancing.json\n"
            f"🔍 Validation report: output/validation.json",
            title="Success",
            style="bold green"
        ))

def main():
    parser = argparse.ArgumentParser(description='Cisco VIP 2025 - Network Analysis Tool')
    parser.add_argument('--config-dir', default='config_files', help='Configuration files directory')
    parser.add_argument('--output-dir', default='output', help='Output directory for reports')
    parser.add_argument('--analyze', action='store_true', help='Run complete network analysis')
    
    args = parser.parse_args()
    
    analyzer = CiscoNetworkAnalyzer()
    
    if args.analyze:
        analyzer.run_complete_analysis(args.config_dir, args.output_dir)
    else:
        console.print("Use --analyze to run complete network analysis")
        console.print("Example: python src/main.py --analyze")

if __name__ == "__main__":
    main()
