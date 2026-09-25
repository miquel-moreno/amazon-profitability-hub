import pytest

from profitability import CostesProducto, calcular_rentabilidad, publicidad_por_unidad

# Producto de ejemplo con datos ficticios.
PRODUCTO = CostesProducto(
    pvp=24.20,               # 20,00 € sin IVA
    iva=0.21,
    coste_producto=5.00,
    envio_a_almacen=0.50,
    comisiones_amazon=6.00,
    almacenamiento=0.30,
    tasa_devolucion=0.05,
    coste_por_devolucion=4.00,  # 0,20 € por unidad vendida
)


def test_sin_publicidad_el_beneficio_es_ingreso_menos_costes():
    r = calcular_rentabilidad(PRODUCTO)
    assert r.ingreso_neto == pytest.approx(20.00)
    assert r.coste_total == pytest.approx(12.00)
    assert r.beneficio == pytest.approx(8.00)
    assert r.margen == pytest.approx(0.40)


def test_la_publicidad_resta_del_beneficio_pero_no_del_margen_sin_publicidad():
    r = calcular_rentabilidad(PRODUCTO, publicidad_ud=3.00)
    assert r.beneficio == pytest.approx(5.00)
    assert r.margen == pytest.approx(0.25)
    assert r.margen_sin_publicidad == pytest.approx(0.40)


def test_acos_de_equilibrio_es_beneficio_sin_publicidad_sobre_pvp():
    r = calcular_rentabilidad(PRODUCTO)
    assert r.acos_equilibrio == pytest.approx(8.00 / 24.20, abs=1e-4)


def test_producto_con_publicidad_excesiva_pierde_dinero():
    r = calcular_rentabilidad(PRODUCTO, publicidad_ud=9.00)
    assert r.beneficio == pytest.approx(-1.00)
    assert not r.es_rentable


def test_acos_de_equilibrio_nunca_es_negativo():
    caro = CostesProducto(12.10, 0.21, 9.0, 0.5, 4.0, 0.3, 0.0, 0.0)
    assert calcular_rentabilidad(caro).acos_equilibrio == 0


def test_publicidad_por_unidad_reparte_el_gasto():
    assert publicidad_por_unidad(120.0, 40) == pytest.approx(3.0)


def test_publicidad_por_unidad_sin_ventas_es_cero():
    assert publicidad_por_unidad(50.0, 0) == 0.0


def test_pvp_cero_es_un_error():
    with pytest.raises(ValueError):
        calcular_rentabilidad(CostesProducto(0, 0.21, 1, 0, 0, 0, 0, 0))
