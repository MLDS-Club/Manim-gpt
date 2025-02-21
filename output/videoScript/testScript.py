from manim import *

class CircleArea(Scene):
    def construct(self):
        # Create a circle with radius 3
        radius = 3
        circle = Circle(radius=radius)
        circle.set_fill(BLUE, opacity=0.5)
        self.play(Create(circle))

        # Display the radius
        radius_line = Line(ORIGIN, circle.get_right())
        radius_label = MathTex("r = 3").next_to(radius_line, UP)
        self.play(
            Create(radius_line),
            Write(radius_label)
        )
        self.wait(1)

        # Display the area formula
        area_formula = MathTex("A = \\pi r^2").to_edge(UP)
        self.play(Write(area_formula))
        self.wait(1)

        # Substitute the radius value
        substituted_formula = MathTex("A = \\pi (3)^2").next_to(area_formula, DOWN)
        self.play(Write(substituted_formula))
        self.wait(1)

        # Calculate and display the area
        area_value = MathTex("A = 9\\pi").next_to(substituted_formula, DOWN)
        self.play(Write(area_value))
        self.wait(1)

        # Show numerical approximation
        approx_value = MathTex("A \\approx 28.27").next_to(area_value, DOWN)
        self.play(Write(approx_value))
        self.wait(1)

        self.play(
            FadeOut(radius_line),
            FadeOut(radius_label),
            FadeOut(area_formula),
            FadeOut(substituted_formula),
            FadeOut(area_value),
            FadeOut(approx_value)
        )
        self.wait(1)