from manim import *
import random

class LiftCalculation(Scene):
    def construct(self):
        # Generate random values
        A = random.uniform(20, 100)  # Wing area in m^2
        Cl = random.uniform(0.5, 1.5)  # Lift coefficient
        rho = 1.225  # Air density in kg/m^3
        v_mph = 500  # Wind speed in mph
        v = v_mph * 0.44704  # Convert mph to m/s
        lift = 0.5 * rho * v ** 2 * A * Cl  # Lift force in Newtons

        # Display the formula
        formula = MathTex(
            "F = \\frac12 \\rho v^2 A C_l"
        ).to_edge(UP)
        values = MathTex(
            f"\\rho = {rho:.3f}, \\quad v = {v:.2f}\\ \\mathrm{{m/s}},",
            f"A = {A:.2f}\\ \\mathrm{{m^2}}, \\quad C_l = {Cl:.2f}"
        ).next_to(formula, DOWN)
        result = MathTex(
            f"F = {lift:.2e}\\ \\mathrm{{N}}"
        ).next_to(values, DOWN)

        # Animate
        self.play(Write(formula))
        self.wait(1)
        self.play(Write(values))
        self.wait(1)
        self.play(Write(result))
        self.wait(2)