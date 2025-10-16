# Python Subnet Calculator

A simple CLI tool to compute network details for IPv4/IPv6 CIDR input.
- Inputs a CIDR (e.g., `192.168.10.0/24` or `2001:db8::/64`)
- Outputs: network address, broadcast (v4), first/last usable (v4), total hosts, wildcard mask, and CIDR summary
- Supports bulk mode from a file of prefixes
- Tested with `pytest`

## Quick Start
### 1. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Re-run the `source .venv/bin/activate` command whenever you open a new
terminal session so the virtual environment stays active.

### 2. Install dependencies

Choose one of the following approaches:

* **Editable install (recommended for development)** – installs the
  package along with dependencies *and* exposes the `subnetcalc` console
  shortcut declared in `pyproject.toml`:

  ```bash
  python3 -m pip install --editable .
  ```

* **Requirements file** – installs only third-party dependencies, after
  which you continue running the CLI through `python3 -m subnet_calc`:

  ```bash
  python3 -m pip install -r requirements.txt
  ```

### 3. Run the CLI

```bash
python3 -m subnet_calc --cidr 192.168.1.0/24
python3 -m subnet_calc --file prefixes.txt --summary
```

If you performed the editable install you can now invoke the shortcut
directly:

```bash
subnetcalc --cidr 192.168.1.0/24
subnetcalc --file prefixes.txt --summary
```

### 4. Execute the test suite (optional)

```bash
python3 -m pytest -q
```
