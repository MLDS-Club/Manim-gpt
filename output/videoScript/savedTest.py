from manim import *

class CubeRootOf64(Scene):
    def construct(self):
        # Introduction
        title = Text("Cube Root of 64").scale(1.5)
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))

        # Show the number 64
        number_64 = MathTex("64").scale(2)
        self.play(Write(number_64))
        self.wait(1)

        # Explain cube root concept
        cube_root_explanation = Tex("What number, when multiplied by itself three times, equals 64?").scale(0.7)
        cube_root_explanation.next_to(number_64, DOWN)
        self.play(Write(cube_root_explanation))
        self.wait(2)
        self.play(FadeOut(cube_root_explanation))

        # Show the cube root symbol and 64
        cube_root_expression = MathTex("\\sqrt[3]{64}").scale(2)
        self.play(Transform(number_64, cube_root_expression))
        self.wait(1)

        # Start with a smaller number: 2
        number_2 = MathTex("2").scale(1.5)
        self.play(Write(number_2))
        self.wait(0.5)
        
        # Show 2*2*2
        multiply_1 = MathTex("2 \\times 2 \\times 2").scale(1.5)
        self.play(Transform(number_2, multiply_1))
        self.wait(1)
        
        result_8 = MathTex("8").scale(1.5)
        self.play(Transform(number_2, result_8))
        self.wait(1)
        self.play(FadeOut(number_2))

        # Try 4
        number_4 = MathTex("4").scale(1.5)
        self.play(Write(number_4))
        self.wait(0.5)

        # Show 4*4*4
        multiply_2 = MathTex("4 \\times 4 \\times 4").scale(1.5)
        self.play(Transform(number_4, multiply_2))
        self.wait(1)

        # Show the result
        result_64 = MathTex("64").scale(1.5)
        self.play(Transform(number_4, result_64))
        self.wait(1)

        # Highlight the solution
        self.play(Indicate(number_4))
        self.wait(1)

        # Show the final answer with cube root
        final_answer = MathTex("\\sqrt[3]{64} = 4").scale(2)
        self.play(Transform(number_64, final_answer))
        self.wait(2)
        self.play(FadeOut(number_4), FadeOut(number_64))