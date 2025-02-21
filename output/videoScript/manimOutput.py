python
from manim import *

class CircleArea(Scene):
    def construct(self):
        # Define the radius
        radius = 3

        # Create the circle
        circle = Circle(radius=radius)
        circle.set_fill(BLUE, opacity=0.5)
        self.play(Create(circle))

        # Show the radius
        radius_line = Line(circle.get_center(), circle.get_right())
        radius_label = MathTex("r = 3").next_to(radius_line, RIGHT)
        self.play(Create(radius_line), Write(radius_label))
        self.wait(1)

        # Calculate the area
        area = PI * radius**2

        # Display the formula
        formula = MathTex("Area = \\pi r^2").to_edge(UP)
        self.play(Write(formula))
        self.wait(1)

        # Substitute the value of r
        substitution = MathTex("Area = \\pi (3)^2").next_to(formula, DOWN)
        self.play(Write(substitution))
        self.wait(1)

        # Show the result
        result = MathTex(f"Area = {area:.2f}").next_to(substitution, DOWN)
        self.play(Write(result))
        self.wait(2)

        # Fill the circle to represent the area
        self.play(circle.animate.set_fill(BLUE, opacity=0.8))
        self.wait(2)