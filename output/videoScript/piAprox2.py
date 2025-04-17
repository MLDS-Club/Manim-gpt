from manim import *
import random
import numpy as np

class WingLiftScene(Scene):
    def construct(self):
        # Randomly generate parameters
        random.seed(42)
        rho = 1.225  # air density (kg/m^3)
        mph_to_mps = 0.44704
        V = 500 * mph_to_mps  # converting to m/s
        k_top = random.uniform(1.05, 1.15)
        k_bottom = random.uniform(0.85, 0.95)
        V_top = V * k_top
        V_bottom = V * k_bottom
        wing_area = random.uniform(20, 30)  # m^2
        delta_p = 0.5 * rho * (V_bottom**2 - V_top**2)
        F = delta_p * wing_area

        # Wing shape via polygon
        upper = [(-3, 0), (-2.5, 0.1), (-1, 0.15), (0, 0.12), (1, 0.1), (2.5, 0.05), (3, 0)]
        lower = [(3, 0), (2.5, -0.05), (1, -0.1), (0, -0.08), (-1, -0.1), (-2.5, -0.07), (-3, 0)]
        points = [np.array([x, y, 0]) for x, y in upper + lower]
        wing = Polygon(*points, color=GRAY, fill_color=GRAY, fill_opacity=1)
        wing.scale(0.8).shift(2 * RIGHT)

        # Vector field for streamlines
        def flow_field(pos):
            return RIGHT * (V_top if pos[1] > 0 else V_bottom)

        stream_lines = StreamLines(
            flow_field,
            x_range=[-6, 6, 1],
            y_range=[-3, 3, 1],
            stroke_width=2,
            max_anchors_per_line=30,
            virtual_time=3,
            padding=1,
        )

        # Bernoulli equation
        eq1 = MathTex("p + \\tfrac12 \\rho V^2 = \\mathrm{constant}").to_corner(UR)
        eq2 = MathTex(
            "\\Delta p = p_{\\text{bottom}} - p_{\\text{top}}",
            "= \\tfrac12 \\rho (V_{\\text{bottom}}^2 - V_{\\text{top}}^2)"
        ).next_to(eq1, DOWN)

        # Numeric substitution steps
        line1 = MathTex(f"\\rho = {rho:.3f}\\,\\mathrm{{kg/m^3}}").to_corner(UL)
        line2 = MathTex(
            f"V = 500\\,\\mathrm{{mph}} = 500 \\times 0.44704 = {V:.1f}\\,\\mathrm{{m/s}}"
        ).next_to(line1, DOWN)
        line3 = MathTex(
            f"V_{{\\text{{top}}}} = k_{{\\text{{top}}}} V = {k_top:.2f} \\times {V:.1f} = {V_top:.1f}\\,\\mathrm{{m/s}}"
        ).next_to(line2, DOWN)
        line4 = MathTex(
            f"V_{{\\text{{bottom}}}} = k_{{\\text{{bottom}}}} V = {k_bottom:.2f} \\times {V:.1f} = {V_bottom:.1f}\\,\\mathrm{{m/s}}"
        ).next_to(line3, DOWN)
        line5 = MathTex(
            f"\\Delta p = 0.5 \\times {rho:.3f} \\times ({V_bottom:.1f}^2 - {V_top:.1f}^2) = {delta_p:.1f}\\,\\mathrm{{Pa}}"
        ).next_to(line4, DOWN)
        line6 = MathTex(
            f"F = \\Delta p \\times S = {delta_p:.1f} \\times {wing_area:.1f} = {F:.1f}\\,\\mathrm{{N}}"
        ).next_to(line5, DOWN)

        # Render scene
        self.add(stream_lines, wing)
        self.play(stream_lines.create(), run_time=3)
        self.wait(1)
        self.play(Write(eq1), run_time=1)
        self.wait(1)
        self.play(Write(eq2), run_time=1)
        self.wait(1)
        for line in [line1, line2, line3, line4, line5, line6]:
            self.play(FadeIn(line, shift=DOWN), run_time=1)
            self.wait(1)
        self.wait(2)