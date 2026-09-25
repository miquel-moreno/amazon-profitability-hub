"""Beneficio real por unidad de un producto vendido en Amazon FBA.

Amazon informa de ventas, comisiones y publicidad por separado. Este módulo
junta todos los costes de una unidad y responde a dos preguntas:

- ¿Cuánto gano de verdad por cada unidad vendida?
- ¿Cuánto puedo gastar en publicidad antes de perder dinero? (ACOS de equilibrio)

Funciones puras: no leen ficheros, ni base de datos, ni APIs.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class CostesProducto:
    """Costes de una unidad, en euros. El PVP incluye IVA."""

    pvp: float
    iva: float                   # 0.21 = 21 %
    coste_producto: float
    envio_a_almacen: float       # envío hasta el almacén de Amazon
    comisiones_amazon: float     # comisión por venta + gestión logística FBA
    almacenamiento: float
    tasa_devolucion: float       # 0.03 = 3 % de las unidades se devuelven
    coste_por_devolucion: float


@dataclass(frozen=True)
class Rentabilidad:
    ingreso_neto: float          # PVP sin IVA: lo que realmente se cobra
    coste_total: float
    beneficio: float
    margen: float                # sobre el ingreso neto
    margen_sin_publicidad: float
    acos_equilibrio: float       # gasto en publicidad / ventas a partir del cual se pierde dinero

    @property
    def es_rentable(self) -> bool:
        return self.beneficio > 0


def publicidad_por_unidad(gasto_publicidad: float, unidades_vendidas: int) -> float:
    """Reparte el gasto en publicidad del periodo entre todas las unidades vendidas."""
    if unidades_vendidas <= 0:
        return 0.0
    return gasto_publicidad / unidades_vendidas


def calcular_rentabilidad(c: CostesProducto, publicidad_ud: float = 0.0) -> Rentabilidad:
    """Calcula el beneficio real de una unidad con y sin publicidad."""
    if c.pvp <= 0:
        raise ValueError("El PVP debe ser mayor que cero")

    ingreso_neto = c.pvp / (1 + c.iva)
    devoluciones = c.tasa_devolucion * c.coste_por_devolucion

    coste_sin_publicidad = (
        c.coste_producto
        + c.envio_a_almacen
        + c.comisiones_amazon
        + c.almacenamiento
        + devoluciones
    )
    beneficio_sin_publicidad = ingreso_neto - coste_sin_publicidad
    beneficio = beneficio_sin_publicidad - publicidad_ud

    return Rentabilidad(
        ingreso_neto=round(ingreso_neto, 4),
        coste_total=round(coste_sin_publicidad + publicidad_ud, 4),
        beneficio=round(beneficio, 4),
        margen=round(beneficio / ingreso_neto, 4),
        margen_sin_publicidad=round(beneficio_sin_publicidad / ingreso_neto, 4),
        # Amazon calcula el ACOS sobre el precio de venta, con IVA incluido.
        acos_equilibrio=round(max(beneficio_sin_publicidad, 0) / c.pvp, 4),
    )
