from manim import *
import random

class WingLiftScene(Scene):
    def construct(self):
        # Randomly generate parameters
        rho = 1.225  # Air density (kg/m^3)
        V = 500 * 0.44704  # Convert 500 mph to m/s
        S = random.uniform(10, 30)  # Wing area in m^2
        Cl = random.uniform(0.5, 1.5)  # Lift coefficient
        # Compute lift
        L = 0.5 * rho * V**2 * S * Cl
        # Rounded display values
        V_disp = round(V, 1)
        S_disp = round(S, 2)
        Cl_disp = round(Cl, 2)
        L_disp = round(L, 1)

        # Display parameter text
        text1 = Text(f"V = {V_disp} m/s, S = {S_disp} m², Cl = {Cl_disp}", font_size=24)
        text1.to_edge(UP)

        # Wing representation
        wing = RoundedRectangle(corner_radius=0.2, width=4, height=0.4, fill_color=GREY, fill_opacity=1)
        wing.rotate(10 * DEGREES)

        # Flow lines
        ys = [-1.0, -0.5, 0.5, 1.0]
        lines = VGroup(*[
            Line(start=LEFT * 6 + UP * y, end=RIGHT * 6 + UP * y, stroke_opacity=0.7)
            for y in ys
        ])
        # Dots moving with flow
        dots = VGroup(*[
            Dot(point=LEFT * 6 + UP * y, color=BLUE)
            for y in ys
        ])

        # Pressure arrows
        arrow_high = Arrow(
            start=wing.get_bottom() + DOWN * 0.1,
            end=wing.get_bottom() + UP * 1.0,
            buff=0,
            color=YELLOW
        )
        arrow_low = Arrow(
            start=wing.get_top() + UP * 0.1,
            end=wing.get_top() + DOWN * 0.4,
            buff=0,
            color=YELLOW
        )

        # Lift text
        text2 = Text(f"Lift = {L_disp} N", font_size=32)
        text2.next_to(wing, DOWN)

        # Add objects
        self.add(text1, wing, lines, dots)
        self.wait(1)

        # Animate flow dots
        animations = []
        for dot, y in zip(dots, ys):
            run_time = 3 if y > 0 else 4
            path = Line(start=LEFT * 6 + UP * y, end=RIGHT * 6 + UP * y)
            animations.append(
                MoveAlongPath(dot, path, rate_func=linear, run_time=run_time)
            )
        self.play(*animations)
        self.wait(0.5)

        # Show pressure arrows
        self.play(GrowArrow(arrow_high), GrowArrow(arrow_low))
        self.wait(0.5)

        # Display lift value
        self.play(Write(text2))
        self.wait(2)