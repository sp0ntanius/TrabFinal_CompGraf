import math
from typing import List, Tuple

def translacao(vertices: List[Tuple[int, int]], dx: int, dy: int) -> List[Tuple[int, int]]:
    """
    Translada todos os vértices pelo deslocamento dx, dy.
    """
    return [(x + dx, y + dy) for x, y in vertices]

def rotacao(vertices: List[Tuple[int, int]], angulo_graus: float, pivô: Tuple[int, int]) -> List[Tuple[int, int]]:
    """
    Rotaciona todos os vértices em torno do pivô pelo ângulo em graus.
    """
    angulo_rad = math.radians(angulo_graus)
    cos_theta = math.cos(angulo_rad)
    sin_theta = math.sin(angulo_rad)
    px, py = pivô
    novos_vertices = []
    for x, y in vertices:
        # Translada para origem
        x0, y0 = x - px, y - py
        # Aplica rotação
        xr = x0 * cos_theta - y0 * sin_theta
        yr = x0 * sin_theta + y0 * cos_theta
        # Translada de volta
        novos_vertices.append((int(round(xr + px)), int(round(yr + py))))
    return novos_vertices

def escala(vertices: List[Tuple[int, int]], sx: float, sy: float, ponto_fixo: Tuple[int, int]) -> List[Tuple[int, int]]:
    """
    Aplica escala sx, sy em relação ao ponto fixo.
    """
    fx, fy = ponto_fixo
    novos_vertices = []
    for x, y in vertices:
        # Translada para origem
        x0, y0 = x - fx, y - fy
        # Aplica escala
        xs = x0 * sx
        ys = y0 * sy
        # Translada de volta
        novos_vertices.append((int(round(xs + fx)), int(round(ys + fy))))
    return novos_vertices