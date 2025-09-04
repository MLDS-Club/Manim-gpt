from manim import *

class WingLiftScene(Scene):
    def construct(self):
        # Draw wing cross‐section
        top_pts = [
            [-3, 0, 0],
            [-1, 0.5, 0],
            [1, 0.5, 0],
            [3, 0, 0],
        ]
        bottom_pts = [
            [3, 0, 0],
            [1, -0.2, 0],
            [-1, -0.2, 0],
            [-3, 0, 0],
        ]
        top_curve = VMobject().set_points_as_cubic_bezier(top_pts)
        bottom_curve = VMobject().set_points_as_cubic_bezier(bottom_pts)
        wing = VGroup(top_curve, bottom_curve)
        wing.set_fill(GRAY, opacity=1).set_stroke(BLACK, 2)
        self.play(Create(wing), run_time=2)
        self.wait(0.5)

        # Add streamlines
        y_vals = [0.8, 0.4, -0.4, -0.8]
        lines = VGroup(*[
            Line([-4, y, 0], [4, y, 0], color=BLUE, stroke_width=1)
            for y in y_vals
        ])
        self.play(LaggedStartMap(Create, lines, lag_ratio=0.2), run_time=2)
        self.wait(0.5)

        # Animate particles on top & bottom
        dot_top = Dot(color=YELLOW).move_to(lines[0].get_start())
        dot_bot = Dot(color=YELLOW).move_to(lines[-1].get_start())
        self.add(dot_top, dot_bot)
        self.play(
            MoveAlongPath(dot_top, lines[0], rate_func=linear),
            run_time=3
        )
        self.play(
            MoveAlongPath(dot_bot, lines[-1], rate_func=linear),
            run_time=5
        )
        self.wait(0.5)

        # Show velocity inequality
        v_tex = MathTex(r"v_{\mathrm{top}} > v_{\mathrm{bottom}}", font_size=36)
        v_tex.to_corner(UR)
        self.play(Write(v_tex), run_time=1)
        self.wait(0.5)

        # Bernoulli's equation
        eqn = MathTex(r"P + \tfrac12 \rho v^2 = \text{constant}", font_size=36)
        eqn.to_edge(LEFT, buff=1)
        self.play(Write(eqn), run_time=1)
        self.wait(0.5)

        # Substitution step
        step1 = MathTex(
            r"P_{\mathrm{up}} + \tfrac12 \rho (50)^2 = "
            r"P_{\mathrm{low}} + \tfrac12 \rho (30)^2",
            font_size=30
        ).next_to(eqn, DOWN, buff=0.4)
        self.play(Write(step1), run_time=1)
        self.wait(0.5)

        # Pressure difference derivation
        step2 = MathTex(
            r"\Delta P = P_{\mathrm{low}} - P_{\mathrm{up}} "
            r"= \tfrac12 \rho \bigl(50^2 - 30^2\bigr)",
            font_size=30
        ).next_to(step1, DOWN, buff=0.4)
        self.play(Write(step2), run_time=1)
        self.wait(0.5)

        # Numeric evaluation
        step3 = MathTex(
            r"= \tfrac12 \,(1.225)\,(2500 - 900) = 980~\mathrm{Pa}",
            font_size=30
        ).next_to(step2, DOWN, buff=0.4)
        self.play(Write(step3), run_time=1)
        self.wait(0.5)

        # Lift arrow and formula
        top_point = wing.get_top() + UP*0.1
        arrow = Arrow(start=top_point, end=top_point + UP*1.2, color=RED)
        formula = MathTex(r"F_L = \Delta P \times A", font_size=36)
        formula.next_to(arrow, UP, buff=0.2)
        self.play(GrowArrow(arrow), Write(formula), run_time=1)
        self.wait(1)