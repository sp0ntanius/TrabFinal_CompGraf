from typing import List, Tuple

def sutherland_hodgman_clip(polygon: List[Tuple[int, int]], clip_rect: Tuple[int, int, int, int]) -> List[Tuple[int, int]]:
    """
    Recorta um polígono contra uma janela retangular usando Sutherland-Hodgman.

    Args:
        polygon: Lista de vértices [(x1, y1), (x2, y2), ...].
        clip_rect: (xmin, ymin, xmax, ymax) da janela de recorte.

    Returns:
        Lista de vértices do polígono recortado.
    """
    xmin, ymin, xmax, ymax = clip_rect

    def clip_edge(vertices, edge_fn):
        result = []
        if not vertices:
            return result
        prev = vertices[-1]
        for curr in vertices:
            if edge_fn(curr):
                if not edge_fn(prev):
                    # Interseção entrando
                    result.append(intersect(prev, curr, edge_fn))
                result.append(curr)
            elif edge_fn(prev):
                # Interseção saindo
                result.append(intersect(prev, curr, edge_fn))
            prev = curr
        return result

    def intersect(p1, p2, edge_fn):
        x1, y1 = p1
        x2, y2 = p2
        if edge_fn == left_edge:
            x = xmin
            y = y1 + (y2 - y1) * (xmin - x1) / (x2 - x1)
        elif edge_fn == right_edge:
            x = xmax
            y = y1 + (y2 - y1) * (xmax - x1) / (x2 - x1)
        elif edge_fn == bottom_edge:
            y = ymin
            x = x1 + (x2 - x1) * (ymin - y1) / (y2 - y1)
        elif edge_fn == top_edge:
            y = ymax
            x = x1 + (x2 - x1) * (ymax - y1) / (y2 - y1)
        return (int(round(x)), int(round(y)))

    def left_edge(p):   return p[0] >= xmin
    def right_edge(p):  return p[0] <= xmax
    def bottom_edge(p): return p[1] >= ymin
    def top_edge(p):    return p[1] <= ymax

    clipped = polygon
    for edge_fn in [left_edge, right_edge, bottom_edge, top_edge]:
        clipped = clip_edge(clipped, edge_fn)
    return clipped