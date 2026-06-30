# Proyecto-Fisica-Electronica-Grupo-7
# Laboratorio Virtual de Transistores BJT NPN de Silicio (2N3904)

Aplicación interactiva en **Python + Streamlit** para simular tres configuraciones
clásicas de polarización de transistores BJT NPN, basada en material académico de
las semanas 7, 8 y 10 (Fundamentos de Electrónica de Transistores).

## Circuitos incluidos

1. **Polarización de Base (Fija)** — Vcc, Rb, Rc.
2. **Polarización de Emisor** — Vcc, Vee, Rb, Rc, Re (dos fuentes).
3. **Polarización por Divisor de Tensión** — Vcc, R1, R2, Rc, Re (método de Thévenin).

Todos los cálculos usan β = 100 fijo y Vbe = 0.7 V (segunda aproximación del
transistor de silicio). El usuario ingresa/ajusta todos los valores mediante
sliders y cajas numéricas; no hay resultados precargados ocultos.

Cada pestaña muestra:
- Diagrama esquemático del circuito (SVG).
- Panel de entrada de datos.
- Métricas calculadas: Ib, Ic, Vce, Ic(sat).
- Gráfica interactiva de la recta de carga DC con el punto Q en tiempo real.
- Diagnóstico automático de fallas: Corte / Saturación / Región Activa.

## Cómo correrlo localmente

```bash
pip install -r requirements.txt
streamlit run app.py
```

Se abrirá automáticamente en tu navegador (por defecto en `http://localhost:8501`).

## Cómo subirlo a GitHub y desplegarlo como página web

1. Crea un repositorio nuevo en GitHub y sube estos archivos:
   ```bash
   git init
   git add app.py requirements.txt README.md
   git commit -m "Laboratorio Virtual BJT 2N3904"
   git branch -M main
   git remote add origin https://github.com/TU_USUARIO/TU_REPO.git
   git push -u origin main
   ```
2. Ve a [share.streamlit.io](https://share.streamlit.io) (Streamlit Community Cloud).
3. Inicia sesión con tu cuenta de GitHub y selecciona "New app".
4. Elige tu repositorio, la rama `main` y el archivo `app.py`.
5. Haz clic en "Deploy". Obtendrás una URL pública tipo `tuapp.streamlit.app`,
   que se actualiza automáticamente cada vez que hagas `git push`.

## Estructura del proyecto

```
bjt-lab/
├── app.py            # Lógica completa de la aplicación (Python)
├── requirements.txt  # Dependencias (streamlit, plotly)
└── README.md
```
