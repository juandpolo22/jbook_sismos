"""Convierte los capítulos fuente (formato «percent»: celdas separadas por ``# %%``) en notebooks
y, opcionalmente, los ejecuta en orden con nbclient.

Uso (desde la raíz del libro):
    python herramientas/construir_notebooks.py            # convierte y ejecuta todos
    python herramientas/construir_notebooks.py 03 04      # solo los capítulos 03 y 04
    python herramientas/construir_notebooks.py --sin-ejecutar
"""
from __future__ import annotations

import re
import sys
import time
from pathlib import Path

import nbformat
from nbclient import NotebookClient

RAIZ = Path(__file__).resolve().parents[1]
FUENTES = RAIZ / "notebooks_src"
DESTINO = RAIZ / "notebooks"


def convertir(ruta: Path) -> nbformat.NotebookNode:
    texto = ruta.read_text(encoding="utf-8")
    cabecera = (FUENTES / "_cabecera.txt").read_text(encoding="utf-8")
    texto = texto.replace("# %% [cabecera]\n", cabecera + "\n")
    bloques = re.split(r"^# %%(.*)$", texto, flags=re.M)
    nb = nbformat.v4.new_notebook()
    nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
    for i in range(1, len(bloques), 2):
        cab, cuerpo = bloques[i], bloques[i + 1].strip("\n")
        if "[markdown]" in cab:
            lineas = [re.sub(r"^# ?", "", l) for l in cuerpo.splitlines()]
            nb.cells.append(nbformat.v4.new_markdown_cell("\n".join(lineas).strip()))
        elif cuerpo.strip():
            celda = nbformat.v4.new_code_cell(cuerpo)
            etiquetas = re.findall(r"tags=\[([^\]]*)\]", cab)
            if etiquetas:
                celda.metadata["tags"] = [t.strip().strip("'\"") for t in etiquetas[0].split(",")]
            nb.cells.append(celda)
    return nb


def main(argv):
    ejecutar = "--sin-ejecutar" not in argv
    filtros = [a for a in argv if not a.startswith("--")]
    DESTINO.mkdir(exist_ok=True)
    for fuente in sorted(FUENTES.glob("*.py")):
        if filtros and not any(fuente.name.startswith(f) for f in filtros):
            continue
        nb = convertir(fuente)
        destino = DESTINO / (fuente.stem + ".ipynb")
        if ejecutar:
            t0 = time.time()
            NotebookClient(nb, timeout=-1, kernel_name="python3",
                           resources={"metadata": {"path": str(DESTINO)}}).execute()
            print(f"{fuente.stem}: ejecutado en {time.time() - t0:.0f} s", flush=True)
        nbformat.write(nb, destino)


if __name__ == "__main__":
    main(sys.argv[1:])
