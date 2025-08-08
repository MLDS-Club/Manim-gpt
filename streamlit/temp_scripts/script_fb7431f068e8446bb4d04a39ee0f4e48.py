from manim import *
import numpy as np

class PolarIntegralScene(Scene):
    def construct(self):
        # Title
        title = Tex(r"Area enclosed by \(r = \sin(\theta)\)", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # Axes
        axes = Axes(
            x_range=[-1.5, 1.5, 0.5],
            y_range=[-0.5, 1.5, 0.5],
            axis_config={"include_tip": False},
        )
        axis_labels = axes.get_axis_labels(x_label="x", y_label="y")
        self.play(Create(axes), Write(axis_labels), run_time=2)
        self.wait(1)

        # Polar curve: r = sin(theta)
        polar_curve = ParametricFunction(
            lambda t: np.array([
                np.sin(t) * np.cos(t),
                np.sin(t) * np.sin(t),
                0
            ]),
            t_range=[0, PI],
            color=YELLOW
        )
        self.play(Create(polar_curve), run_time=2)
        self.wait(1)

        # Region shading approximation using polygon
        theta_vals = np.linspace(0, PI, 100)
        pts = [np.array([np.sin(t)*np.cos(t), np.sin(t)*np.sin(t), 0]) for t in theta_vals]
        region_pts = [ORIGIN, *pts, ORIGIN]
        region = Polygon(*region_pts, color=BLUE, fill_opacity=0.5, stroke_width=0)
        self.play(FadeIn(region), run_time=2)
        self.wait(1)

        # Step-by-step derivation
        eq1 = MathTex(r"A = \tfrac{1}{2} \int_{0}^{\pi} r^2 \, d\theta") \
              .scale(0.7).to_corner(UL)
        eq2 = MathTex(r"= \tfrac{1}{2} \int_{0}^{\pi} \sin^2 \theta \, d\theta") \
              .scale(0.7).next_to(eq1, DOWN, aligned_edge=LEFT)
        eq3 = MathTex(r"= \tfrac{1}{2} \int_{0}^{\pi} \tfrac{1 - \cos(2\theta)}{2} \, d\theta") \
              .scale(0.7).next_to(eq2, DOWN, aligned_edge=LEFT)
        eq4 = MathTex(r"= \tfrac{1}{4} \int_{0}^{\pi} (1 - \cos(2\theta)) \, d\theta") \
              .scale(0.7).next_to(eq3, DOWN, aligned_edge=LEFT)
        eq5 = MathTex(r"= \tfrac{1}{4} \Bigl[ \theta - \tfrac{\sin(2\theta)}{2} \Bigr]_{0}^{\pi}") \
              .scale(0.7).next_to(eq4, DOWN, aligned_edge=LEFT)
        eq6 = MathTex(r"= \tfrac{1}{4} (\pi - 0) = \tfrac{\pi}{4}") \
              .scale(0.7).next_to(eq5, DOWN, aligned_edge=LEFT)

        for eq in [eq1, eq2, eq3, eq4, eq5, eq6]:
            self.play(Write(eq), run_time=1)
            self.wait(1)

        self.wait(2)