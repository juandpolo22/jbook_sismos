# Pronóstico mensual de sismos por celda en Colombia · Entregable 2

Proyecto de Machine Learning (Universidad del Norte) · Juan David Polo y Gabriella Pallares.

Pronostica el **número de sismos M ≥ 2,5 del mes siguiente en cada celda de 0,5° × 0,5°** de Colombia con el catálogo
del Servicio Geológico Colombiano (2004–2026). El informe es un Jupyter Book: capítulos 1–12 (Entregable 1: datos, EDA,
auditoría de fuga, preprocesamiento y modelo base) y 13–23 (Entregable 2: 140 combinaciones de modelos benchmark con
validación anidada, optimización de hiperparámetros y computacional, evaluación, interpretabilidad con SHAP y LIME,
robustez, comparación estadística y modelo propuesto A+B v2).

## Estructura

```text
notebooks/          capítulos del libro ya ejecutados (.ipynb)
notebooks_src/      fuentes de los capítulos (formato percent) y cabecera común
src/                módulos: config.py (rutas y SEMILLA = 42), datos.py (carga y panel), eda.py, modelos.py,
                    benchmark.py (modelos, balanceo y optimizadores), evaluacion.py, estadistica.py, propuesto.py,
                    arbol_cart.py (CART propio), etas.py, resultados_e2.py
scripts/            experimentos (140 combinaciones, origen móvil, pruebas de independencia, GPU)
resultados/         resultados precalculados; resultados/benchmark/experimentos_maestro.csv es la tabla maestra
tables/, figures/   tablas y figuras que guardan los capítulos
data/               archivos crudos del SGC (data/crudos/) y catálogo limpio
tests/              pruebas unitarias (pytest)
herramientas/       conversión de fuentes a notebooks
requirements.txt    versiones exactas (Python 3.9.25)
```

## Uso

```bash
pip install -r requirements.txt
jupyter-book build .                              # compila el libro con los notebooks ya ejecutados → _build/html/index.html
python -m pytest tests                            # pruebas unitarias
python herramientas/construir_notebooks.py        # vuelve a ejecutar todos los capítulos desde notebooks_src/
python scripts/correr_experimentos.py --tarea reg              # 28 combinaciones de regresión
python scripts/correr_experimentos.py --tarea clf --fase todo  # clasificación (tamizaje + validación anidada)
python scripts/correr_experimentos.py --tabla                  # recompila la tabla maestra
```

Semilla global única: `SEMILLA = 42` en `src/config.py`, propagada a numpy, random, scikit-learn, XGBoost, SMOTE/ADASYN,
Optuna y DEAP.

## Datos

Catálogo sísmico de la Red Sismológica Nacional de Colombia, Servicio Geológico Colombiano
(<https://www.sgc.gov.co/sismos>). Uso académico, con atribución.
