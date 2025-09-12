from typing import List, Tuple
import numpy as np
from .bresenham import bresenham_line

def rasterize_bezier(p0: Tuple[int, int], p1: Tuple[int, int], p2: Tuple[int, int], p3: Tuple[int, int], num_segments: int = 50) -> List[Tuple[int, int]]:
    """
    Calcula os pontos de uma curva de Bézier cúbica e os rasteriza com o algoritmo de Bresenham.
    
    Args:
        p0: Ponto inicial.
        p1: Primeiro ponto de controle.
        p2: Segundo ponto de controle.
        p3: Ponto final.
        num_segments: Número de segmentos de linha para aproximar a curva.
    """
    
    # Converte os pontos para o formato numpy para facilitar os cálculos
    p0, p1, p2, p3 = np.array(p0), np.array(p1), np.array(p2), np.array(p3)
    
    # Gera uma lista de pontos (vértices) ao longo da curva de Bézier
    curve_vertices = []
    for i in range(num_segments + 1):
        t = i / num_segments
        # Fórmula da curva de Bézier cúbica
        point = (1-t)**3 * p0 + 3*(1-t)**2 * t * p1 + 3*(1-t) * t**2 * p2 + t**3 * p3
        curve_vertices.append(tuple(point.round().astype(int)))

    # Rasteriza os segmentos de linha entre os vértices da curva
    rasterized_points = set()
    for i in range(num_segments):
        start_point = curve_vertices[i]
        end_point = curve_vertices[i+1]
        line_segment_pixels = bresenham_line(start_point[0], start_point[1], end_point[0], end_point[1])
        rasterized_points.update(line_segment_pixels)
        
    return sorted(list(rasterized_points))