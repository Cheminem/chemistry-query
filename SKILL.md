---
name: chemistry-query
description: Chemistry agent skill for PubChem API queries (compound info/properties, structures/SMILES/images, synthesis routes/references) + RDKit cheminformatics (SMILES to molecule props/logP/TPSA, 2D PNG/SVG viz, Morgan fingerprints, retrosynthesis/BRICS disconnects, multi-step synth planning). Use for chemistry tasks involving compounds, molecules, structures, PubChem data, RDKit analysis, SMILES processing, synthesis routes, retrosynthesis, reaction simulation. Triggers on chemistry, compounds, molecules, chemical data/properties, PubChem, RDKit, SMILES, structures, synthesis, reactions, retrosynthesis, synth plan/route.
---

# Chemistry Query Agent

## Overview

Full-stack chemistry toolkit: PubChem data retrieval + RDKit molecule processing/visualization/analysis/retrosynthesis/planning. Outputs JSON for easy parsing; generates images/files as needed. New: BRICS retrosynthesis + 20+ reaction templates lib (v1.2).

## Quick Start

**PubChem:** `exec python skills/chemistry-query/scripts/query_pubchem.py --compound \"aspirin\" --type info`

**RDKit Props:** `exec python skills/chemistry-query/scripts/rdkit_mol.py --target \"aspirin\" --action props`

**Retro:** `--action retro --target ethanol --depth 2`

**Plan:** `--action plan --target ibuprofen --steps 3`

**React:** `--action react --reactants \"c1ccccc1Br c1ccccc1B(O)O\" --smarts \"[c:1][Br:2].[c:3][B]([c:4])(O)O>>[c:1][c:3]\"`

## Tasks

### PubChem Queries

`scripts/query_pubchem.py --compound &lt;name|CID&gt; --type &lt;info|structure|synthesis|similar&gt; [--format smiles|image]`

- **info:** Formula, MW, IUPAC, InChIKey (JSON)
- **structure:** SMILES/InChI/image URL (name→CID auto)
- **synthesis:** References/routes (CID)
- **similar:** Similar compounds SMILES (threshold 80%)

### RDKit Molecule Processing

`scripts/rdkit_mol.py --target &lt;SMILES/name&gt; --action &lt;props|draw|fingerprint|similarity|substruct|xyz|react|retro|plan&gt; [--output mol.png] [--depth 2] [--steps 3]`

- **props:** JSON {mw, logP, TPSA, HBD, HBA, rotb, arom_rings}
- **draw:** 2D PNG/SVG (300x300)
- **retro:** BRICS recursive precursors [{"target":"CC(=O)O...", "precursors":["CCO","OC(=O)c1..."]}]
- **plan:** Multi-step retro JSON [{"step":1, "precursors":[], "cond":"BRICS", "product":""}]
- **react:** Forward rxn products from reactants + SMARTS
- **fingerprint:** Morgan BV JSON

**Templates:** scripts/templates.json (21 rxns: Suzuki/Heck/Grignard/Wittig/DA/... w/ yields/conds/refs). Used in future plan/--templates suzuki.

Examples:
- Aspirin: logP 1.31, TPSA 63.6
- Ethanol retro: BRICS fragments (simple molecules often unchanged)
- Biphenyl Suzuki: react PhBr + PhB(OH)2 → Ph-Ph
- Ibuprofen plan: 3-step BRICS retro route

## Chaining Examples

1. **Name → SMILES → Props:** PubChem structure → rdkit props
2. **Retro + Viz:** `--target aspirin --action retro` → `--smiles prec1 --action draw --output prec1.png`
3. **Suzuki Test:** `--reactants \"c1ccccc1Br c1ccccc1B(O)O\" --action react --smarts suzuki`
4. **Full Synth Route:** plan ibuprofen → props/draw each precursor → lit search PubMed

## Resources

### scripts/
- `query_pubchem.py`: PubChem API (requests)
- `rdkit_mol.py`: RDKit (props/draw/fp/retro/plan/react)
- `templates.json`: 21 rxn templates (Suzuki etc, yields/conds)
- `rdkit_reaction.py`: Legacy rxn (forward/retro placeholder)

### references/
- `api_endpoints.md`: PubChem endpoints/limits

Version 1.2.0: Retrosynthesis (BRICS) + templates lib. Multi-step planning. Stereo/yields TBD.