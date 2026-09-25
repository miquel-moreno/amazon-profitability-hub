# Muestra de código

Extracto adaptado del proyecto privado: el cálculo de rentabilidad y las métricas de publicidad. Son funciones puras, sin acceso a APIs ni a datos reales. Los tests usan cifras ficticias.

| Archivo | Qué hace |
|---|---|
| `profitability.py` | Beneficio real por unidad, margen con y sin publicidad, y ACOS de equilibrio |
| `ads_metrics.py` | Totales y ratios de las campañas (ACOS, ROAS, CPC, CTR, CVR) y TACOS |
| `tests/` | 13 tests con pytest |

```bash
pip install pytest
pytest
```
