from manim import *
import numpy as np

class WeightDistributionScene(Scene):
    def construct(self):
        # Title
        title = Text("Weight Distribution & Lift for Takeoff", font_size=36)
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.to_edge(UP))
        self.wait(0.5)

        # Stylized airplane silhouette
        fuselage = Line(LEFT * 1, RIGHT * 1).shift(UP * 1)
        left_wing = Line(ORIGIN, RIGHT * 1.5).rotate(30 * DEGREES).shift(UP * 1)
        right_wing = Line(ORIGIN, LEFT * 1.5).rotate(-30 * DEGREES).shift(UP * 1)
        plane = VGroup(fuselage, left_wing, right_wing).set_color(GRAY)
        self.play(Create(plane), run_time=2)
        self.wait(1)

        # Weight arrow at center of gravity
        weight_arrow = Arrow(start=UP * 1.2, end=UP * 0.8, buff=0, color=RED)
        weight_label = MathTex("W", font_size=24, color=RED).next_to(weight_arrow, UP)
        self.play(GrowArrow(weight_arrow), Write(weight_label))
        self.wait(1)

        # Axes for lift distribution
        axes = Axes(
            x_range=[-1.5, 1.5, 0.5],
            y_range=[0, 1.5, 0.5],
            x_length=5,
            y_length=3,
            axis_config={"include_tip": False, "stroke_color": WHITE},
        ).to_corner(DL)
        # Axis labels manually positioned
        x_label = MathTex("x", font_size=24).next_to(axes.x_axis, RIGHT, buff=0.1)
        y_label = MathTex("L(x)", font_size=24).next_to(axes.y_axis, UP, buff=0.1)
        self.play(Create(axes), Write(VGroup(x_label, y_label)))
        self.wait(1)

        # Plot lift distribution: elliptical
        a = 1.5
        def L(x):
            return np.sqrt(np.maximum(0, 1 - (x / a) ** 2))
        lift_curve = axes.plot(lambda x: L(x), x_range=[-a, a], color=BLUE)
        self.play(Create(lift_curve), run_time=2)
        self.wait(1)

        # Display integral for total lift = weight
        integral_eq = MathTex(
            r"W = \int_{-a}^{a} L(x)\,dx",
            font_size=28,
        ).to_corner(DR, buff=0.5)
        self.play(Write(integral_eq))
        self.wait(2)

        # Show center of gravity formula
        cog_eq = MathTex(
            r"x_{CG} = \frac{1}{W} \int_{-a}^{a} x\,L(x)\,dx",
            font_size=28,
        ).next_to(integral_eq, UP, aligned_edge=RIGHT, buff=0.3)
        self.play(Write(cog_eq))
        self.wait(2)

        # Clean up
        self.play(FadeOut(VGroup(plane, weight_arrow, weight_label, axes, lift_curve, integral_eq, cog_eq, title)))
        self.wait(1)