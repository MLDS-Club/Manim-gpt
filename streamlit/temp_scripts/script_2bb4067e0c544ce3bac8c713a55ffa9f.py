from manim import *
import numpy as np

class CameraLightProcessScene(Scene):
    def construct(self):
        # Title
        title = Tex("How a Camera Captures Light", font_size=48).to_edge(UP)
        self.play(Write(title), run_time=2)
        self.wait(1)

        # Optical geometry constants
        d_o = 10        # object distance
        f = 4           # focal length
        d_i = 20/3      # image distance from lens
        h_o = 2         # object height
        h_i = -d_i / d_o * h_o  # image height by magnification

        # Draw lens
        lens = Line(UP * 3, DOWN * 3, color=BLUE)
        lens_label = MathTex("Lens", color=BLUE).next_to(lens, UP)
        self.play(Create(lens), Write(lens_label))
        self.wait(1)

        # Draw object arrow
        obj_top = np.array([-d_o,  h_o/2, 0])
        obj_bot = np.array([-d_o, -h_o/2, 0])
        obj_arrow = Arrow(obj_bot, obj_top, buff=0, color=GREEN)
        obj_label = MathTex("Object", color=GREEN).next_to(obj_arrow, LEFT)
        self.play(Create(obj_arrow), Write(obj_label))
        self.wait(1)

        # Label d_o and h_o
        brace_do = BraceBetweenPoints(obj_arrow.get_center(), lens.get_center(), direction=DOWN)
        label_do = brace_do.get_tex(r"d_o = 10")
        brace_ho = BraceBetweenPoints(obj_top, obj_bot, direction=LEFT)
        label_ho = brace_ho.get_tex(r"h_o = 2")
        self.play(Create(brace_do), Write(label_do))
        self.play(Create(brace_ho), Write(label_ho))
        self.wait(1)

        # Draw image arrow
        img_top = np.array([ d_i,  h_i/2, 0])
        img_bot = np.array([ d_i, -h_i/2, 0])
        img_arrow = Arrow(img_top, img_bot, buff=0, color=RED)
        img_label = MathTex("Image", color=RED).next_to(img_arrow, RIGHT)
        self.play(Create(img_arrow), Write(img_label))
        self.wait(1)

        # Label d_i and h_i
        brace_di = BraceBetweenPoints(lens.get_center(), img_arrow.get_center(), direction=UP)
        label_di = brace_di.get_tex(r"d_i = \tfrac{20}{3}\approx6.67")
        brace_hi = BraceBetweenPoints(img_top, img_bot, direction=RIGHT)
        label_hi = brace_hi.get_tex(r"h_i = -\tfrac{4}{3}\approx-1.33")
        self.play(Create(brace_di), Write(label_di))
        self.play(Create(brace_hi), Write(label_hi))
        self.wait(2)

        # Ray diagrams
        # 1) Ray parallel to axis then through focal point
        p1_start = obj_top
        p1_mid   = np.array([0,  h_o/2, 0])
        p1_end   = img_top
        ray1a = Line(p1_start, p1_mid, color=YELLOW)
        ray1b = Line(p1_mid, p1_end, color=YELLOW)
        self.play(Create(ray1a), Create(ray1b), run_time=2)
        self.wait(0.5)
        # 2) Ray through lens center (undeviated)
        ray2 = Line(obj_top, img_top, color=YELLOW)
        self.play(Create(ray2), run_time=2)
        self.wait(2)

        # Lens formula derivation
        eq1 = MathTex(r"\frac{1}{d_o} + \frac{1}{d_i} = \frac{1}{f}", font_size=36).to_corner(UL)
        eq2 = MathTex(r"\frac{1}{10} + \frac{1}{d_i} = \frac{1}{4}", font_size=32).next_to(eq1, DOWN, aligned_edge=LEFT)
        eq3 = MathTex(r"\frac{1}{d_i} = \frac{1}{4} - \frac{1}{10} = \frac{3}{20}", font_size=32).next_to(eq2, DOWN, aligned_edge=LEFT)
        eq4 = MathTex(r"d_i = \frac{20}{3}\approx6.67", font_size=32).next_to(eq3, DOWN, aligned_edge=LEFT)
        self.play(Write(eq1))
        self.play(Write(eq2))
        self.play(Write(eq3))
        self.play(Write(eq4))
        self.wait(2)

        # Sensor (image plane) & pixel grid
        sensor = Line(UP*3, DOWN*3, color=GREY).shift(RIGHT * d_i)
        self.play(Create(sensor))
        self.wait(1)

        cols, rows = 5, 3
        cell_w, cell_h = 0.5, 1.0
        left = d_i - cols*cell_w/2
        top  = rows*cell_h/2
        grid = VGroup()
        for i in range(cols+1):
            x = left + i*cell_w
            grid.add(Line([x, top, 0], [x, top-rows*cell_h, 0], color=GREY))
        for j in range(rows+1):
            y = top - j*cell_h
            grid.add(Line([left, y, 0], [left+cols*cell_w, y, 0], color=GREY))
        self.play(Create(grid), run_time=2)
        self.wait(1)

        # Fill pixels by light intensity
        intensities = [
            [0.2, 0.5, 0.8, 0.5, 0.2],
            [0.5, 0.9, 1.0, 0.9, 0.5],
            [0.2, 0.5, 0.8, 0.5, 0.2],
        ]
        pixels = VGroup()
        for i in range(cols):
            for j in range(rows):
                rect = Rectangle(width=cell_w, height=cell_h, color=GREY)
                rect.set_fill(WHITE, opacity=intensities[j][i])
                cx = left + (i+0.5)*cell_w
                cy = top  - (j+0.5)*cell_h
                rect.move_to([cx, cy, 0])
                pixels.add(rect)
        self.play(FadeIn(pixels), run_time=2)
        self.wait(2)

        # Show resulting digital matrix
        matrix = MathTex(
            r"\begin{bmatrix}"
            r"0.2 & 0.5 & 0.8 & 0.5 & 0.2 \\"
            r"0.5 & 0.9 & 1.0 & 0.9 & 0.5 \\"
            r"0.2 & 0.5 & 0.8 & 0.5 & 0.2"
            r"\end{bmatrix}", font_size=24
        ).next_to(grid, DOWN, buff=1)
        self.play(Write(matrix))
        self.wait(2)