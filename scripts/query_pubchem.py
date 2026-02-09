import argparse
import requests
import json
import sys

def main():
    parser = argparse.ArgumentParser(description="Query PubChem API")
    parser.add_argument("--compound", required=True, help="Compound name or CID")
    parser.add_argument("--type", required=True, choices=["info", "structure", "synthesis", "similar"], help="Query type")
    parser.add_argument("--format", default="json", choices=["json", "smiles", "inchi", "image"], help="For structure")
    parser.add_argument("--threshold", type=int, default=80, help="Similarity threshold (0-100, similar only)")
    args = parser.parse_args()

    base_url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"
    
    orig_compound = args.compound
    is_cid = args.compound.isdigit()
    identifier = "cid" if is_cid else "name"
    
    # Resolve CID for structure/synthesis/similar if name
    cid_resolve_types = ["structure", "synthesis", "similar"]
    cid = None
    if not is_cid and args.type in cid_resolve_types:
        cid_url = f"{base_url}/compound/name/{orig_compound}/cids/JSON"
        resp = requests.get(cid_url)
        if resp.status_code != 200:
            print(json.dumps({"error": "CID resolution failed", "status": resp.status_code}))
            sys.exit(1)
        cid_data = resp.json().get("IdentifierList", {}).get("CID", [])
        if not cid_data:
            print(json.dumps({"error": "Compound not found"}))
            sys.exit(1)
        cid = cid_data[0]
        args.compound = str(cid)
        identifier = "cid"

    if args.type == "info":
        url = f"{base_url}/compound/{identifier}/{args.compound}/property/MolecularFormula,MolecularWeight,IUPACName,InChIKey/JSON"
    elif args.type == "structure":
        fmt = args.format.lower()
        if fmt == "smiles":
            url = f"{base_url}/compound/{identifier}/{args.compound}/canonicalsmiles/TXT"
        elif fmt == "inchi":
            url = f"{base_url}/compound/{identifier}/{args.compound}/inchi/TXT"
        elif fmt == "image":
            url = f"{base_url}/compound/{identifier}/{args.compound}/PNG?image_size=large"
            print(json.dumps({"image_url": url}))
            sys.exit(0)
        else:
            url = f"{base_url}/compound/{identifier}/{args.compound}/JSON"
    elif args.type == "synthesis":
        url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/{args.compound}/JSON?heading=Synthesis"
    elif args.type == "similar":
        # Get canonical SMILES for query
        smiles_url = f"{base_url}/compound/{identifier}/{args.compound}/canonicalsmiles/TXT"
        resp = requests.get(smiles_url)
        if resp.status_code != 200:
            print(json.dumps({"error": "SMILES fetch failed", "status": resp.status_code}))
            sys.exit(1)
        query_smiles = resp.text.strip()
        url = f"{base_url}/compound/similarity_2d/smiles/JSON"
        resp = requests.post(url, data=query_smiles, params={"Threshold": args.threshold}, headers={"Content-Type": "text/plain"})
        if resp.status_code != 200:
            print(json.dumps({"error": resp.text, "status": resp.status_code}))
            sys.exit(1)
        data = resp.json()
        # Flatten smiles list
        similar_smiles = []
        info_list = data.get("InformationList", {}).get("Information", [])
        for info in info_list:
            smiles_list = info.get("Smiles", [])
            similar_smiles.extend(smiles_list)
        print(json.dumps({"query_smiles": query_smiles, "threshold": args.threshold, "similar_smiles": similar_smiles[:20]}))  # Top 20
        sys.exit(0)

    resp = requests.get(url)
    if resp.status_code == 200:
        if "smiles" in url or "inchi" in url:
            print(json.dumps({"result": resp.text.strip()}))
        else:
            print(json.dumps(resp.json()))
    else:
        print(json.dumps({"error": resp.text, "status": resp.status_code}))

if __name__ == "__main__":
    main()