#!/usr/bin/env python3
# src/simulator.py - Network Simulator for Day-1 scenarios

import threading
import time
import json
import queue
import random
from datetime import datetime
import os

class NetworkDevice(threading.Thread):
    def __init__(self, device_id, device_type, config):
        super().__init__()
        self.device_id = device_id
        self.device_type = device_type
        self.config = config
        self.running = False
        self.logs = []
        
    def log_event(self, event_type, description):
        timestamp = datetime.now().strftime('%H:%M:%S')
        log_entry = f"[{timestamp}] {self.device_id}: {description}"
        self.logs.append(log_entry)
        print(log_entry)
        
    def start_simulation(self):
        self.running = True
        self.start()
        
    def run(self):
        # Simulate device boot
        self.log_event("BOOT", "Device starting up")
        time.sleep(random.uniform(1, 3))
        
        if self.device_type == 'router':
            self.simulate_router_startup()
        elif self.device_type == 'switch':
            self.simulate_switch_startup()
        elif self.device_type == 'endpoint':
            self.simulate_endpoint_startup()
            
        # Main operation loop
        while self.running:
            self.periodic_tasks()
            time.sleep(2)
            
    def simulate_router_startup(self):
        self.log_event("OSPF", "OSPF process starting")
        time.sleep(1)
        self.log_event("INTERFACE", "Interfaces coming up")
        
    def simulate_switch_startup(self):
        self.log_event("STP", "Spanning Tree Protocol enabled")
        time.sleep(1)
        self.log_event("VLAN", "VLAN configuration loaded")
        
    def simulate_endpoint_startup(self):
        self.log_event("DHCP", "Requesting IP address")
        time.sleep(1)
        self.log_event("ARP", "Learning gateway MAC address")
        
    def periodic_tasks(self):
        if random.random() < 0.1:  # 10% chance
            self.log_event("HEARTBEAT", "Device operational")
    
    def stop_simulation(self):
        self.running = False

class NetworkSimulator:
    def __init__(self):
        self.devices = {}
        
    def load_topology(self, topology_file):
        with open(topology_file, 'r') as f:
            topology_data = json.load(f)
            
        for device_id, config in topology_data['devices'].items():
            device_type = config['device_type']
            device = NetworkDevice(device_id, device_type, config)
            self.devices[device_id] = device
            
        print(f"✅ Loaded {len(self.devices)} devices for simulation")
        
    def run_day1_simulation(self, duration_seconds=30):
        print("🚀 Starting Day-1 Network Simulation")
        print("=" * 50)
        
        # Start all devices
        for device in self.devices.values():
            device.start_simulation()
        
        print(f"⏱️  Running simulation for {duration_seconds} seconds...")
        time.sleep(duration_seconds)
        
        # Stop simulation
        for device in self.devices.values():
            device.stop_simulation()
            
        # Wait for threads to complete
        for device in self.devices.values():
            device.join(timeout=2)
            
        self.generate_simulation_report()
        print("✅ Day-1 simulation completed!")
        
    def generate_simulation_report(self):
        report = {
            'timestamp': datetime.now().isoformat(),
            'devices_simulated': len(self.devices),
            'simulation_logs': {}
        }
        
        for device_id, device in self.devices.items():
            report['simulation_logs'][device_id] = device.logs
            
        os.makedirs('output', exist_ok=True)
        with open('output/day1_simulation.json', 'w') as f:
            json.dump(report, f, indent=2)
            
        print("📊 Simulation report saved to output/day1_simulation.json")

if __name__ == "__main__":
    try:
        simulator = NetworkSimulator()
        simulator.load_topology('output/network_topology.json')
        simulator.run_day1_simulation(20)
    except FileNotFoundError:
        print("❌ Run main analysis first: python src/main.py --analyze")
    except Exception as e:
        print(f"❌ Simulation error: {e}")
