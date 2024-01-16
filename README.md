# fuzzy-logic

Este repositorio contiene implementaciones en Python de funciones relacionadas con lógica difusa. La lógica difusa es una técnica que permite manejar la incertidumbre y la imprecisión en sistemas de control y toma de decisiones. El código proporciona funciones para la definición de conjuntos difusos, operaciones difusas y funciones de pertenencia, así como la simulación de sistemas difusos.

## Archivos incluidos

### `fuzzy.py`

Este archivo contiene implementaciones de funciones relacionadas con lógica difusa. Algunas de las funciones incluidas son:

- `singleton(x, x0)`: Función de pertenencia singleton.
- `trimf(x, param)`: Función de pertenencia triangular.
- `trapmf(x, param)`: Función de pertenencia trapezoidal.
- `gaussmf(x, param)`: Función de pertenencia gaussiana.
- `gbellmf(x, param)`: Función de pertenencia campana generalizada.
- `sigmf(x, param)`: Función de pertenencia sigmoidal.
- `cartesian(mA, mB)`: Relación cartesiana difusa.
- `compose(mRA, mRB)`: Composición difusa max-min.
- `Tmin(mA, mB)`: Norma T (mínimo).
- `Smax(mA, mB)`: Norma S (máximo).
- `Nc(mA)`: Complemento.
- `cut(value, mf)`: Cortar.
- `union(data)`: Unión de funciones de membresía por método max.
- `fuzz(x0, y, mA_list, mB_list)`: Fuzzificación.
- `defuzz(y, mf, option)`: Defuzzificación.

### `gui.py`

Este archivo contiene una interfaz gráfica implementada con PyQt5 para la simulación de un sistema de control difuso. La interfaz gráfica permite establecer un punto de ajuste (setpoint) y visualizar gráficos de las funciones de pertenencia asociadas al error y al termostato. También se presenta una simulación en tiempo real del sistema de control difuso.

## Uso

Para utilizar las funciones de lógica difusa, simplemente importe el módulo `fuzzy.py` en su código y utilice las funciones según sea necesario. Para ejecutar la interfaz gráfica, ejecute el archivo `main.py`.

```python
# Ejemplo de uso de funciones de lógica difusa
import fuzzy

# Definir conjuntos difusos y parámetros
e = [0, 1, 2, 3, 4]
param_trimf = [1, 2, 3]

# Calcular función de pertenencia triangular
membership = fuzzy.trimf(e, param_trimf)

# Imprimir resultado
print(membership)

# Ejecutar
python main.py
```
![Ejecución](fuzzy-logic.jpg)
