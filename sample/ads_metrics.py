"""Métricas de publicidad agregadas a partir de las campañas de Amazon Ads.

Recibe la lista de campañas tal como la devuelve la API y calcula los totales
y los ratios del periodo. Si falta un dato para calcular un ratio (por ejemplo,
cero clics), devuelve None en lugar de fallar.
"""


def _ratio(numerador: float, denominador: float) -> float | None:
    return round(numerador / denominador, 4) if denominador > 0 else None


def resumen_campanas(campanas: list[dict]) -> dict:
    """Suma gasto, ventas, pedidos, clics e impresiones y calcula ACOS, ROAS, CPC, CTR y CVR."""
    gasto = sum(float(c.get("cost") or 0) for c in campanas)
    ventas = sum(float(c.get("sales7d") or 0) for c in campanas)
    pedidos = sum(int(c.get("purchases7d") or 0) for c in campanas)
    clics = sum(int(c.get("clicks") or 0) for c in campanas)
    impresiones = sum(int(c.get("impressions") or 0) for c in campanas)

    return {
        "campanas": len(campanas),
        "gasto": round(gasto, 2),
        "ventas_atribuidas": round(ventas, 2),
        "pedidos": pedidos,
        "clics": clics,
        "impresiones": impresiones,
        "acos": _ratio(gasto, ventas),       # gasto / ventas atribuidas
        "roas": _ratio(ventas, gasto),       # ventas atribuidas / gasto
        "cpc": _ratio(gasto, clics),         # coste por clic
        "ctr": _ratio(clics, impresiones),   # clics / impresiones
        "cvr": _ratio(pedidos, clics),       # pedidos / clics
    }


def tacos(gasto_publicidad: float, ventas_totales: float) -> float | None:
    """Gasto en publicidad sobre ventas totales (orgánicas + publicidad)."""
    return _ratio(gasto_publicidad, ventas_totales)
