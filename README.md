
# Python Subnet Calculator

A simple CLI tool to compute network details for IPv4/IPv6 CIDR input.
- Inputs a CIDR (e.g., `192.168.10.0/24` or `2001:db8::/64`)
- Outputs: network address, broadcast (v4), first/last usable (v4), total hosts, wildcard mask, and CIDR summary
- Supports bulk mode from a file of prefixes
- Tested with `pytest`

## Quick Start
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m subnet_calc --cidr 192.168.1.0/24
python -m subnet_calc --file prefixes.txt --summary
pytest -q
```
