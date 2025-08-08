from manim import *
import numpy as np

class SpiralConstructionScene(Scene):
    def construct(self):
        # 1) Title
        title = Text("Drawing an Archimedean Spiral", font_size=48).to_edge(UP)
        self.play(Write(title), run_time=2)
        self.wait(1)

        # 2) Show polar formula r = a + b·θ
        a_val, b_val = 0.5, 0.2
        polar_formula = MathTex("r", "=", "a", "+", "b", "\\theta", font_size=48)
        polar_formula.next_to(title, DOWN, buff=1)
        self.play(Write(polar_formula), run_time=2)
        self.wait(1)

        # 3) Label a and b values
        a_label = MathTex("a=0.5", color=YELLOW, font_size=36)
        b_label = MathTex("b=0.2", color=YELLOW, font_size=36)
        a_label.next_to(polar_formula[2], DOWN, buff=0.2)
        b_label.next_to(polar_formula[4], DOWN, buff=0.2)
        self.play(Write(a_label), Write(b_label), run_time=1.5)
        self.wait(1)

        # 4) Parametric equations
        param_x = MathTex(
            "x(\\theta)", "=", "r\\cos\\theta", "=", "(a+b\\theta)\\cos\\theta",
            font_size=36
        )
        param_y = MathTex(
            "y(\\theta)", "=", "r\\sin\\theta", "=", "(a+b\\theta)\\sin\\theta",
            font_size=36
        )
        param_x.next_to(polar_formula, DOWN, buff=1)
        param_y.next_to(param_x, DOWN, buff=0.5)
        self.play(Write(param_x), run_time=2)
        self.play(Write(param_y), run_time=2)
        self.wait(2)

        # 5) Clear intermediate formulas (keep title)
        clear_group = VGroup(polar_formula, a_label, b_label, param_x, param_y)
        self.play(FadeOut(clear_group), run_time=1)
        self.wait(1)

        # 6) Set up a theta ValueTracker for animation
        theta = ValueTracker(0)

        # 7) Define the spiral in Cartesian form
        def spiral_func(u):
            return np.array([
                (a_val + b_val * u) * np.cos(u),
                (a_val + b_val * u) * np.sin(u),
                0
            ])

        # 8) ParametricFunction that redraws up to current theta
        spiral = always_redraw(lambda: ParametricFunction(
            spiral_func,
            t_range=[0, theta.get_value()],
            color=BLUE,
            stroke_width=4
        ))

        # 9) Dot at the moving tip
        tip_dot = always_redraw(lambda: Dot(
            spiral_func(theta.get_value()), color=RED, radius=0.05
        ))

        # 10) Trace path behind the tip dot
        trace = TracedPath(
            tip_dot.get_center,
            stroke_color=YELLOW,
            stroke_width=2
        )

        # 11) Draw coordinate axes
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            axis_config={"include_numbers": True}
        ).set_height(8).set_width(8).to_edge(DOWN)
        self.play(Create(axes), run_time=2)

        # 12) Add spiral, dot, and trace
        self.add(trace)
        self.play(FadeIn(spiral), FadeIn(tip_dot), run_time=1)
        self.wait(1)

        # 13) Animate theta from 0 → 4·TAU (two full turns)
        self.play(theta.animate.set_value(4 * TAU),
                  run_time=8, rate_func=linear)
        self.wait(2)
```
This single `Scene` demonstrates:
1. The polar formula and parameter labels (a, b).
2. Conversion to Cartesian parametric form.
3. A live‐drawing spiral with a tip dot and its trace.
4. Clear, step‐by‐step annotations and smooth animation pacing.