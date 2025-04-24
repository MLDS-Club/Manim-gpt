from manim import *
import numpy as np


class PythagoreanTheoremWalkthrough(Scene):
    def construct(self):
        # -----------------------------------------------------------
        # 1) Title
        # -----------------------------------------------------------
        title = Tex("The Pythagorean Theorem", color=YELLOW).to_edge(UP)
        self.play(Write(title), run_time=2)
        self.wait(0.5)

        # -----------------------------------------------------------
        # 2) Build a 3‑4‑5 right‑triangle
        # -----------------------------------------------------------
        A = np.array([0, 0, 0])     # Right‑angle vertex
        B = np.array([4, 0, 0])     # Horizontal leg end  (b = 4)
        C = np.array([0, 3, 0])     # Vertical   leg end  (a = 3)

        triangle = Polygon(A, B, C, stroke_color=WHITE)
        self.play(Create(triangle), run_time=1)

        # Right‑angle marker
        ra_marker = VGroup(
            Line(A + 0.4 * RIGHT, A + 0.4 * RIGHT + 0.4 * UP),
            Line(A + 0.4 * UP, A + 0.4 * RIGHT + 0.4 * UP),
            Line(A + 0.4 * RIGHT, A + 0.4 * UP),
        ).set_color(WHITE)
        self.play(Create(ra_marker), run_time=0.8)
        self.wait(0.3)

        # -----------------------------------------------------------
        # 3) Label the three sides
        # -----------------------------------------------------------
        side_a_lbl = MathTex("a = 3").next_to(Line(B, A), DOWN, buff=0.3)
        side_b_lbl = MathTex("b = 4").next_to(Line(A, C), LEFT, buff=0.3)
        side_c_lbl = MathTex("c = 5").next_to(Line(B, C), UP, buff=0.3)
        self.play(Write(side_a_lbl), Write(side_b_lbl), Write(side_c_lbl), lag_ratio=0.4)
        self.wait(0.5)

        # -----------------------------------------------------------
        # 4) Helper: build a square on a directed segment
        # -----------------------------------------------------------
        def square_on_edge(P, Q, color):
            """
            Build a square on the directed segment P→Q (external to triangle).
            """
            vec = Q - P
            length = np.linalg.norm(vec)
            # Perpendicular unit‑vector (+90° rotation)
            perp = np.array([-vec[1], vec[0], 0]) / np.linalg.norm(vec)
            perp *= length
            R = Q + perp
            S = P + perp
            return Polygon(P, Q, R, S, stroke_color=color, fill_color=color, fill_opacity=0.40)

        # Squares on each side
        square_a = square_on_edge(A, C, BLUE)
        square_b = square_on_edge(A, B, GREEN)
        square_c = square_on_edge(B, C, RED)

        # -----------------------------------------------------------
        # 5) Grow the three squares
        # -----------------------------------------------------------
        self.play(Create(square_a), run_time=1)
        self.play(Create(square_b), run_time=1)
        self.play(Create(square_c), run_time=1)
        self.wait(0.5)

        # -----------------------------------------------------------
        # 6) Display the area of each square
        # -----------------------------------------------------------
        area_a_lbl = MathTex("a^{2}=9").move_to(square_a.get_center())
        area_b_lbl = MathTex("b^{2}=16").move_to(square_b.get_center())
        area_c_lbl = MathTex("c^{2}=25").move_to(square_c.get_center())
        self.play(Write(area_a_lbl), Write(area_b_lbl), Write(area_c_lbl), lag_ratio=0.3)
        self.wait(1)

        # -----------------------------------------------------------
        # 7) State the theorem symbolically
        # -----------------------------------------------------------
        formula = MathTex("a^{2} + b^{2} = c^{2}").scale(1.3).to_edge(DOWN)
        self.play(Write(formula))
        self.wait(1)

        # -----------------------------------------------------------
        # 8) Substitute the concrete values
        # -----------------------------------------------------------
        numeric = MathTex("9 \\; + \\; 16 \\;=\\; 25").scale(1.3).move_to(formula)
        self.play(TransformMatchingTex(formula, numeric), run_time=1.5)
        self.wait(1.5)

        # -----------------------------------------------------------
        # 9) Final emphasis on the hypotenuse square
        # -----------------------------------------------------------
        self.play(Flash(square_c, color=YELLOW, run_time=1.2))
        self.wait(2)