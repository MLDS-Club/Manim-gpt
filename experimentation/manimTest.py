# FOR MANUALLY RENDERING VIDEOS OUTPUTTED BY THE AGENT (JAMES)
# manim manimTest.py -ql -p

from manim import *

class CircleArea(Scene):
    def construct(self):
        # Define the radius
        radius = 3

        # Create the circle
        circle = Circle(radius=radius)
        circle.set_fill(BLUE, opacity=0.5)  # Fill with blue color and set opacity

        # Create the radius line
        radius_line = Line(ORIGIN, circle.get_right())
        radius_label = MathTex("r = 3").next_to(radius_line, UP)

        # Display the circle and radius
        self.play(Create(circle))
        self.play(Create(radius_line), Write(radius_label))


        # Formula for the area of a circle
        area_formula = MathTex("A = \\pi r^2")
        area_formula.to_edge(UP)
        self.play(Write(area_formula))
        self.wait(1)

        # Substitute the value of r
        substituted_formula = MathTex("A = \\pi (3)^2")
        substituted_formula.next_to(area_formula, DOWN)
        self.play(TransformMatchingTex(area_formula.copy(), substituted_formula))
        self.wait(1)

        # Calculate the area
        calculated_area = MathTex("A = 9\\pi")
        calculated_area.next_to(substituted_formula, DOWN)
        self.play(TransformMatchingTex(substituted_formula.copy(), calculated_area))
        self.wait(1)

        # Show numerical approximation
        approx_area = MathTex("A \\approx 28.27")  # Using PI from manim
        approx_area.next_to(calculated_area, DOWN)
        self.play(TransformMatchingTex(calculated_area.copy(), approx_area))
        self.wait(1)
        self.play(FadeOut(radius_line), FadeOut(radius_label))

        # Display area value on the circle
        area_text = Text(f"Area = {round(PI * radius**2, 2)}").scale(0.8)
        area_text.move_to(circle.get_center())

        self.play(Write(area_text))
        self.wait(2)