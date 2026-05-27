"""
WeskerMethod - Terminal de Optimizacion Clasificada
Corporacion Umbrella - Division de Investigacion Analitica
"""

import streamlit as st
import numpy as np
import sympy as sp
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots


# =============================================================================
# CONFIGURACION DE PAGINA Y TEMA
# =============================================================================

st.set_page_config(
    page_title="WeskerMethod",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
/* Fondo negro puro de bunker subterraneo */
.stApp {
    background-color: #000000;
    color: #b8b8b8;
}

/* Container principal con tono ligeramente distinto del fondo */
.main .block-container {
    background-color: #000000;
    padding-top: 2rem;
}

/* Tipografia tecnica y opresiva */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Courier New', 'Consolas', monospace !important;
    color: #d4d4d4 !important;
    letter-spacing: 2px;
    text-transform: uppercase;
}

h1 {
    color: #f0f0f0 !important;
    border-bottom: 2px solid #4a0000;
    padding-bottom: 12px;
    font-weight: bold;
    text-shadow: 0px 0px 4px rgba(139, 0, 0, 0.4);
}

h3 {
    color: #8b0000 !important;
    border-left: 3px solid #4a0000;
    padding-left: 10px;
    font-size: 1.1rem;
}

/* Texto general en gris apagado */
p, span, label, div {
    font-family: 'Courier New', 'Consolas', monospace;
    color: #a0a0a0;
}

/* Inputs con fondo casi negro */
.stTextInput input,
.stNumberInput input,
.stTextArea textarea,
.stSelectbox > div > div {
    background-color: #0a0a0a !important;
    color: #d4d4d4 !important;
    border: 1px solid #2a0000 !important;
    border-radius: 0px !important;
    font-family: 'Courier New', monospace !important;
}

.stTextInput input:focus,
.stNumberInput input:focus,
.stTextArea textarea:focus {
    border: 1px solid #8b0000 !important;
    box-shadow: 0px 0px 5px rgba(139, 0, 0, 0.5) !important;
}

/* Labels de los inputs */
.stTextInput label,
.stNumberInput label,
.stTextArea label,
.stSelectbox label {
    color: #8b0000 !important;
    font-family: 'Courier New', monospace !important;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-size: 0.8rem;
}

/* Boton de ejecucion en rojo sangre muy oscuro */
.stButton > button {
    background-color: #4a0000;
    color: #f0f0f0;
    border: 1px solid #6b0000;
    border-radius: 0px;
    font-family: 'Courier New', monospace;
    text-transform: uppercase;
    letter-spacing: 4px;
    font-weight: bold;
    width: 100%;
    padding: 12px;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    background-color: #6b0000;
    border: 1px solid #8b0000;
    box-shadow: 0px 0px 12px rgba(139, 0, 0, 0.7);
    color: #ffffff;
    text-shadow: 0px 0px 3px rgba(255, 0, 0, 0.6);
}

/* Tarjetas de metricas - estilo terminal clasificada */
[data-testid="stMetric"] {
    background-color: #080808;
    border: 1px solid #2a0000;
    border-left: 4px solid #6b0000;
    padding: 18px;
    border-radius: 0px;
    box-shadow: inset 0px 0px 20px rgba(0, 0, 0, 0.8);
}

[data-testid="stMetricLabel"] {
    color: #8b0000 !important;
    font-family: 'Courier New', monospace !important;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-size: 0.7rem !important;
}

[data-testid="stMetricValue"] {
    color: #e0e0e0 !important;
    font-family: 'Courier New', monospace !important;
}

/* Alertas en rojo sangre oscuro */
.stAlert {
    background-color: #1a0000;
    border: 1px solid #4a0000;
    border-left: 4px solid #8b0000;
    border-radius: 0px;
    color: #d4a0a0;
    font-family: 'Courier New', monospace;
}

/* Info boxes */
div[data-baseweb="notification"] {
    background-color: #0a0a0a;
    border-left: 4px solid #4a0000;
    color: #a0a0a0;
}

/* Divisores - linea de rojo sangre */
hr {
    border-color: #2a0000 !important;
    background-color: #2a0000 !important;
    margin: 25px 0px;
}

/* LaTeX en blanco hueso */
.katex {
    color: #d4d4d4 !important;
}

/* Footer */
.wesker-footer {
    text-align: center;
    color: #4a4a4a;
    font-family: 'Courier New', monospace;
    font-size: 0.75rem;
    letter-spacing: 2px;
    padding: 25px;
    border-top: 1px solid #2a0000;
    margin-top: 50px;
    text-transform: uppercase;
}

/* Lore visible - logs de terminal clasificada, estilo monitor antiguo */
.wesker-lore {
    color: #5a1a1a;
    font-family: 'Courier New', monospace;
    font-size: 0.72rem;
    letter-spacing: 1px;
    text-transform: uppercase;
    border-left: 2px solid #2a0000;
    padding: 6px 14px;
    margin: 8px 0px;
    background-color: #050505;
    font-style: italic;
    opacity: 0.75;
}

.wesker-lore-centered {
    color: #5a1a1a;
    font-family: 'Courier New', monospace;
    font-size: 0.7rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    text-align: center;
    margin: 4px 0px 12px 0px;
    opacity: 0.6;
}

/* Scrollbar oscuro */
::-webkit-scrollbar {
    width: 10px;
    background-color: #000000;
}
::-webkit-scrollbar-thumb {
    background-color: #2a0000;
    border: 1px solid #4a0000;
}
::-webkit-scrollbar-thumb:hover {
    background-color: #4a0000;
}

/* Ocultar el menu hamburguesa para look mas limpio */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# =============================================================================
# NUCLEO MATEMATICO: PARSEO Y EVALUACION
# =============================================================================

def parse_function(func_str, n_vars_declared):
    """
    Parsea la funcion del usuario. Retorna (expr, variables, grad_expr, hess_expr).
    Maneja correctamente el caso 1D vs ND.
    """
    # Reemplazo de operador potencia humano a python
    func_str_clean = func_str.replace('^', '**')

    # Parseo a sympy
    expr = sp.sympify(func_str_clean)

    # Extraccion ordenada alfabeticamente de variables
    variables = sorted(list(expr.free_symbols), key=lambda s: s.name)

    if len(variables) == 0:
        raise ValueError("La funcion no contiene variables.")

    if len(variables) != n_vars_declared:
        raise ValueError(
            f"Inconsistencia dimensional: declaradas {n_vars_declared} variables, "
            f"detectadas {len(variables)} ({[str(v) for v in variables]})."
        )

    # Gradiente: lista de derivadas parciales
    grad_expr = [sp.diff(expr, v) for v in variables]

    # Hessiana: matriz de segundas derivadas
    # Para 1 variable es escalar (1x1), para N es NxN
    n = len(variables)
    hess_expr = sp.Matrix(n, n, lambda i, j: sp.diff(expr, variables[i], variables[j]))

    return expr, variables, grad_expr, hess_expr


def make_numeric_evaluators(expr, variables, grad_expr, hess_expr):
    """
    Genera funciones numericas vectorizadas con lambdify.
    Devuelve f(x), grad(x), hess(x) donde x es np.array de shape (n,).
    """
    # lambdify acepta tupla de variables
    f_lamb = sp.lambdify(variables, expr, modules='numpy')
    grad_lamb = [sp.lambdify(variables, g, modules='numpy') for g in grad_expr]
    hess_lamb = sp.lambdify(variables, hess_expr, modules='numpy')

    def f(x):
        # x es np.array de shape (n,)
        x = np.atleast_1d(np.asarray(x, dtype=float))
        val = f_lamb(*x)
        return float(val)

    def grad(x):
        x = np.atleast_1d(np.asarray(x, dtype=float))
        g = np.array([gi(*x) for gi in grad_lamb], dtype=float)
        return g  # shape (n,)

    def hess(x):
        x = np.atleast_1d(np.asarray(x, dtype=float))
        H = np.array(hess_lamb(*x), dtype=float)
        # Garantizar forma matricial
        if H.ndim == 0:
            H = H.reshape(1, 1)
        elif H.ndim == 1:
            H = H.reshape(len(variables), len(variables))
        return H

    return f, grad, hess


# =============================================================================
# BUSQUEDA DE LINEA: BACKTRACKING CON CONDICION DE ARMIJO
# =============================================================================

def backtracking_line_search(f, grad, x, d, c1=1e-4, c2=0.9, rho=0.5,
                             alpha_init=1.0, max_backtrack=50):
    """
    Busqueda de linea por backtracking con rastreo completo de cada intento.

    Detencion: cuando se cumple la Condicion de Armijo (LHS <= RHS).
    Adicionalmente, en cada intento se evalua (sin influir en la detencion)
    la Condicion 2 fuerte de Wolfe (curvatura).

        Armijo (C1):       f(x + alpha*d) <= f(x) + c1 * alpha * grad(x).T @ d
        Wolfe 2 (C2):      |grad(x + alpha*d).T @ d| <= c2 * |grad(x).T @ d|

    Si Armijo no se cumple, se reduce el paso: alpha = rho * alpha.

    Retorna (alpha_final, tracking_list) donde tracking_list es una lista de
    diccionarios, uno por intento, con todas las metricas pedidas para auditoria.
    """
    phi_0 = float(f(x))
    grad_0 = grad(x)
    dphi_0 = float(np.dot(grad_0, d))
    abs_dphi_0 = abs(dphi_0)

    tracking = []

    # Si d no es direccion de descenso, registramos un intento unico y salimos
    if dphi_0 >= 0:
        alpha_safe = float(min(alpha_init, 1.0))
        x_new = x + alpha_safe * d
        lhs = float(f(x_new))
        rhs = phi_0 + c1 * alpha_safe * dphi_0
        grad_new = grad(x_new)
        dphi_new = float(np.dot(grad_new, d))
        tracking.append({
            'iter_bt': 1,
            'alpha': alpha_safe,
            'x_new': np.asarray(x_new, dtype=float).copy(),
            'lhs_armijo': lhs,
            'rhs_armijo': rhs,
            'cumple_armijo': lhs <= rhs,
            'cumple_wolfe2': abs(dphi_new) <= c2 * abs_dphi_0,
        })
        return alpha_safe, tracking

    alpha = float(alpha_init)

    for i in range(1, max_backtrack + 1):
        x_new = x + alpha * d
        lhs = float(f(x_new))
        rhs = phi_0 + c1 * alpha * dphi_0
        cumple_armijo = lhs <= rhs

        # Wolfe 2 (curvatura fuerte): solo informativo, no detiene el bucle
        grad_new = grad(x_new)
        dphi_new = float(np.dot(grad_new, d))
        cumple_wolfe2 = abs(dphi_new) <= c2 * abs_dphi_0

        tracking.append({
            'iter_bt': i,
            'alpha': alpha,
            'x_new': np.asarray(x_new, dtype=float).copy(),
            'lhs_armijo': lhs,
            'rhs_armijo': rhs,
            'cumple_armijo': bool(cumple_armijo),
            'cumple_wolfe2': bool(cumple_wolfe2),
        })

        # Detencion: Armijo cumplido
        if cumple_armijo:
            return alpha, tracking

        # Reduccion del paso
        alpha = rho * alpha

    # Se agotaron los intentos sin cumplir Armijo: devolver el ultimo alpha
    return alpha, tracking


# =============================================================================
# ALGORITMOS DE OPTIMIZACION
# =============================================================================

def _init_history(x0, f_val, g_norm):
    """
    Estructura uniforme de telemetria. El indice k corresponde a la iteracion
    global: k=0 es el punto inicial (sin paso aun, alpha=NaN, sin tracking).
    """
    return {
        'x': [np.array(x0, dtype=float).copy()],
        'f': [float(f_val)],
        'grad_norm': [float(g_norm)],
        'alpha': [float('nan')],
        'n_backtrack': [-1],
        'bt_tracking': [[]],  # lista de intentos de backtracking por iter global
    }


def gradient_descent(f, grad, x0, max_iter, tol, c1, c2, rho):
    """Metodo del descenso por gradiente con backtracking Armijo."""
    x = np.array(x0, dtype=float).flatten()
    g = grad(x)
    g_norm = float(np.linalg.norm(g))
    history = _init_history(x, f(x), g_norm)
    stop_reason = "Iteraciones agotadas"

    for k in range(max_iter):
        if g_norm < tol:
            stop_reason = f"Convergencia alcanzada (||grad|| < {tol})"
            break

        d = -g
        alpha, tracking = backtracking_line_search(f, grad, x, d, c1=c1, c2=c2, rho=rho)
        x = x + alpha * d
        g = grad(x)
        g_norm = float(np.linalg.norm(g))

        history['x'].append(x.copy())
        history['f'].append(float(f(x)))
        history['grad_norm'].append(g_norm)
        history['alpha'].append(float(alpha))
        history['n_backtrack'].append(int(len(tracking)))
        history['bt_tracking'].append(tracking)

    return x, history, stop_reason


def conjugate_gradient(f, grad, x0, max_iter, tol, c1, c2, rho):
    """Gradiente conjugado no lineal (Polak-Ribiere+) con backtracking Armijo."""
    x = np.array(x0, dtype=float).flatten()
    n = len(x)
    g = grad(x)
    g_norm = float(np.linalg.norm(g))
    d = -g.copy()
    history = _init_history(x, f(x), g_norm)
    stop_reason = "Iteraciones agotadas"

    for k in range(max_iter):
        if g_norm < tol:
            stop_reason = f"Convergencia alcanzada (||grad|| < {tol})"
            break

        alpha, tracking = backtracking_line_search(f, grad, x, d, c1=c1, c2=c2, rho=rho)
        x_new = x + alpha * d
        g_new = grad(x_new)

        # Polak-Ribiere+
        denom = float(np.dot(g, g))
        if denom < 1e-20:
            beta = 0.0
        else:
            beta = float(np.dot(g_new, g_new - g)) / denom
            beta = max(beta, 0.0)

        d = -g_new + beta * d

        # Reinicio si la nueva direccion no es de descenso o periodicamente
        if float(np.dot(g_new, d)) >= 0 or (k + 1) % n == 0:
            d = -g_new

        x = x_new
        g = g_new
        g_norm = float(np.linalg.norm(g))

        history['x'].append(x.copy())
        history['f'].append(float(f(x)))
        history['grad_norm'].append(g_norm)
        history['alpha'].append(float(alpha))
        history['n_backtrack'].append(int(len(tracking)))
        history['bt_tracking'].append(tracking)

    return x, history, stop_reason


def newton_method(f, grad, hess, x0, max_iter, tol, c1, c2, rho):
    """Metodo de Newton con backtracking Armijo."""
    x = np.array(x0, dtype=float).flatten()
    g = grad(x)
    g_norm = float(np.linalg.norm(g))
    history = _init_history(x, f(x), g_norm)
    stop_reason = "Iteraciones agotadas"

    for k in range(max_iter):
        if g_norm < tol:
            stop_reason = f"Convergencia alcanzada (||grad|| < {tol})"
            break

        H = hess(x)

        # Caso 1D: Hessiana es 1x1
        if H.shape == (1, 1):
            h_val = float(H[0, 0])
            if abs(h_val) < 1e-14:
                raise np.linalg.LinAlgError(
                    "Hessiana nula o casi nula en iteracion {}.".format(k)
                )
            d = -g / h_val
        else:
            try:
                d = np.linalg.solve(H, -g)
            except np.linalg.LinAlgError as e:
                raise np.linalg.LinAlgError(
                    f"Hessiana singular en iteracion {k}: {e}"
                )

        # Fallback a -g si no es direccion de descenso
        if float(np.dot(g, d)) >= 0:
            d = -g

        alpha, tracking = backtracking_line_search(f, grad, x, d, c1=c1, c2=c2, rho=rho)
        x = x + alpha * d
        g = grad(x)
        g_norm = float(np.linalg.norm(g))

        history['x'].append(x.copy())
        history['f'].append(float(f(x)))
        history['grad_norm'].append(g_norm)
        history['alpha'].append(float(alpha))
        history['n_backtrack'].append(int(len(tracking)))
        history['bt_tracking'].append(tracking)

    return x, history, stop_reason


# =============================================================================
# VISUALIZACION
# =============================================================================

def plot_convergence(history):
    """Grafico de norma del gradiente vs iteraciones."""
    grad_norms = history.get('grad_norm', [])
    if len(grad_norms) == 0:
        return None

    # Limpieza: convertir a array, descartar NaN/Inf que dañarian la escala log
    arr = np.array(grad_norms, dtype=float)
    finite_mask = np.isfinite(arr)
    if not np.any(finite_mask):
        return None

    iter_idx = np.arange(len(arr))[finite_mask]
    y_vals = arr[finite_mask]

    # Decidir escala: si todos los valores son positivos y abarcan al menos 1
    # orden de magnitud, usamos log; de lo contrario lineal para evitar la
    # apariencia de "linea plana constante".
    positive_mask = y_vals > 0
    use_log = False
    if np.any(positive_mask):
        pos_vals = y_vals[positive_mask]
        if pos_vals.min() > 0 and (pos_vals.max() / pos_vals.min()) > 10.0:
            use_log = True

    # Sustituimos ceros exactos por un piso minimo razonable para que la escala
    # log no los excluya silenciosamente
    if use_log:
        floor = max(np.finfo(float).eps, pos_vals.min() * 1e-3)
        y_plot = np.where(y_vals > 0, y_vals, floor)
    else:
        y_plot = y_vals

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=iter_idx,
        y=y_plot,
        mode='lines+markers',
        name='||grad f(x_k)||',
        line=dict(color='#b22222', width=2),
        marker=dict(color='#ff4444', size=6),
        hovertemplate='Iter k=%{x}<br>||grad||=%{y:.6e}<extra></extra>',
    ))
    fig.update_layout(
        template='plotly_dark',
        title='CURVA DE CONVERGENCIA',
        xaxis_title='Iteracion k',
        yaxis_title='Norma del gradiente' + (' (escala log)' if use_log else ''),
        yaxis_type='log' if use_log else 'linear',
        paper_bgcolor='#000000',
        plot_bgcolor='#0a0a0a',
        font=dict(family='Courier New', color='#cccccc'),
        height=400,
    )
    return fig


def plot_1d(f_callable, history, variable_name):
    """Grafico 2D para funciones de 1 variable."""
    trajectory = np.array([x[0] for x in history['x']])
    f_values = np.array(history['f'])

    # Rango: cubrir la trayectoria con margen
    x_min, x_max = float(trajectory.min()), float(trajectory.max())
    span = max(x_max - x_min, 1.0)
    margin = 0.5 * span + 1.0
    xs = np.linspace(x_min - margin, x_max + margin, 400)
    try:
        ys = np.array([f_callable(np.array([xi])) for xi in xs])
    except Exception:
        return None

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=xs, y=ys,
        mode='lines',
        name=f'f({variable_name})',
        line=dict(color='#888888', width=2),
    ))
    fig.add_trace(go.Scatter(
        x=trajectory, y=f_values,
        mode='lines+markers',
        name='Trayectoria',
        line=dict(color='#b22222', width=2, dash='dot'),
        marker=dict(color='#ff4444', size=8, symbol='circle'),
    ))
    # Marcar punto final
    fig.add_trace(go.Scatter(
        x=[trajectory[-1]], y=[f_values[-1]],
        mode='markers',
        name='Minimo encontrado',
        marker=dict(color='#ffff00', size=14, symbol='x'),
    ))

    fig.update_layout(
        template='plotly_dark',
        title='TRAYECTORIA DEL DESCENSO',
        xaxis_title=variable_name,
        yaxis_title=f'f({variable_name})',
        paper_bgcolor='#000000',
        plot_bgcolor='#0a0a0a',
        font=dict(family='Courier New', color='#cccccc'),
        height=500,
    )
    return fig


def plot_2d_contour(f_callable, history, var_names):
    """Mapa topografico (contour plot) para funciones de 2 variables."""
    traj = np.array(history['x'])  # shape (k, 2)
    x_coords = traj[:, 0]
    y_coords = traj[:, 1]

    x_min, x_max = float(x_coords.min()), float(x_coords.max())
    y_min, y_max = float(y_coords.min()), float(y_coords.max())
    x_span = max(x_max - x_min, 1.0)
    y_span = max(y_max - y_min, 1.0)
    x_margin = 0.5 * x_span + 1.0
    y_margin = 0.5 * y_span + 1.0

    xs = np.linspace(x_min - x_margin, x_max + x_margin, 100)
    ys = np.linspace(y_min - y_margin, y_max + y_margin, 100)
    X, Y = np.meshgrid(xs, ys)
    Z = np.zeros_like(X)
    try:
        for i in range(X.shape[0]):
            for j in range(X.shape[1]):
                Z[i, j] = f_callable(np.array([X[i, j], Y[i, j]]))
    except Exception:
        return None

    fig = go.Figure()
    fig.add_trace(go.Contour(
        x=xs, y=ys, z=Z,
        colorscale='Greys',
        contours=dict(
            showlabels=True,
            labelfont=dict(color='#cccccc', family='Courier New', size=10),
        ),
        colorbar=dict(title='f(x,y)', tickfont=dict(color='#cccccc')),
        opacity=0.85,
    ))
    fig.add_trace(go.Scatter(
        x=x_coords, y=y_coords,
        mode='lines+markers',
        name='Trayectoria',
        line=dict(color='#b22222', width=2),
        marker=dict(color='#ff4444', size=7, symbol='circle'),
    ))
    fig.add_trace(go.Scatter(
        x=[x_coords[0]], y=[y_coords[0]],
        mode='markers',
        name='Inicio',
        marker=dict(color='#00ff00', size=14, symbol='diamond'),
    ))
    fig.add_trace(go.Scatter(
        x=[x_coords[-1]], y=[y_coords[-1]],
        mode='markers',
        name='Minimo',
        marker=dict(color='#ffff00', size=14, symbol='x'),
    ))

    fig.update_layout(
        template='plotly_dark',
        title='MAPA TOPOGRAFICO - CURVAS DE NIVEL',
        xaxis_title=var_names[0],
        yaxis_title=var_names[1],
        paper_bgcolor='#000000',
        plot_bgcolor='#0a0a0a',
        font=dict(family='Courier New', color='#cccccc'),
        height=600,
    )
    return fig


# =============================================================================
# INTERFAZ DE USUARIO
# =============================================================================

st.markdown(
    """
    <h1 style="text-align: center;">WeskerMethod</h1>
    <p class="wesker-lore-centered">// CLASSIFIED - UMBRELLA INTERNAL USE ONLY - ACCESS LEVEL 6 CLEARANCE REQUIRED //</p>
    """,
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='text-align: center;'><em>Sistema de optimizacion matematica para localizacion de minimos en espacios n-dimensionales</em></p>",
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="wesker-lore">Log 0451 :: Raccoon City Underground Lab - Sector B5 - Optimization engine deployed for Project Tyrant containment protocols.</div>',
    unsafe_allow_html=True,
)
st.markdown("---")

# =============================================================================
# PANEL DE PARAMETROS - LAYOUT EN COLUMNAS (SIN SIDEBAR)
# =============================================================================

st.markdown(
    """
    <div class="wesker-lore">Memo HUNK :: STARS unit neutralized. Spencer Mansion archives integrated into this terminal.</div>
    """,
    unsafe_allow_html=True,
)
st.markdown("### PARAMETROS DE OPERACION")

# Fila 1: numero de variables y metodo
row1_col1, row1_col2 = st.columns([1, 2])
with row1_col1:
    n_vars = st.number_input(
        "Numero de variables",
        min_value=1, max_value=500, value=2, step=1
    )
with row1_col2:
    method = st.selectbox(
        "Metodo de optimizacion",
        ["Gradiente", "Gradiente Conjugado", "Newton"]
    )

# Defaults dinamicos segun n_vars
if n_vars == 1:
    default_func = "x^2 - 4*x + 3"
    default_x0 = "5"
elif n_vars == 2:
    default_func = "x^2 + y^2 - 2*x*y + 4*x"
    default_x0 = "1.0, 1.0"
else:
    default_func = " + ".join([f"x{i}^2" for i in range(1, n_vars + 1)])
    default_x0 = ", ".join(["1.0"] * n_vars)

# Fila 2: funcion objetivo (mas ancha) y punto de partida
row2_col1, row2_col2 = st.columns([2, 1])
with row2_col1:
    func_str = st.text_area(
        "Funcion objetivo (use ^ para potencias)",
        value=default_func,
        height=100,
    )
with row2_col2:
    x0_str = st.text_area(
        "Punto de partida (separado por comas)",
        value=default_x0,
        height=100,
    )

# Fila 3: tolerancia, iteraciones y parametros de Wolfe
st.markdown(
    """
    <div class="wesker-lore">Encrypted Note :: T-Virus mutation logs sealed under Wesker private key. Decryption requires director authorization.</div>
    """,
    unsafe_allow_html=True,
)
st.markdown("### CRITERIOS DE CONVERGENCIA Y BUSQUEDA DE LINEA")
row3_col1, row3_col2, row3_col3, row3_col4, row3_col5 = st.columns(5)
with row3_col1:
    max_iter = st.number_input(
        "Maximo de iteraciones",
        min_value=1, max_value=10000, value=100, step=10
    )
with row3_col2:
    tol = st.number_input(
        "Tolerancia",
        min_value=1e-15, max_value=1.0, value=1e-6, format="%.1e"
    )
with row3_col3:
    c1 = st.number_input(
        "c1 (Armijo)",
        min_value=1e-6, max_value=0.5, value=1e-4, format="%.1e"
    )
with row3_col4:
    c2 = st.number_input(
        "c2 (Curvatura)",
        min_value=0.1, max_value=0.999, value=0.9, step=0.05
    )
with row3_col5:
    rho = st.number_input(
        "Factor de reduccion (rho)",
        min_value=0.1, max_value=0.9, value=0.5, step=0.05
    )

if c1 >= c2:
    st.warning("Se recomienda c1 < c2 para coherencia teorica de las condiciones de Wolfe.")

st.markdown("---")

st.markdown(
    """
    <div class="wesker-lore">Transmission 12-A :: Bioweapon Containment Division standing by. Awaiting authorization to engage minimization protocol.</div>
    """,
    unsafe_allow_html=True,
)

# Boton ancho de ejecucion
execute = st.button("EJECUTAR OPTIMIZACION", use_container_width=True)

st.markdown("---")

# =============================================================================
# RESULTADOS Y VISUALIZACION
# =============================================================================
if not execute:
    st.info("Configure los parametros en el panel superior y presione EJECUTAR OPTIMIZACION para iniciar el analisis.")
else:
    try:
        # Parseo de la funcion
        expr, variables, grad_expr, hess_expr = parse_function(func_str, int(n_vars))
        var_names = [str(v) for v in variables]
        f_callable, grad_callable, hess_callable = make_numeric_evaluators(
            expr, variables, grad_expr, hess_expr
        )

        # Parseo del punto inicial
        try:
            x0 = np.array([float(v.strip()) for v in x0_str.split(",")], dtype=float)
        except ValueError:
            raise ValueError("El punto de partida debe ser una lista de numeros separados por comas.")

        if len(x0) != len(variables):
            raise ValueError(
                f"El punto inicial tiene {len(x0)} componentes pero se requieren {len(variables)}."
            )

        # Ejecucion del algoritmo
        with st.spinner(f"Ejecutando {method}..."):
            if method == "Gradiente":
                x_star, history, stop_reason = gradient_descent(
                    f_callable, grad_callable, x0, int(max_iter), float(tol),
                    float(c1), float(c2), float(rho)
                )
            elif method == "Gradiente Conjugado":
                x_star, history, stop_reason = conjugate_gradient(
                    f_callable, grad_callable, x0, int(max_iter), float(tol),
                    float(c1), float(c2), float(rho)
                )
            else:  # Newton
                x_star, history, stop_reason = newton_method(
                    f_callable, grad_callable, hess_callable, x0,
                    int(max_iter), float(tol), float(c1), float(c2), float(rho)
                )

        f_star = f_callable(x_star)
        n_iter = len(history['x']) - 1
        final_grad_norm = history['grad_norm'][-1] if history['grad_norm'] else float('nan')

        # Deteccion de divergencia: funcion no acotada inferiormente o iterado fuera de rango
        if not np.all(np.isfinite(x_star)) or not np.isfinite(f_star):
            raise OverflowError(
                "El iterando o el valor de la funcion no es finito (inf/nan detectado). "
                "La funcion objetivo podria no estar acotada inferiormente."
            )
        # Tambien detectamos si la trayectoria divergio en algun momento
        f_history_arr = np.array(history['f'], dtype=float)
        if not np.all(np.isfinite(f_history_arr)):
            raise OverflowError(
                "La trayectoria del algoritmo genero valores no finitos (inf/nan). "
                "La funcion objetivo podria no estar acotada inferiormente."
            )

        # --- Resultados con st.metric (inmediatamente debajo del boton) ---
        st.markdown(
            """
            <div class="wesker-lore">Field Report :: Specimen W-001 (A. Wesker) demonstrated convergence beyond human limits. Replication studies ongoing.</div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("### RESULTADOS")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            # Formateo visual a 2 decimales (precision matematica interna intacta)
            x_str = "[" + ", ".join([f"{v:.2f}" for v in x_star]) + "]"
            st.metric("Punto minimo (x*)", x_str)
        with col2:
            st.metric("f(x*)", f"{f_star:.2f}")
        with col3:
            st.metric("Iteraciones", n_iter)
        with col4:
            st.metric("Norma final ||grad||", f"{final_grad_norm:.2f}")

        st.info(f"Criterio de parada: {stop_reason}")

        st.markdown("---")

        # --- Telemetria del backtracking ---
        st.markdown("### REGISTRO DE TELEMETRIA (BACKTRACKING)")

        import pandas as pd  # import local: evita cargas innecesarias

        # Resumen por iteracion global
        telem_rows = []
        for k_idx in range(len(history['x'])):
            xk = history['x'][k_idx]
            xk_fmt = "[" + ", ".join(f"{v:.4f}" for v in xk) + "]"
            alpha_k = history['alpha'][k_idx]
            nb_k = history['n_backtrack'][k_idx]
            telem_rows.append({
                'Iteracion (k)': k_idx,
                'x_k': xk_fmt,
                'f(x_k)': f"{history['f'][k_idx]:.4f}",
                '||grad||': f"{history['grad_norm'][k_idx]:.4f}",
                'Alpha': "---" if (isinstance(alpha_k, float) and np.isnan(alpha_k)) else f"{alpha_k:.4f}",
                'Iter. Backtracking': "---" if nb_k < 0 else int(nb_k),
            })
        df_telem = pd.DataFrame(telem_rows)
        st.dataframe(df_telem, use_container_width=True, hide_index=True)

        # --- Detalle microscopico por iteracion global seleccionada ---
        st.markdown("#### DETALLE MICROSCOPICO DEL BACKTRACKING")

        # Solo iteraciones globales con tracking (excluye k=0 que es estado inicial)
        valid_k = [k_idx for k_idx in range(len(history['bt_tracking']))
                   if len(history['bt_tracking'][k_idx]) > 0]

        if len(valid_k) == 0:
            st.info("No hay intentos de backtracking registrados (el algoritmo no realizo iteraciones).")
        else:
            k_selected = st.selectbox(
                "Ver detalle de Backtracking para Iteracion Global:",
                options=valid_k,
                index=0,
                format_func=lambda k: f"k = {k}",
            )

            tracking_k = history['bt_tracking'][k_selected]
            detail_rows = []
            for entry in tracking_k:
                x_new_fmt = "[" + ", ".join(f"{v:.4f}" for v in entry['x_new']) + "]"
                detail_rows.append({
                    'Iteracion BT': entry['iter_bt'],
                    'Alpha': f"{entry['alpha']:.4f}",
                    'x = x_k + alpha * d': x_new_fmt,
                    'LHS: f(x)': f"{entry['lhs_armijo']:.4f}",
                    'RHS Armijo': f"{entry['rhs_armijo']:.4f}",
                    'LHS <= RHS': "Si" if entry['cumple_armijo'] else "No",
                    '¿Cumple Wolfe 2?': "Si" if entry['cumple_wolfe2'] else "No",
                })
            df_detail = pd.DataFrame(detail_rows)
            st.dataframe(df_detail, use_container_width=True, hide_index=True)

        st.markdown("---")

        # --- Expresiones simbolicas ---
        st.markdown("### EXPRESIONES SIMBOLICAS")
        col_a, col_b = st.columns(2)

        with col_a:
            st.markdown("**Variables (orden alfabetico):**")
            st.latex(", ".join(var_names))
            st.markdown("**Funcion objetivo:**")
            st.latex("f(" + ", ".join(var_names) + ") = " + sp.latex(expr))

        with col_b:
            st.markdown("**Gradiente:**")
            if len(variables) == 1:
                st.latex(r"\nabla f = \frac{df}{d" + var_names[0] + "} = " + sp.latex(grad_expr[0]))
            else:
                grad_vec = sp.Matrix(grad_expr)
                st.latex(r"\nabla f = " + sp.latex(grad_vec))

            st.markdown("**Hessiana:**")
            if len(variables) == 1:
                st.latex(r"\nabla^2 f = \frac{d^2 f}{d" + var_names[0] + "^2} = " + sp.latex(hess_expr[0, 0]))
            else:
                st.latex(r"\nabla^2 f = " + sp.latex(hess_expr))

        st.markdown("---")

        # --- Graficos al final ---
        st.markdown(
            """
            <div class="wesker-lore">Birkin Notes :: Convergence curves echo the G-virus replication pattern. Telemetry archived in vault NE-7.</div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("### ANALISIS DE CONVERGENCIA")
        fig_conv = plot_convergence(history)
        if fig_conv is not None:
            st.plotly_chart(fig_conv, use_container_width=True)

        # --- Grafico espacial segun dimensionalidad ---
        if len(variables) == 1:
            st.markdown("### VISUALIZACION 2D - FUNCION UNIVARIADA")
            fig_1d = plot_1d(f_callable, history, var_names[0])
            if fig_1d is not None:
                st.plotly_chart(fig_1d, use_container_width=True)
            else:
                st.warning("No se pudo renderizar el grafico 1D para esta funcion.")
        elif len(variables) == 2:
            st.markdown("### MAPA TOPOGRAFICO - CURVAS DE NIVEL")
            fig_2d = plot_2d_contour(f_callable, history, var_names)
            if fig_2d is not None:
                st.plotly_chart(fig_2d, use_container_width=True)
            else:
                st.warning("No se pudo renderizar el mapa de contorno para esta funcion.")
        else:
            st.info(f"Dimension del problema: {len(variables)}. Visualizacion espacial omitida por exceder 2D.")

    except (sp.SympifyError, SyntaxError, TypeError) as e:
        st.error(f"ERROR DE SINTAXIS en la funcion objetivo: {e}")
    except np.linalg.LinAlgError as e:
        st.error(
            "ALERTA DE SEGURIDAD - UMBRELLA CORP: SISTEMA COMPROMETIDO. "
            "Se ha detectado una anomalia matematica critica. El sujeto de prueba "
            "(funcion objetivo) carece de un minimo acotado o ha generado una "
            "singularidad inestable en el espacio dimensional. Protocolo de "
            "contencion activado."
        )
        st.error(
            f"Diagnostico tecnico: matriz Hessiana singular o sistema lineal "
            f"mal condicionado durante la resolucion. Detalle: {e}. "
            f"Causa probable: la Hessiana es no invertible en algun iterando "
            f"(determinante cero o columnas linealmente dependientes). Considere "
            f"reformular la funcion, usar otro punto inicial, o aplicar el "
            f"metodo del Gradiente o Gradiente Conjugado."
        )
    except ZeroDivisionError as e:
        st.error(
            "ALERTA DE SEGURIDAD - UMBRELLA CORP: SISTEMA COMPROMETIDO. "
            "Se ha detectado una anomalia matematica critica. El sujeto de prueba "
            "(funcion objetivo) carece de un minimo acotado o ha generado una "
            "singularidad inestable en el espacio dimensional. Protocolo de "
            "contencion activado."
        )
        st.error(
            f"Diagnostico tecnico: division por cero durante la evaluacion. "
            f"Detalle: {e}. Causa probable: la funcion objetivo o su gradiente "
            f"contiene un denominador que se anula en la trayectoria del "
            f"algoritmo."
        )
    except (OverflowError, FloatingPointError) as e:
        st.error(
            "ALERTA DE SEGURIDAD - UMBRELLA CORP: SISTEMA COMPROMETIDO. "
            "Se ha detectado una anomalia matematica critica. El sujeto de prueba "
            "(funcion objetivo) carece de un minimo acotado o ha generado una "
            "singularidad inestable en el espacio dimensional. Protocolo de "
            "contencion activado."
        )
        st.error(
            f"Diagnostico tecnico: desbordamiento numerico durante la "
            f"iteracion. Detalle: {e}. Causa probable: la funcion no esta "
            f"acotada inferiormente (tiende a menos infinito) o el iterando "
            f"diverge hacia magnitudes fuera del rango representable. "
            f"Verifique que la funcion tenga al menos un minimo local en la "
            f"vecindad del punto inicial."
        )
    except ValueError as e:
        st.error(f"ERROR DE VALIDACION: {e}")
    except Exception as e:
        # Captura cualquier otra anomalia inesperada con la misma alerta corporativa
        st.error(
            "ALERTA DE SEGURIDAD - UMBRELLA CORP: SISTEMA COMPROMETIDO. "
            "Se ha detectado una anomalia matematica critica. El sujeto de prueba "
            "(funcion objetivo) carece de un minimo acotado o ha generado una "
            "singularidad inestable en el espacio dimensional. Protocolo de "
            "contencion activado."
        )
        st.error(f"Diagnostico tecnico: {type(e).__name__}: {e}")


# --- Footer ---
st.markdown(
    '<div class="wesker-footer">Desarrollado en las instalaciones de Raccoon City | Aprobado por A. Wesker</div>',
    unsafe_allow_html=True
)
