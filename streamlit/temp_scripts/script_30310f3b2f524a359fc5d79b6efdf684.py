from manim import *

class LongDivisionScene(Scene):
    def construct(self):
        # Display long division setup: 6 ) 234
        divisor = MathTex("6")
        bracket = MathTex(r"\big)")
        d2 = MathTex("2")
        d3 = MathTex("3")
        d4 = MathTex("4")
        dividend = VGroup(d2, d3, d4).arrange(RIGHT, buff=0.1)
        setup = VGroup(divisor, bracket, dividend).arrange(RIGHT, buff=0.1)
        setup.scale(1.5).to_edge(LEFT, buff=1)
        self.play(Write(setup))
        self.wait(1)

        # Step 1: Divide 23 by 6, quotient digit 3
        group23 = VGroup(d2, d3)
        box23 = SurroundingRectangle(group23, color=YELLOW)
        self.play(Create(box23))
        self.wait(0.5)
        q1 = MathTex("3").scale(1.5).next_to(d3, UP, buff=0.1)
        self.play(Write(q1))
        self.wait(0.5)
        self.play(FadeOut(box23))
        self.wait(0.5)

        # Multiply: 3 * 6 = 18
        m1_1 = MathTex("1").scale(1.5).next_to(d2, DOWN, buff=0.1)
        m1_2 = MathTex("8").scale(1.5).next_to(d3, DOWN, buff=0.1)
        self.play(Write(VGroup(m1_1, m1_2)))
        self.wait(0.5)

        # Subtraction: 23 - 18 = 5
        sub_line1 = Line(
            m1_1.get_bottom() + DOWN * 0.05,
            m1_2.get_bottom() + DOWN * 0.05,
            stroke_width=2
        )
        self.play(Create(sub_line1))
        self.wait(0.5)
        diff1 = MathTex("5").scale(1.5).next_to(sub_line1, DOWN, buff=0.1)
        diff1.align_to(m1_2, LEFT)
        self.play(Write(diff1))
        self.wait(0.5)

        # Bring down 4
        box4 = SurroundingRectangle(d4, color=YELLOW)
        self.play(Create(box4))
        self.wait(0.5)
        b4 = MathTex("4").scale(1.5).next_to(diff1, RIGHT, buff=0.1)
        self.play(Write(b4))
        self.wait(0.5)
        self.play(FadeOut(box4))
        self.wait(0.5)

        # Step 2: Divide 54 by 6, quotient digit 9
        group54 = VGroup(diff1, b4)
        box54 = SurroundingRectangle(group54, color=YELLOW)
        self.play(Create(box54))
        self.wait(0.5)
        q2 = MathTex("9").scale(1.5).next_to(d4, UP, buff=0.1)
        self.play(Write(q2))
        self.wait(0.5)
        self.play(FadeOut(box54))
        self.wait(0.5)

        # Multiply: 9 * 6 = 54
        m2_1 = MathTex("5").scale(1.5).next_to(diff1, DOWN, buff=0.1)
        m2_2 = MathTex("4").scale(1.5).next_to(b4, DOWN, buff=0.1)
        self.play(Write(VGroup(m2_1, m2_2)))
        self.wait(0.5)

        # Subtraction: 54 - 54 = 0
        sub_line2 = Line(
            m2_1.get_bottom() + DOWN * 0.05,
            m2_2.get_bottom() + DOWN * 0.05,
            stroke_width=2
        )
        self.play(Create(sub_line2))
        self.wait(0.5)
        diff2 = MathTex("0").scale(1.5).next_to(sub_line2, DOWN, buff=0.1)
        diff2.align_to(m2_2, LEFT)
        self.play(Write(diff2))
        self.wait(1)