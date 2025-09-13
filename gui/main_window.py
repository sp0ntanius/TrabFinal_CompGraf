import tkinter as tk
from tkinter import ttk, messagebox
import re
from algoritmos.bresenham import bresenham_line
from algoritmos.circulo import midpoint_circle
from algoritmos.curva import rasterize_bezier
from algoritmos.polilinha import draw_polyline
from algoritmos.preenchimento import recursive_fill
from algoritmos.recorte import cohen_sutherland_clip
from algoritmos.recorte_poligono import sutherland_hodgman_clip
from algoritmos.transformacoes import translacao, rotacao, escala


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.drawn_pixels = set()  # <-- Adicione esta linha
        self.title("Computação Gráfica - Trabalho Final")
        self.geometry("1000x700")

        # --- Layout Principal ---
        # Frame de controles à direita com scroll
        control_canvas = tk.Canvas(self, width=250)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=control_canvas.yview)
        control_canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        control_canvas.pack(side="right", fill="y", expand=False)

        # Frame real de controles dentro do canvas
        control_frame = ttk.Frame(control_canvas)
        control_canvas.create_window((0, 0), window=control_frame, anchor="nw")

        # Atualiza o scrollregion quando widgets são adicionados
        def on_configure(event):
            control_canvas.configure(scrollregion=control_canvas.bbox("all"))
        control_frame.bind("<Configure>", on_configure)

        # --- Canvas para desenho à esquerda ---
        self.canvas = tk.Canvas(self, bg="white", highlightthickness=1, highlightbackground="black")
        self.canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        control_canvas.create_window((0, 0), window=control_frame, anchor="nw", width=250)

        self.canvas.update_idletasks()

        # --- Widgets de Controle ---
        self._create_bresenham_controls(control_frame)
        self._create_circle_controls(control_frame)
        self._create_curve_controls(control_frame)
        self._create_polyline_controls(control_frame)
        self._create_fill_controls(control_frame)
        self._create_clipping_controls(control_frame)
        self._create_polygon_clipping_controls(control_frame)
        self._create_transform_controls(control_frame)

        ttk.Button(control_frame, text="Limpar Tela", command=self.clear_canvas).pack(pady=20, fill='x')

    def _create_bresenham_controls(self, parent):
        frame = ttk.LabelFrame(parent, text="Bresenham (Linha)", padding=10)
        frame.pack(fill='x', pady=5)
        
        self.bresenham_entries = {}
        for label_text in ["X0", "Y0", "X1", "Y1"]:
            ttk.Label(frame, text=label_text).pack(side='left', padx=5)
            entry = ttk.Entry(frame, width=5)
            entry.pack(side='left')
            self.bresenham_entries[label_text] = entry
        
        ttk.Button(frame, text="Desenhar", command=self.draw_bresenham_line).pack(side='left', padx=10)

    def _create_circle_controls(self, parent):
        frame = ttk.LabelFrame(parent, text="Círculo", padding=10)
        frame.pack(fill='x', pady=5)

        self.circle_entries = {}
        for label_text in ["Xc", "Yc", "Raio"]:
            ttk.Label(frame, text=label_text).pack(side='left', padx=5)
            entry = ttk.Entry(frame, width=5)
            entry.pack(side='left')
            self.circle_entries[label_text] = entry

        ttk.Button(frame, text="Desenhar", command=self.draw_circle).pack(side='left', padx=10)
        
    def _create_curve_controls(self, parent):
        frame = ttk.LabelFrame(parent, text="Curva de Bézier", padding=10)
        frame.pack(fill='x', pady=5)
        
        self.curve_entries = {}
        # Usando grid para melhor alinhamento
        grid_frame = ttk.Frame(frame)
        grid_frame.pack()
        
        labels = ["P0(x)", "P0(y)", "P1(x)", "P1(y)", "P2(x)", "P2(y)", "P3(x)", "P3(y)"]
        for i, label in enumerate(labels):
            row, col = divmod(i, 4)
            ttk.Label(grid_frame, text=label).grid(row=row*2, column=col, padx=2, pady=2)
            entry = ttk.Entry(grid_frame, width=5)
            entry.grid(row=row*2+1, column=col, padx=2, pady=2)
            self.curve_entries[label] = entry
            
        ttk.Button(frame, text="Desenhar", command=self.draw_bezier_curve).pack(pady=10)
    
    def _create_polyline_controls(self, parent):
        frame = ttk.LabelFrame(parent, text="Polilinha", padding=10)
        frame.pack(fill='x', pady=5)
        ttk.Label(frame, text="Vértices: (x1,y1), (x2,y2), ...").pack(anchor='w')
        self.polyline_entry = ttk.Entry(frame)
        self.polyline_entry.pack(fill='x')
        self.polyline_entry.insert(0, "(-100,-50), (-50,50), (0,-50), (50,50), (100,-50)")
        ttk.Button(frame, text="Desenhar", command=self.draw_polyline_command).pack(pady=5)
    
    def _create_fill_controls(self, parent):
        frame = ttk.LabelFrame(parent, text="Preenchimento Recursivo", padding=10)
        frame.pack(fill='x', pady=5)
        self.fill_entries = {}
        for label_text in ["X", "Y"]:
            ttk.Label(frame, text=label_text).pack(side='left', padx=5)
            entry = ttk.Entry(frame, width=5)
            entry.pack(side='left')
            self.fill_entries[label_text] = entry
        ttk.Button(frame, text="Preencher", command=self.fill_command).pack(side='left', padx=10)

    def _create_clipping_controls(self, parent):
        frame = ttk.LabelFrame(parent, text="Recorte de Linha (Cohen-Sutherland)", padding=10)
        frame.pack(fill='x', pady=5)
        self.clipping_entries = {}
        grid_frame = ttk.Frame(frame)
        grid_frame.pack()
        labels = ["Xmin", "Ymin", "Xmax", "Ymax", "X0", "Y0", "X1", "Y1"]
        defaults = ["-80", "-80", "80", "80", "-100", "0", "100", "20"]
        for i, label in enumerate(labels):
            row, col = divmod(i, 4)
            ttk.Label(grid_frame, text=label).grid(row=row*2, column=col, padx=2, pady=2)
            entry = ttk.Entry(grid_frame, width=5)
            entry.grid(row=row*2+1, column=col, padx=2, pady=2)
            entry.insert(0, defaults[i])
            self.clipping_entries[label] = entry
        ttk.Button(frame, text="Recortar e Desenhar", command=self.clip_and_draw_line).pack(pady=10)

    def _create_polygon_clipping_controls(self, parent):
        frame = ttk.LabelFrame(parent, text="Recorte de Polígono (Sutherland-Hodgman)", padding=10)
        frame.pack(fill='x', pady=5)
        ttk.Label(frame, text="Polígono: (x1,y1), (x2,y2), ...").pack(anchor='w')
        self.polygon_entry = ttk.Entry(frame)
        self.polygon_entry.pack(fill='x')
        self.polygon_entry.insert(0, "(-100,-50), (-50,50), (0,-50), (50,50), (100,-50)")
        ttk.Label(frame, text="Janela: xmin, ymin, xmax, ymax").pack(anchor='w')
        self.clip_rect_entry = ttk.Entry(frame)
        self.clip_rect_entry.pack(fill='x')
        self.clip_rect_entry.insert(0, "-80,-80,80,80")
        ttk.Button(frame, text="Recortar e Desenhar", command=self.clip_and_draw_polygon).pack(pady=5)

    def _create_transform_controls(self, parent):
        frame = ttk.LabelFrame(parent, text="Transformações", padding=10)
        frame.pack(fill='x', pady=5)

        # Polígono
        ttk.Label(frame, text="Polígono: (x1,y1), (x2,y2), ...").pack(anchor='w')
        self.transform_poly_entry = ttk.Entry(frame)
        self.transform_poly_entry.pack(fill='x')
        self.transform_poly_entry.insert(0, "(-100,-50), (-50,50), (0,-50), (50,50), (100,-50)")

        # --- Translação ---
        ttk.Label(frame, text="Translação: dx, dy").pack(anchor='w')
        self.trans_entry = ttk.Entry(frame)
        self.trans_entry.pack(fill='x')
        self.trans_entry.insert(0, "20,30")
        ttk.Button(frame, text="Aplicar Translação", command=self.apply_translation).pack(pady=2, fill='x')

        # --- Rotação ---
        ttk.Label(frame, text="Rotação: Ângulo (graus), Pivô (x,y)").pack(anchor='w')
        self.rot_entry = ttk.Entry(frame)
        self.rot_entry.pack(fill='x')
        self.rot_entry.insert(0, "90,0,-50")
        ttk.Button(frame, text="Aplicar Rotação", command=self.apply_rotation).pack(pady=2, fill='x')

        # --- Escala ---
        ttk.Label(frame, text="Escala: sx, sy, Ponto Fixo (x,y)").pack(anchor='w')
        self.scale_entry = ttk.Entry(frame)
        self.scale_entry.pack(fill='x')
        self.scale_entry.insert(0, "1,2,0,-50")
        ttk.Button(frame, text="Aplicar Escala", command=self.apply_scale).pack(pady=2, fill='x')

    def draw_pixel(self, x, y, color="black"):
        """Desenha um 'pixel' e o adiciona ao set de pixels desenhados."""
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        center_x, center_y = canvas_width / 2, canvas_height / 2
        
        # O sistema de coordenadas do Canvas tem Y invertido em relação ao cartesiano
        plot_x, plot_y = center_x + x, center_y - y
        
        self.canvas.create_rectangle(plot_x, plot_y, plot_x + 1, plot_y + 1, fill=color, outline=color, tags="pixel")
        self.drawn_pixels.add((x,y))

    def clear_canvas(self):
        self.canvas.delete("all")
        self.drawn_pixels.clear()

    def _get_int_values(self, entry_dict):
        """Helper para extrair valores inteiros das caixas de texto."""
        try:
            return [int(entry.get()) for entry in entry_dict.values()]
        except ValueError:
            messagebox.showerror("Erro de Entrada", "Por favor, insira apenas números inteiros.")
            return None

    def draw_bresenham_line(self):
        values = self._get_int_values(self.bresenham_entries)
        if values:
            x0, y0, x1, y1 = values
            points = bresenham_line(x0, y0, x1, y1)
            for x, y in points:
                self.draw_pixel(x, y)

    def draw_circle(self):
        values = self._get_int_values(self.circle_entries)
        if values:
            xc, yc, radius = values
            points = midpoint_circle(xc, yc, radius)
            for x, y in points:
                self.draw_pixel(x, y, color="red") # Cor diferente para destacar

    def draw_bezier_curve(self):
        values = self._get_int_values(self.curve_entries)
        if values:
            p0 = (values[0], values[1])
            p1 = (values[2], values[3])
            p2 = (values[4], values[5])
            p3 = (values[6], values[7])
            points = rasterize_bezier(p0, p1, p2, p3)
            for x, y in points:
                self.draw_pixel(x, y, color="blue")
    
    def draw_polyline_command(self):
        text = self.polyline_entry.get()
        # Regex para encontrar tuplas de números: (num,num)
        try:
            # Encontra todos os pares de números dentro de parênteses
            points_str = re.findall(r'\(\s*(-?\d+)\s*,\s*(-?\d+)\s*\)', text)
            vertices = [(int(x), int(y)) for x, y in points_str]
            if len(vertices) < 2:
                raise ValueError
        except (ValueError, IndexError):
            messagebox.showerror("Erro de Entrada", "Formato inválido. Use: (x1,y1), (x2,y2), ...")
            return
        points = draw_polyline(vertices)
        for x, y in points:
            self.draw_pixel(x, y, color="green")

    def fill_command(self):
        values = self._get_int_values(self.fill_entries)
        if values:
            start_x, start_y = values
            dims = (self.canvas.winfo_width(), self.canvas.winfo_height())
            
            # O preenchimento precisa saber os limites do canvas e as barreiras já desenhadas
            points_to_fill = recursive_fill(start_x, start_y, self.drawn_pixels, dims)
            
            for x, y in points_to_fill:
                self.draw_pixel(x, y, color="orange")
    
    def clip_and_draw_line(self):
        values = self._get_int_values(self.clipping_entries)
        if values:
            xmin, ymin, xmax, ymax, x0, y0, x1, y1 = values

            # Desenha a janela de recorte para visualização
            clip_window_poly = [(xmin, ymin), (xmax, ymin), (xmax, ymax), (xmin, ymax), (xmin, ymin)]
            clip_window_pixels = draw_polyline(clip_window_poly)
            for x, y in clip_window_pixels:
                self.draw_pixel(x, y, color="lightgrey")
            
            # Desenha a linha original em cor suave
            original_line_pixels = bresenham_line(x0, y0, x1, y1)
            for x, y in original_line_pixels:
                # Não adiciona a linha original ao `drawn_pixels` para não interferir no preenchimento
                canvas_width = self.canvas.winfo_width()
                canvas_height = self.canvas.winfo_height()
                center_x, center_y = canvas_width / 2, canvas_height / 2
                plot_x, plot_y = center_x + x, center_y - y
                self.canvas.create_rectangle(plot_x, plot_y, plot_x + 1, plot_y + 1, fill="pink", outline="pink")

            # Recorta e desenha a linha final
            accepted, nx0, ny0, nx1, ny1 = cohen_sutherland_clip(x0, y0, x1, y1, xmin, ymin, xmax, ymax)

            if accepted:
                clipped_line_pixels = bresenham_line(nx0, ny0, nx1, ny1)
                for x, y in clipped_line_pixels:
                    self.draw_pixel(x, y, color="purple")

    def clip_and_draw_polygon(self):
        # Extrai os vértices do polígono
        text = self.polygon_entry.get()
        try:
            points_str = re.findall(r'\(\s*(-?\d+)\s*,\s*(-?\d+)\s*\)', text)
            vertices = [(int(x), int(y)) for x, y in points_str]
            if len(vertices) < 3:
                raise ValueError
        except (ValueError, IndexError):
            messagebox.showerror("Erro de Entrada", "Formato inválido de polígono. Use: (x1,y1), (x2,y2), ...")
            return

        # Extrai a janela de recorte
        rect_text = self.clip_rect_entry.get()
        try:
            rect_values = [int(v) for v in rect_text.split(",")]
            if len(rect_values) != 4:
                raise ValueError
            xmin, ymin, xmax, ymax = rect_values
        except ValueError:
            messagebox.showerror("Erro de Entrada", "Formato inválido da janela. Use: xmin,ymin,xmax,ymax")
            return

        # Desenha a janela de recorte
        clip_window_poly = [(xmin, ymin), (xmax, ymin), (xmax, ymax), (xmin, ymax), (xmin, ymin)]
        clip_window_pixels = draw_polyline(clip_window_poly)
        for x, y in clip_window_pixels:
            self.draw_pixel(x, y, color="lightgrey")

        # Desenha o polígono original
        original_poly_pixels = draw_polyline(vertices + [vertices[0]])
        for x, y in original_poly_pixels:
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            center_x, center_y = canvas_width / 2, canvas_height / 2
            plot_x, plot_y = center_x + x, center_y - y
            self.canvas.create_rectangle(plot_x, plot_y, plot_x + 1, plot_y + 1, fill="pink", outline="pink")

        # Recorta e desenha o polígono final
        clipped_vertices = sutherland_hodgman_clip(vertices, (xmin, ymin, xmax, ymax))
        if len(clipped_vertices) > 2:
            clipped_poly_pixels = draw_polyline(clipped_vertices + [clipped_vertices[0]])
            for x, y in clipped_poly_pixels:
                self.draw_pixel(x, y, color="purple")

    def _parse_vertices(self, entry):
        text = entry.get()
        points_str = re.findall(r'\(\s*(-?\d+)\s*,\s*(-?\d+)\s*\)', text)
        return [(int(x), int(y)) for x, y in points_str]

    def apply_translation(self):
        try:
            vertices = self._parse_vertices(self.transform_poly_entry)
            dx, dy = [int(v) for v in self.trans_entry.get().split(",")]
        except Exception:
            messagebox.showerror("Erro", "Verifique os valores de entrada para translação.")
            return
        self.clear_canvas()
        # Desenha original em cinza
        for x, y in draw_polyline(vertices + [vertices[0]]):
            self.draw_pixel(x, y, color="lightgrey")
        # Aplica e desenha transformado
        new_vertices = translacao(vertices, dx, dy)
        for x, y in draw_polyline(new_vertices + [new_vertices[0]]):
            self.draw_pixel(x, y, color="red")

    def apply_rotation(self):
        try:
            vertices = self._parse_vertices(self.transform_poly_entry)
            ang, px, py = [float(v) for v in self.rot_entry.get().split(",")]
        except Exception:
            messagebox.showerror("Erro", "Verifique os valores de entrada para rotação.")
            return
        self.clear_canvas()
        for x, y in draw_polyline(vertices + [vertices[0]]):
            self.draw_pixel(x, y, color="lightgrey")
        new_vertices = rotacao(vertices, ang, (px, py))
        for x, y in draw_polyline(new_vertices + [new_vertices[0]]):
            self.draw_pixel(x, y, color="blue")

    def apply_scale(self):
        try:
            vertices = self._parse_vertices(self.transform_poly_entry)
            sx, sy, fx, fy = [float(v) for v in self.scale_entry.get().split(",")]
        except Exception:
            messagebox.showerror("Erro", "Verifique os valores de entrada para escala.")
            return
        self.clear_canvas()
        for x, y in draw_polyline(vertices + [vertices[0]]):
            self.draw_pixel(x, y, color="lightgrey")
        new_vertices = escala(vertices, sx, sy, (fx, fy))
        for x, y in draw_polyline(new_vertices + [new_vertices[0]]):
            self.draw_pixel(x, y, color="green")