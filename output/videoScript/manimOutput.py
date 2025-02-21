from manim import *

class Addition(Scene):
    def construct(self):
        # Create the text objects
        text1 = Tex("1")
        text2 = Tex("+")
        text3 = Tex("4")
        text4 = Tex("=")
        text5 = Tex("5")

        # Position the text objects
        text1.move_to(LEFT * 2)
        text2.next_to(text1, RIGHT)
        text3.next_to(text2, RIGHT)
        text4.next_to(text3, RIGHT)
        text5.next_to(text4, RIGHT)

        # Add the text objects to the scene
        self.play(Write(text1))
        self.wait(0.5)
        self.play(Write(text2))
        self.wait(0.5)
        self.play(Write(text3))
        self.wait(0.5)
        self.play(Write(text4))
        self.wait(0.5)
        self.play(Write(text5))
        self.wait(1)

        # Group text1, text2, and text3
        group = VGroup(text1, text2, text3)

        # Create five dots
        dots = VGroup(*[Dot() for _ in range(5)])
        dots.arrange(RIGHT)
        dots.next_to(group, DOWN)

        # Show 1 dot
        self.play(Create(dots[0]))
        self.wait(0.5)

        # Show 4 dots
        self.play(Create(dots[1:5]))
        self.wait(1)

        # Highlight all 5 dots and the answer
        self.play(Indicate(dots), Indicate(text5))
        self.wait(2)