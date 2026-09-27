# Amazon Profitability Hub

Calcula cuánto gana **de verdad** cada producto de una marca que vende en Amazon, cruzando ventas, comisiones, logística y publicidad.

> Código privado. Las capturas usan datos ficticios. Muestra del código con tests en [`sample/`](sample/).

![Resumen del panel](./images/resumen.png)

## Qué hace

- Descarga ventas, comisiones, logística y publicidad con las **APIs de Amazon**.
- Calcula el **beneficio real y el margen** de cada producto, con y sin publicidad.
- Indica el **gasto máximo en publicidad** antes de perder dinero (ACOS de equilibrio).
- Avisa de **roturas de stock** y envía un resumen diario.

## Stack

Python · Amazon SP-API y Ads API · OAuth 2.0 · SQL · pytest

**445 tests** · credenciales fuera del código · modo demo separado de los datos reales.

## Mi papel

Todo el desarrollo: integración con las APIs, modelo de datos, cálculos, panel y tests. Desarrollo asistido por IA bajo mi especificación y revisión.

---

[Perfil](https://github.com/miquel-moreno) · [LinkedIn](https://www.linkedin.com/in/miquel-moreno-martinez)