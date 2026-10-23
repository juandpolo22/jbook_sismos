"""Piloto de costo: tiempo de un ajuste + predicción por modelo y balanceo (tamaño de un pliegue interno)."""
import sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import numpy as np, pandas as pd, tracemalloc
from src import datos, benchmark as bm, config as cfg
ev_, X, info, tr, gp, te = datos.panel_completo()
y = info["y"]; tm = info["tm"]
ext = bm.pliegues_externos(tm[tr])
a, v = ext[0]
ia = tr[a]
inner = bm.pliegues_internos(tm[ia])
fa, fv = ia[inner[-1][0]], ia[inner[-1][1]]
print("filas ajuste interno (mayor):", len(fa), "validación:", len(fv), flush=True)
filas = []
for tarea, modelos, bal in (("reg", bm.MODELOS_REG, ["—"]), ("clf", bm.MODELOS_CLF, bm.BALANCEOS)):
    for mo in modelos:
        for b in bal:
            p = {q[0]: bm._centro(q) for q in bm.ESPACIOS[(tarea, mo)]}
            m = bm.construir(tarea, mo, p, X.columns, b if tarea == "clf" else "sin balanceo")
            yy = y if tarea == "reg" else (y >= 1).astype(int)
            tracemalloc.start(); t0 = time.perf_counter()
            m.fit(X.iloc[fa], yy[fa]); t1 = time.perf_counter()
            s = m.predict(X.iloc[fv]) if tarea == "reg" else bm.puntaje_clf(m, X.iloc[fv]); t2 = time.perf_counter()
            mem = tracemalloc.get_traced_memory()[1] / 1e6; tracemalloc.stop()
            met = bm.metricas_reg(y[fv], s)["RMSLE"] if tarea == "reg" else bm.roc_auc_score(yy[fv], s)
            filas.append({"tarea": tarea, "modelo": mo, "balanceo": b, "t_ajuste_s": t1 - t0, "t_pred_s": t2 - t1, "mem_pico_MB": mem, "metrica": met})
            print(filas[-1], flush=True)
pd.DataFrame(filas).to_csv(cfg.RESULTADOS / "benchmark" / "piloto_costos.csv", index=False)
