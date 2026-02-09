---
name: chemistry-query
description: Chemistry agent skill for PubChem API queries (compound info/properties, structures/SMILES/images, synthesis routes/references) + RDKit cheminformatics (SMILES to molecule props/logP/TPSA, 2D PNG/SVG viz, Morgan fingerprints). Use for chemistry tasks involving compounds, molecules, structures, PubChem data, RDKit analysis, SMILES processing, synthesis, or molecular descriptors. Triggers on chemistry, compounds, molecules, chemical data/properties, PubChem, RDKit, SMILES, structures, synthesis.
---

# Chemistry Query Agent

## Overview

Full-stack chemistry toolkit: PubChem data retrieval + RDKit molecule processing/visualization/analysis. Outputs JSON for easy parsing; generates images/files as needed.

## Quick Start

**PubChem:** `exec python skills/chemistry-query/scripts/query_pubchem.py --compound \"aspirin\" --type info`

**RDKit:** `exec python skills/chemistry-query/scripts/rdkit_mol.py --smiles \"CCO\" --action props`

Types/actions detailed below.

## Tasks

### PubChem Queries

`scripts/query_pubchem.py --compound &lt;name|CID&gt; --type &lt;info|structure|synthesis&gt; [--format smiles|image (structure only)]`

- **info:** Formula, MW, IUPAC, InChIKey (JSON)
- **structure:** SMILES/InChI/image URL (resolve name→CID internally where needed)
- **synthesis:** References/routes if available (CID required)

See references/api_endpoints.md for endpoints/rates.

### RDKit Molecule Processing

Chain from PubChem SMILES: `scripts/rdkit_mol.py --smiles &lt;SMILES&gt; --action &lt;props|draw|fingerprint&gt; [--output mol.png] [--radius 2]`

- **props:** JSON {mw, logP, TPSA, HBD, HBA, rotb, arom_rings}
- **draw:** 2D PNG/SVG (size 300x300 default)
- **fingerprint:** Morgan bitvector JSON (2048 bits)

Examples:
- Aspirin props: logP 1.31, TPSA 63.6
- Ethanol draw: Generates ethanol.png

## Chaining Example

1. PubChem: `--compound ethanol --type structure --format smiles` → "CCO"
2. RDKit: `--smiles "CCO" --action props` → {"logp": -0.1, ...}
3. `--action draw --output ethanol.png`

## Resources

### scripts/
- `query_pubchem.py`: PubChem API client (requests, JSON/TXT/PNG)
- `rdkit_mol.py`: RDKit ops (Chem/Descriptors/Draw/AllChem, JSON/PNG out)

### references/
- `api_endpoints.md`: PubChem endpoints, params, limits