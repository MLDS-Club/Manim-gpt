from manim import *

class SquareRoot(Scene):
    def construct(self):
        # Create a text object for the question
        question = Text("What is the square root of 64?")
        self.play(Write(question))
        self.wait(2)

        # Create a square to represent 64
        square = Square(side_length=8)
        square.set_fill(BLUE, opacity=0.5)
        self.play(Create(square))
        self.wait(1)

        # Add text to indicate the area of the square
        area_text = Text("Area = 64").next_to(square, DOWN)
        self.play(Write(area_text))
        self.wait(1)

        # Explain the concept of square root
        explain_text = Text("Square root is the side length").next_to(area_text, DOWN)
        self.play(Write(explain_text))
        self.wait(2)

        # Show side length
        side_length_text = MathTex("8").next_to(square, RIGHT) # Use MathTex for numbers
        self.play(Write(side_length_text))
        self.wait(1)

        # Show the answer
        answer_text = MathTex(r"\sqrt{64} = 8")
        self.play(Transform(question, answer_text))
        self.wait(2)

        self.play(FadeOut(square),FadeOut(area_text), FadeOut(explain_text), FadeOut(side_length_text))
        self.wait(2)