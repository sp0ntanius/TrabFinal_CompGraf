from typing import List, Tuple
from .bresenham import bresenham_line

def draw_polyline(vertices: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """
    Gera os pixels para uma polilinha conectando uma lista de vértices.

    Args:
        [cite_start]vertices: Uma lista de pontos (x, y). [cite: 45]
    """
    if len(vertices) < 2:
        return []

    all_points = set()
    for i in range(len(vertices) - 1):
        p1 = vertices[i]
        p2 = vertices[i+1]
        line_segment = bresenham_line(p1[0], p1[1], p2[0], p2[1])
        all_points.update(line_segment)
    
    return sorted(list(all_points))