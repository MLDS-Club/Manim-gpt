from manim import *
import numpy as np

class SineAreaRightRiemannScene(Scene):
    def construct(self):
        # Title
        title = Text("Area under $y=\\sin(x)$ from $0$ to $\\pi$") \
            .scale(0.7) \
            .to_edge(UP)
        self.play(Write(title), run_time=2)
        self.wait(1)

        # Axes and sine curve
        axes = Axes(
            x_range=[0, PI, PI/4],
            y_range=[0, 1.5, 0.5],
            x_length=6,
            y_length=3,
            tips=False
        ).to_edge(DOWN)
        ax_labels = axes.get_axis_labels(x_label="x", y_label="y")
        sine_curve = axes.plot(lambda x: np.sin(x), color=YELLOW)
        sine_label = MathTex("y=\\sin(x)").next_to(sine_curve, UP)
        self.play(Create(axes), Write(ax_labels))
        self.play(Create(sine_curve), Write(sine_label), run_time=2)
        self.wait(1)

        # Show integral formula
        integral = MathTex(r"A = \int_0^\pi \sin(x)\,dx") \
            .to_edge(UL)
        self.play(Write(integral), run_time=2)
        self.wait(1)

        # Show delta x formula
        dx_formula = MathTex(r"\Delta x = \frac{\pi - 0}{n} = \frac{\pi}{n}")
        dx_formula.next_to(integral, DOWN, aligned_edge=LEFT)
        self.play(Write(dx_formula), run_time=2)
        self.wait(1)

        # Partition and rectangles for n=6
        n = 6
        dx = PI / n
        rects = VGroup()
        for i in range(1, n+1):
            x_left = (i - 1) * dx
            x_right = i * dx
            height = np.sin(i * dx)
            rect = Rectangle(
                width=dx,
                height=height,
                stroke_width=1,
                stroke_color=WHITE,
                fill_color=BLUE,
                fill_opacity=0.5
            )
            # Position rectangle at correct location
            mid_x = (x_left + x_right) / 2
            rect.move_to(axes.coords_to_point(mid_x, height / 2))
            rects.add(rect)
        self.play(LaggedStart(*[Create(r) for r in rects], lag_ratio=0.3), run_time=3)
        self.wait(1)

        # Show Riemann sum formula
        sum_formula = MathTex(
            r"R_n = \sum_{i=1}^{n} \sin\bigl(i\Delta x\bigr)\,\Delta x"
        )
        sum_formula.next_to(dx_formula, DOWN, aligned_edge=LEFT)
        self.play(Write(sum_formula), run_time=2)
        self.wait(1)

        # Show limit as n->infinity
        limit = MathTex(r"A = \lim_{n \to \infty} R_n = 2") \
            .to_edge(DR)
        self.play(Write(limit), run_time=2)
        self.wait(2)