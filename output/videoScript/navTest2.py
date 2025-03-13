from manim import *

class OnePlusOne(Scene):
    def construct(self):
        # Create two Text objects representing the number 1
        one1 = Tex("1", font_size=144)
        one2 = Tex("1", font_size=144)

        # Position the first '1' on the left side of the screen
        one1.move_to(LEFT * 2)

        # Create a plus sign and position it next to the first '1'
        plus = Tex("+", font_size=144)
        plus.next_to(one1, RIGHT)

        # Position the second '1' next to the plus sign
        one2.next_to(plus, RIGHT)

        # Create an equals sign
        equals = Tex("=", font_size=144)
        equals.next_to(one2, RIGHT)

        # Create the answer '2' and position it next to the equals sign
        two = Tex("2", font_size=144)
        two.next_to(equals, RIGHT)

        # Display the first '1'
        self.play(Write(one1))
        self.wait(0.5)

        # Display the plus sign
        self.play(Write(plus))
        self.wait(0.5)

        # Display the second '1'
        self.play(Write(one2))
        self.wait(0.5)
        
        # Display the equals sign
        self.play(Write(equals))
        self.wait(0.5)

        # Display the answer '2'
        self.play(Write(two))
        self.wait(1)

        # Group all elements together
        group = VGroup(one1, plus, one2, equals, two)

        # Fade out the entire equation
        self.play(FadeOut(group))
        self.wait(1)