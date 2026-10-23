"""Imprime las salidas de texto de un notebook ejecutado (para revisión)."""
import json, sys
nb = json.load(open(sys.argv[1]))
for i, c in enumerate(nb["cells"]):
    if c["cell_type"] != "code":
        continue
    for o in c.get("outputs", []):
        if o.get("output_type") == "error":
            print(f"[{i}] ERROR", o["ename"], o["evalue"])
        txt = o.get("text") or o.get("data", {}).get("text/markdown") or o.get("data", {}).get("text/plain")
        if txt:
            t = "".join(txt)
            print(f"--- [{i}]\n" + (t[:int(sys.argv[2]) if len(sys.argv) > 2 else 3000]))
        if "image/png" in o.get("data", {}):
            print(f"--- [{i}] <figura>")
