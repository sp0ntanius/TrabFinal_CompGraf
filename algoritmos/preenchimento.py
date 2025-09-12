# algorithms/fill.py

from typing import List, Tuple, Set

def recursive_fill(x: int, y: int, boundary_pixels: Set[Tuple[int, int]], canvas_dimensions: Tuple[int, int]) -> Set[Tuple[int, int]]:
    """
    Preenche uma área a partir de um ponto inicial (x,y) até encontrar uma barreira.

    Args:
        [cite_start]x, y: Ponto inicial para o preenchimento. [cite: 53]
        boundary_pixels: Um set com os pontos (x,y) que formam a barreira.
        canvas_dimensions: A largura e altura do canvas para evitar preenchimento infinito.
    """
    filled_pixels = set()
    width, height = canvas_dimensions
    
    # Usamos uma pilha para simular a recursão e evitar estouro de pilha
    stack = [(x, y)]
    
    while stack:
        px, py = stack.pop()
        
        # Verifica se o pixel está dentro dos limites, não é barreira e ainda não foi preenchido
        # A verificação de limites é uma salvaguarda.
        if (
            -width//2 < px < width//2 and 
            -height//2 < py < height//2 and
            (px, py) not in boundary_pixels and 
            (px, py) not in filled_pixels
        ):
            filled_pixels.add((px, py))
            stack.append((px + 1, py))
            stack.append((px - 1, py))
            stack.append((px, py + 1))
            stack.append((px, py - 1))
            
    return filled_pixels