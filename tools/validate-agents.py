#!/usr/bin/env python3
"""
AI Agent Orchestration System - Agent Mode Validator

This script validates all agent YAML files against the defined JSON schema,
ensuring structural integrity and compliance with the agent definition standard.

Usage:
    python tools/validate-agents.py
    python tools/validate-agents.py --verbose
    python tools/validate-agents.py --agent agents/uber-orchestrator.yaml
"""

import sys
import json
import yaml
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Any
from jsonschema import validate, ValidationError, SchemaError

# Color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def load_schema(schema_path: Path) -> Dict:
    """Load and parse the JSON schema."""
    try:
        with open(schema_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"{Colors.RED}✗ Schema file not found: {schema_path}{Colors.END}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"{Colors.RED}✗ Invalid JSON in schema: {e}{Colors.END}")
        sys.exit(1)

def load_yaml_file(yaml_path: Path) -> Dict:
    """Load and parse a YAML agent definition file."""
    try:
        with open(yaml_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"YAML file not found: {yaml_path}")
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML: {e}")

def validate_communication_protocol(agent_data: Dict, agent_file: str) -> List[str]:
    """
    Validate that the agent's customInstructions includes the mandatory
    communication protocol header requirement.
    """
    warnings = []
    
    if 'customModes' not in agent_data:
        return warnings
    
    for mode in agent_data['customModes']:
        custom_instructions = mode.get('customInstructions', '')
        slug = mode.get('slug', 'unknown')
        
        # Check for mandatory routing header mention
        protocol_keywords = [
            'To: [recipient agent\'s slug], From: [your agent\'s slug]',
            'mandatory routing header',
            'communication protocol'
        ]
        
        has_protocol = any(keyword in custom_instructions for keyword in protocol_keywords)
        
        if not has_protocol:
            warnings.append(
                f"  ⚠️  Agent '{slug}' may be missing communication protocol requirement"
            )
    
    return warnings

def validate_signal_framework(agent_data: Dict, agent_file: str) -> List[str]:
    """
    Validate Signal Interpretation Framework presence in orchestrator-state-scribe.
    """
    warnings = []
    
    if 'orchestrator-state-scribe' not in agent_file:
        return warnings
    
    if 'customModes' not in agent_data:
        return warnings
    
    for mode in agent_data['customModes']:
        custom_instructions = mode.get('customInstructions', '')
        
        # Check for Signal Framework components
        framework_components = [
            'Signal Interpretation Framework',
            'signalCategories',
            'signalTypes',
            'interpretationLogic',
            'keywordsToSignalType'
        ]
        
        missing_components = [
            comp for comp in framework_components 
            if comp not in custom_instructions
        ]
        
        if missing_components:
            warnings.append(
                f"  ⚠️  State Scribe may be missing Signal Framework components: {', '.join(missing_components)}"
            )
    
    return warnings

def validate_agent_file(
    yaml_path: Path, 
    schema: Dict, 
    verbose: bool = False
) -> Tuple[bool, List[str], List[str]]:
    """
    Validate a single agent YAML file against the schema.
    
    Returns:
        (is_valid, errors, warnings)
    """
    errors = []
    warnings = []
    
    try:
        # Load YAML
        agent_data = load_yaml_file(yaml_path)
        
        # Schema validation
        try:
            validate(instance=agent_data, schema=schema)
        except ValidationError as e:
            errors.append(f"  ✗ Schema validation failed: {e.message}")
            if verbose:
                errors.append(f"    Path: {' -> '.join(str(p) for p in e.path)}")
            return False, errors, warnings
        except SchemaError as e:
            errors.append(f"  ✗ Schema itself is invalid: {e.message}")
            return False, errors, warnings
        
        # Custom validation: Communication Protocol
        comm_warnings = validate_communication_protocol(agent_data, str(yaml_path))
        warnings.extend(comm_warnings)
        
        # Custom validation: Signal Framework (for state-scribe)
        signal_warnings = validate_signal_framework(agent_data, str(yaml_path))
        warnings.extend(signal_warnings)
        
        # Additional checks
        if 'customModes' in agent_data:
            for mode in agent_data['customModes']:
                # Check for very long single-line customInstructions
                custom_inst = mode.get('customInstructions', '')
                if len(custom_inst) > 1000 and '\n' not in custom_inst:
                    warnings.append(
                        f"  ⚠️  Agent '{mode.get('slug')}' has very long single-line customInstructions (>1000 chars)"
                    )
        
        return True, errors, warnings
        
    except FileNotFoundError as e:
        errors.append(f"  ✗ {e}")
        return False, errors, warnings
    except ValueError as e:
        errors.append(f"  ✗ {e}")
        return False, errors, warnings
    except Exception as e:
        errors.append(f"  ✗ Unexpected error: {e}")
        return False, errors, warnings

def main():
    parser = argparse.ArgumentParser(
        description='Validate AI Agent YAML definitions against schema'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show detailed validation messages'
    )
    parser.add_argument(
        '--agent', '-a',
        type=str,
        help='Validate a specific agent file instead of all agents'
    )
    
    args = parser.parse_args()
    
    # Paths
    project_root = Path(__file__).parent.parent
    schema_path = project_root / 'schemas' / 'agent-mode-schema.json'
    agents_dir = project_root / 'agents'
    
    # Load schema
    print(f"\n{Colors.BLUE}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}AI Agent Orchestration System - Validator{Colors.END}")
    print(f"{Colors.BLUE}{'='*70}{Colors.END}\n")
    
    print(f"Loading schema from: {schema_path}")
    schema = load_schema(schema_path)
    print(f"{Colors.GREEN}✓ Schema loaded successfully{Colors.END}\n")
    
    # Determine which files to validate
    if args.agent:
        agent_files = [Path(args.agent)]
        print(f"Validating single agent: {args.agent}\n")
    else:
        agent_files = sorted(agents_dir.glob('*.yaml'))
        print(f"Validating {len(agent_files)} agent files from: {agents_dir}\n")
    
    # Validate each file
    results = {
        'passed': [],
        'failed': [],
        'warnings': []
    }
    
    for yaml_file in agent_files:
        relative_path = yaml_file.relative_to(project_root)
        print(f"Validating: {relative_path}")
        
        is_valid, errors, warnings = validate_agent_file(yaml_file, schema, args.verbose)
        
        if is_valid:
            print(f"{Colors.GREEN}  ✓ PASS{Colors.END}")
            results['passed'].append(str(relative_path))
            if warnings:
                results['warnings'].append((str(relative_path), warnings))
                for warning in warnings:
                    print(f"{Colors.YELLOW}{warning}{Colors.END}")
        else:
            print(f"{Colors.RED}  ✗ FAIL{Colors.END}")
            results['failed'].append(str(relative_path))
            for error in errors:
                print(f"{Colors.RED}{error}{Colors.END}")
            for warning in warnings:
                print(f"{Colors.YELLOW}{warning}{Colors.END}")
        
        print()  # Blank line between files
    
    # Summary
    print(f"{Colors.BLUE}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}Validation Summary{Colors.END}")
    print(f"{Colors.BLUE}{'='*70}{Colors.END}\n")
    
    total = len(agent_files)
    passed = len(results['passed'])
    failed = len(results['failed'])
    warned = len(results['warnings'])
    
    print(f"Total agents:    {total}")
    print(f"{Colors.GREEN}Passed:          {passed}{Colors.END}")
    if failed > 0:
        print(f"{Colors.RED}Failed:          {failed}{Colors.END}")
    else:
        print(f"Failed:          {failed}")
    
    if warned > 0:
        print(f"{Colors.YELLOW}With warnings:   {warned}{Colors.END}")
    
    # Exit code
    if failed > 0:
        print(f"\n{Colors.RED}✗ Validation FAILED{Colors.END}")
        sys.exit(1)
    elif warned > 0:
        print(f"\n{Colors.YELLOW}⚠ Validation PASSED with warnings{Colors.END}")
        sys.exit(0)
    else:
        print(f"\n{Colors.GREEN}✓ All validations PASSED{Colors.END}")
        sys.exit(0)

if __name__ == '__main__':
    main()