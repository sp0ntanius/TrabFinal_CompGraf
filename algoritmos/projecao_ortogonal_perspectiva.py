from typing import List, Tuple

def projecao_ortogonal(vertices_3d: List[Tuple[float, float, float]], eixo: str = 'z') -> List[Tuple[int, int]]:
    """
    Projeta ortogonalmente os vértices 3D em 2D, ignorando o eixo especificado.
    Por padrão, projeta no plano XY (ignora Z).
    """
    if eixo == 'z':
        return [(int(round(x)), int(round(y))) for x, y, z in vertices_3d]
    elif eixo == 'y':
        return [(int(round(x)), int(round(z))) for x, y, z in vertices_3d]
    elif eixo == 'x':
        return [(int(round(y)), int(round(z))) for x, y, z in vertices_3d]
    else:
        raise ValueError("Eixo deve ser 'x', 'y' ou 'z'.")

def projecao_perspectiva(vertices_3d: List[Tuple[float, float, float]], d: float = 200.0) -> List[Tuple[int, int]]:
    """
    Projeta os vértices 3D em 2D usando projeção perspectiva simples.
    d: distância do observador ao plano de projeção (quanto maior, menos distorção).
    """
    resultado = []
    for x, y, z in vertices_3d:
        # Evita divisão por zero
        fator = d / (d + z) if (d + z) != 0 else 1
        xp = x * fator
        yp = y * fator
        resultado.append((int(round(xp)), int(round(yp))))
    return resultado