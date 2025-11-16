#!/usr/bin/env python3
"""
AI Agent Orchestration System - Dependency Graph Generator

This script analyzes agent YAML files to extract delegation patterns and
generates visual dependency graphs in multiple formats (DOT, PNG, SVG, Mermaid).

Usage:
    python tools/generate-dependency-graph.py
    python tools/generate-dependency-graph.py --format png
    python tools/generate-dependency-graph.py --format mermaid
    python tools/generate-dependency-graph.py --output docs/agent-graph
"""

import sys
import re
import yaml
import argparse
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict

try:
    import graphviz
    HAS_GRAPHVIZ = True
except ImportError:
    HAS_GRAPHVIZ = False
    print("Warning: graphviz not installed. Only Mermaid output will be available.")
    print("Install with: pip install graphviz")

# Color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

class AgentGraph:
    """Represents the agent dependency graph."""
    
    def __init__(self):
        self.nodes: Dict[str, Dict] = {}  # slug -> {name, role, groups}
        self.edges: List[Tuple[str, str, str]] = []  # (from, to, delegation_type)
        self.categories: Dict[str, List[str]] = defaultdict(list)
        
    def add_agent(self, slug: str, name: str, role: str, groups: List[str]):
        """Add an agent node to the graph."""
        self.nodes[slug] = {
            'name': name,
            'role': role,
            'groups': groups
        }
        
        # Categorize by type
        if 'orchestrator' in slug:
            self.categories['orchestrator'].append(slug)
        elif any(x in slug for x in ['validator', 'auditor', 'guardian']):
            self.categories['validator'].append(slug)
        elif any(x in slug for x in ['coder', 'tester', 'writer', 'architect']):
            self.categories['worker'].append(slug)
        elif 'bmo' in slug or 'ruler' in slug or 'devil' in slug:
            self.categories['quality'].append(slug)
        else:
            self.categories['other'].append(slug)
    
    def add_delegation(self, from_slug: str, to_slug: str, delegation_type: str = "delegates"):
        """Add a delegation edge between agents."""
        self.edges.append((from_slug, to_slug, delegation_type))
    
    def get_node_color(self, slug: str) -> str:
        """Get color for node based on category."""
        if slug in self.categories['orchestrator']:
            return '#4A90E2'  # Blue
        elif slug in self.categories['worker']:
            return '#7ED321'  # Green
        elif slug in self.categories['validator']:
            return '#F5A623'  # Orange
        elif slug in self.categories['quality']:
            return '#BD10E0'  # Purple
        else:
            return '#9B9B9B'  # Gray

def extract_delegations(custom_instructions: str) -> Set[str]:
    """
    Extract agent slugs that are delegated to from customInstructions.
    Looks for patterns like: "delegate to agent-slug" or "new_task to agent-slug"
    """
    delegations = set()
    
    # Pattern 1: "delegate to agent-slug"
    pattern1 = r'delegate[s]?\s+to\s+([a-z0-9]+(?:-[a-z0-9]+)*)'
    matches1 = re.findall(pattern1, custom_instructions, re.IGNORECASE)
    delegations.update(matches1)
    
    # Pattern 2: "new_task to agent-slug" or "task agent-slug"
    pattern2 = r'(?:new_task|task)\s+(?:to\s+)?([a-z0-9]+(?:-[a-z0-9]+)*)'
    matches2 = re.findall(pattern2, custom_instructions, re.IGNORECASE)
    delegations.update(matches2)
    
    # Pattern 3: Direct agent mentions in workflow sequences
    pattern3 = r'\b([a-z]+-[a-z]+(?:-[a-z]+)*)\b'
    potential_agents = re.findall(pattern3, custom_instructions)
    # Filter to only include known agent-like patterns
    agent_keywords = ['orchestrator', 'writer', 'coder', 'tester', 'architect', 
                     'validator', 'auditor', 'guardian', 'planner', 'researcher',
                     'debugger', 'optimizer', 'advocate', 'ruler', 'bmo']
    for agent in potential_agents:
        if any(keyword in agent for keyword in agent_keywords):
            delegations.add(agent)
    
    return delegations

def analyze_agents(agents_dir: Path) -> AgentGraph:
    """Analyze all agent YAML files and build dependency graph."""
    graph = AgentGraph()
    
    yaml_files = sorted(agents_dir.glob('*.yaml'))
    print(f"\n{Colors.BLUE}Analyzing {len(yaml_files)} agent files...{Colors.END}\n")
    
    # First pass: collect all agents
    all_agent_data = {}
    for yaml_file in yaml_files:
        try:
            with open(yaml_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                
            if 'customModes' in data:
                for mode in data['customModes']:
                    slug = mode.get('slug', '')
                    name = mode.get('name', '')
                    role = mode.get('roleDefinition', '')[:100] + '...'
                    groups = mode.get('groups', [])
                    custom_inst = mode.get('customInstructions', '')
                    
                    all_agent_data[slug] = {
                        'name': name,
                        'role': role,
                        'groups': groups,
                        'instructions': custom_inst
                    }
                    
                    graph.add_agent(slug, name, role, groups)
                    
        except Exception as e:
            print(f"{Colors.YELLOW}Warning: Could not parse {yaml_file}: {e}{Colors.END}")
    
    # Second pass: extract delegations
    for slug, data in all_agent_data.items():
        delegations = extract_delegations(data['instructions'])
        
        # Filter to only include actual agents in our system
        valid_delegations = delegations.intersection(all_agent_data.keys())
        
        for target in valid_delegations:
            graph.add_delegation(slug, target)
            
        if valid_delegations:
            print(f"{Colors.GREEN}✓{Colors.END} {slug} → {', '.join(sorted(valid_delegations))}")
    
    return graph

def generate_mermaid(graph: AgentGraph, output_path: Path):
    """Generate Mermaid flowchart syntax."""
    lines = [
        "```mermaid",
        "flowchart TD",
        ""
    ]
    
    # Define nodes with shortened names
    for slug, data in graph.nodes.items():
        # Extract emoji and short name
        name = data['name']
        emoji_match = re.match(r'([^\w\s]+)\s*(.*)', name)
        if emoji_match:
            emoji, short_name = emoji_match.groups()
            label = f"{emoji} {short_name[:30]}"
        else:
            label = name[:35]
        
        # Node style based on category
        node_id = slug.replace('-', '_')
        lines.append(f"    {node_id}[\"{label}\"]")
    
    lines.append("")
    
    # Define edges
    for from_slug, to_slug, delegation_type in graph.edges:
        from_id = from_slug.replace('-', '_')
        to_id = to_slug.replace('-', '_')
        lines.append(f"    {from_id} --> {to_id}")
    
    lines.append("")
    
    # Add styling
    lines.extend([
        "    classDef orchestrator fill:#4A90E2,stroke:#2E5C8A,color:#fff",
        "    classDef worker fill:#7ED321,stroke:#5A9B18,color:#000",
        "    classDef validator fill:#F5A623,stroke:#B87A1A,color:#000",
        "    classDef quality fill:#BD10E0,stroke:#8A0BA8,color:#fff",
        ""
    ])
    
    # Apply classes
    for category, slugs in graph.categories.items():
        if slugs and category != 'other':
            node_ids = ','.join(slug.replace('-', '_') for slug in slugs)
            lines.append(f"    class {node_ids} {category}")
    
    lines.append("```")
    
    # Write to file
    output_path.write_text('\n'.join(lines), encoding='utf-8')
    print(f"\n{Colors.GREEN}✓ Generated Mermaid diagram: {output_path}{Colors.END}")

def generate_graphviz(graph: AgentGraph, output_path: Path, format: str = 'png'):
    """Generate Graphviz DOT format and render to image."""
    if not HAS_GRAPHVIZ:
        print(f"{Colors.RED}✗ Graphviz not installed. Cannot generate {format} output.{Colors.END}")
        return
    
    dot = graphviz.Digraph(comment='AI Agent Dependency Graph')
    dot.attr(rankdir='TB', splines='ortho', nodesep='0.5', ranksep='0.8')
    dot.attr('node', shape='box', style='rounded,filled', fontname='Arial', fontsize='10')
    dot.attr('edge', fontname='Arial', fontsize='8')
    
    # Add nodes
    for slug, data in graph.nodes.items():
        color = graph.get_node_color(slug)
        # Shorten label
        name = data['name']
        emoji_match = re.match(r'([^\w\s]+)\s*(.*)', name)
        if emoji_match:
            emoji, short_name = emoji_match.groups()
            label = f"{emoji}\\n{short_name[:25]}"
        else:
            label = name[:30]
        
        dot.node(slug, label, fillcolor=color, fontcolor='white' if color in ['#4A90E2', '#BD10E0'] else 'black')
    
    # Add edges
    for from_slug, to_slug, delegation_type in graph.edges:
        dot.edge(from_slug, to_slug, label='')
    
    # Render
    try:
        dot.render(str(output_path), format=format, cleanup=True)
        print(f"\n{Colors.GREEN}✓ Generated {format.upper()} diagram: {output_path}.{format}{Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}✗ Failed to render graph: {e}{Colors.END}")

def main():
    parser = argparse.ArgumentParser(
        description='Generate agent dependency graph visualizations'
    )
    parser.add_argument(
        '--format', '-f',
        choices=['dot', 'png', 'svg', 'mermaid', 'all'],
        default='mermaid',
        help='Output format (default: mermaid)'
    )
    parser.add_argument(
        '--output', '-o',
        type=str,
        default='docs/agent-dependency-graph',
        help='Output file path (without extension)'
    )
    
    args = parser.parse_args()
    
    # Paths
    project_root = Path(__file__).parent.parent
    agents_dir = project_root / 'agents'
    output_path = project_root / args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"\n{Colors.BLUE}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}AI Agent Orchestration System - Dependency Graph Generator{Colors.END}")
    print(f"{Colors.BLUE}{'='*70}{Colors.END}")
    
    # Analyze agents
    graph = analyze_agents(agents_dir)
    
    print(f"\n{Colors.BLUE}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}Graph Statistics{Colors.END}")
    print(f"{Colors.BLUE}{'='*70}{Colors.END}\n")
    print(f"Total agents:     {len(graph.nodes)}")
    print(f"Total delegations: {len(graph.edges)}")
    print(f"Orchestrators:    {len(graph.categories['orchestrator'])}")
    print(f"Workers:          {len(graph.categories['worker'])}")
    print(f"Validators:       {len(graph.categories['validator'])}")
    print(f"Quality Agents:   {len(graph.categories['quality'])}")
    
    # Generate output
    formats = [args.format] if args.format != 'all' else ['mermaid', 'png', 'svg']
    
    for fmt in formats:
        if fmt == 'mermaid':
            mermaid_path = output_path.with_suffix('.md')
            generate_mermaid(graph, mermaid_path)
        else:
            generate_graphviz(graph, output_path, fmt)
    
    print(f"\n{Colors.GREEN}✓ Dependency graph generation complete{Colors.END}\n")

if __name__ == '__main__':
    main()