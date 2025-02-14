from manim import *

class RightTriangle(Scene):
    def construct(self):
        # Create a right triangle
        triangle = Polygon(ORIGIN, [4, 0, 0], [0, 3, 0], color=BLUE)
        self.play(Create(triangle))

        # Label the legs
        leg1_label = MathTex("3").next_to(triangle.get_bottom(), DOWN)
        leg2_label = MathTex("4").next_to(triangle.get_left(), LEFT)
        self.play(Write(leg1_label), Write(leg2_label))

        # Calculate the hypotenuse using the Pythagorean theorem
        hypotenuse_length = (3**2 + 4**2)**0.5

        # Label the hypotenuse
        hypotenuse_label = MathTex(str(hypotenuse_length)).move_to([2,1.5,0])
        self.play(Write(hypotenuse_label))
        self.wait(2)

        # Display the Pythagorean theorem
        theorem = MathTex("a^2 + b^2 = c^2").to_edge(UP)
        self.play(Write(theorem))
        self.wait(1)

        # Substitute values and solve
        substitution = MathTex("3^2 + 4^2 = c^2").next_to(theorem, DOWN)
        self.play(Write(substitution))
        self.wait(1)

        calculation = MathTex("9 + 16 = c^2").next_to(substitution, DOWN)
        self.play(Write(calculation))
        self.wait(1)

        result = MathTex("25 = c^2").next_to(calculation, DOWN)
        self.play(Write(result))
        self.wait(1)

        final_result = MathTex("c = 5").next_to(result, DOWN)
        self.play(Write(final_result))
        self.wait(2)