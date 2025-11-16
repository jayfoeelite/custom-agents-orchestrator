#!/usr/bin/env python3
"""
Merge all agent YAML files into RooCode's custom_modes.yaml
"""

import yaml
import os
from pathlib import Path

def merge_agents():
    # Define paths
    agents_dir = Path('agents')
    output_file = Path('../../../AppData/Roaming/Code/User/globalStorage/rooveterinaryinc.roo-cline/settings/custom_modes.yaml')
    
    # Get all YAML files in agents directory
    agent_files = sorted(agents_dir.glob('*.yaml'))
    
    print(f"Found {len(agent_files)} agent files")
    
    # Collect all agent definitions
    all_agents = []
    
    for agent_file in agent_files:
        print(f"Processing {agent_file.name}...")
        with open(agent_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            if 'customModes' in data and isinstance(data['customModes'], list):
                # Each file should have one agent in the customModes array
                all_agents.extend(data['customModes'])
    
    # Create the merged structure
    merged_data = {
        'customModes': all_agents
    }
    
    # Write to output file
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        yaml.dump(merged_data, f, default_flow_style=False, allow_unicode=True, width=120, sort_keys=False)
    
    print(f"\n✓ Successfully merged {len(all_agents)} agents into {output_file}")
    print(f"  File: {output_file.absolute()}")
    
    return len(all_agents)

if __name__ == '__main__':
    print("="*70)
    print("AI Agent Orchestration System - Agent Merger")
    print("="*70)
    print()
    
    count = merge_agents()
    
    print()
    print("="*70)
    print(f"Merge complete: {count} agents now available in RooCode")
    print("="*70)