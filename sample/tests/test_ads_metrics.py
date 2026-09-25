import pytest

from ads_metrics import resumen_campanas, tacos

CAMPANA_A = {"impressions": 5000, "clicks": 100, "cost": 95.0, "sales7d": 190.0, "purchases7d": 10}
CAMPANA_B = {"impressions": 1000, "clicks": 20, "cost": 25.0, "sales7d": 50.0, "purchases7d": 2}


def test_suma_totales_de_varias_campanas():
    r = resumen_campanas([CAMPANA_A, CAMPANA_B])
    assert r["campanas"] == 2
    assert r["gasto"] == 120.0
    assert r["ventas_atribuidas"] == 240.0
    assert r["pedidos"] == 12
    assert r["clics"] == 120


def test_calcula_los_ratios():
    r = resumen_campanas([CAMPANA_A, CAMPANA_B])
    assert r["acos"] == pytest.approx(0.5)
    assert r["roas"] == pytest.approx(2.0)
    assert r["cpc"] == pytest.approx(1.0)
    assert r["ctr"] == pytest.approx(0.02)
    assert r["cvr"] == pytest.approx(0.1)


def test_sin_campanas_no_falla_y_los_ratios_son_none():
    r = resumen_campanas([])
    assert r["gasto"] == 0
    assert r["acos"] is None and r["cpc"] is None and r["cvr"] is None


def test_campana_sin_clics_ni_ventas_no_divide_por_cero():
    r = resumen_campanas([{"impressions": 300, "clicks": 0, "cost": 0.0, "sales7d": 0.0}])
    assert r["acos"] is None
    assert r["cpc"] is None
    assert r["ctr"] == 0.0


def test_tacos_usa_las_ventas_totales():
    assert tacos(120.0, 1200.0) == pytest.approx(0.1)
    assert tacos(120.0, 0) is None
