from typing import Tuple

# Códigos de região
INSIDE = 0  # 0000
LEFT = 1    # 0001
RIGHT = 2   # 0010
BOTTOM = 4  # 0100
TOP = 8     # 1000

def cohen_sutherland_clip(x0: int, y0: int, x1: int, y1: int, xmin: int, ymin: int, xmax: int, ymax: int) -> Tuple[bool, int, int, int, int]:
    """
    Recorta uma linha (x0,y0) a (x1,y1) contra uma janela de recorte.

    Args:
        x0, y0, x1, y1: Coordenadas da linha.
        [cite_start]xmin, ymin, xmax, ymax: Coordenadas da janela de recorte. [cite: 59]

    Returns:
        Uma tupla (aceito, x0', y0', x1', y1') com as novas coordenadas da linha, se aceita.
    """
    
    def _compute_code(x, y):
        code = INSIDE
        if x < xmin:
            code |= LEFT
        elif x > xmax:
            code |= RIGHT
        if y < ymin:
            code |= BOTTOM
        elif y > ymax:
            code |= TOP
        return code

    code0 = _compute_code(x0, y0)
    code1 = _compute_code(x1, y1)
    accepted = False

    while True:
        # Caso 1: Ambos os pontos dentro (aceitação trivial)
        if code0 == 0 and code1 == 0:
            accepted = True
            break
        # Caso 2: Ambos os pontos fora na mesma região (rejeição trivial)
        elif (code0 & code1) != 0:
            break
        # Caso 3: Precisa recortar
        else:
            x, y = 0, 0
            # Pelo menos um ponto está fora, pegue ele
            code_out = code1 if code1 > code0 else code0

            # Calcula o ponto de interseção
            if code_out & TOP:
                x = x0 + (x1 - x0) * (ymax - y0) / (y1 - y0)
                y = ymax
            elif code_out & BOTTOM:
                x = x0 + (x1 - x0) * (ymin - y0) / (y1 - y0)
                y = ymin
            elif code_out & RIGHT:
                x = xmax
                y = y0 + (y1 - y0) * (xmax - x0) / (x1 - x0)
            elif code_out & LEFT:
                x = xmin
                y = y0 + (y1 - y0) * (xmin - x0) / (x1 - x0)
            
            # Atualiza o ponto que estava fora com a interseção
            if code_out == code0:
                x0, y0 = int(x), int(y)
                code0 = _compute_code(x0, y0)
            else:
                x1, y1 = int(x), int(y)
                code1 = _compute_code(x1, y1)

    return accepted, x0, y0, x1, y1