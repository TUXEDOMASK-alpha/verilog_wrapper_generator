# Verilog Wrapper Generator

A Python tool that automatically generates Verilog wrapper files by instantiating modules and connecting their ports.

## Features

- Parses Verilog files to extract module definitions and port information
- Creates top-level wrapper modules with specified instances
- Handles port mapping between instances and top-level ports
- Supports input, output, and inout ports with arbitrary widths
- Generates internal wires for unmapped ports
- Command-line interface for easy usage

## Usage

```bash
python verilog_wrapper_generator.py config.json [-o output.v]
```

## Configuration Format

The tool uses a JSON configuration file to specify:

```json
{
  "top_module": "system_top",
  "instances": [
    {
      "file": "path/to/module.v",
      "instance_name": "inst_name",
      "port_mapping": {
        "module_port": "top_port_name"
      }
    }
  ]
}
```

### Configuration Fields

- `top_module`: Name of the generated wrapper module
- `instances`: Array of module instances to create
  - `file`: Path to the Verilog file containing the module
  - `instance_name`: Name for the instance in the wrapper
  - `port_mapping`: Maps module ports to top-level ports

## Example

Run with the provided example:

```bash
python verilog_wrapper_generator.py example_config.json -o system_top.v
```

This will generate a wrapper that instantiates CPU and memory modules with appropriate port connections.

## Generated Output

The tool generates a complete Verilog wrapper with:
- Module declaration with top-level ports
- Internal wire declarations for unmapped ports
- Instance declarations with port connections
- Proper Verilog syntax and formatting