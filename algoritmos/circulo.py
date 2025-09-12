from typing import List, Tuple

def midpoint_circle(xc: int, yc: int, radius: int) -> List[Tuple[int, int]]:
    """Gera os pontos para um círculo usando o algoritmo do ponto médio."""
    if radius <= 0:
        return [(xc, yc)] if radius == 0 else []
        
    points = set()
    x = radius
    y = 0
    p = 1 - radius

    while x >= y:
        points.update([
            (xc + x, yc + y), (xc - x, yc + y), (xc + x, yc - y), (xc - x, yc - y),
            (xc + y, yc + x), (xc - y, yc + x), (xc + y, yc - x), (xc - y, yc - x)
        ])
        
        y += 1
        if p <= 0:
            p = p + 2 * y + 1
        else:
            x -= 1
            p = p + 2 * y - 2 * x + 1
            
    return sorted(list(points))