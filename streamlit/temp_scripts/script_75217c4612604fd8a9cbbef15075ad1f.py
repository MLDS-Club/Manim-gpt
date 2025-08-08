from manim import *
import numpy as np

class TriangleAreaCalculationScene(Scene):
    def construct(self):
        # Title
        title = Tex("Area of a Triangle", font_size=48)
        self.play(Write(title))
        self.wait(1)

        # Define vertices
        A = np.array([0, 2, 0])
        B = np.array([-3, 0, 0])
        C = np.array([3, 0, 0])

        # Draw triangle
        triangle = Polygon(A, B, C, color=GREY)
        triangle.set_fill(BLUE, opacity=0.3)
        self.play(Create(triangle), run_time=2)

        # Label vertices
        label_A = MathTex("A").next_to(A, UP + LEFT, buff=0.1)
        label_B = MathTex("B").next_to(B, DOWN, buff=0.1)
        label_C = MathTex("C").next_to(C, DOWN, buff=0.1)
        self.play(Write(label_A), Write(label_B), Write(label_C))
        self.wait(1)

        # Highlight base BC
        side_bc = Line(B, C, color=YELLOW, stroke_width=4)
        self.play(Create(side_bc), run_time=1)
        b_label = MathTex("b").set_color(YELLOW).next_to(side_bc, DOWN, buff=0.1)
        self.play(Write(b_label))
        self.wait(1)

        # Draw height AD
        D = np.array([0, 0, 0])
        height_line = DashedLine(A, D, color=GREEN)
        self.play(Create(height_line), run_time=1)
        h_label = MathTex("h").set_color(GREEN).next_to(height_line, LEFT, buff=0.1)
        self.play(Write(h_label))
        self.wait(1)

        # Show formula
        formula = MathTex("A", "=", r"\tfrac{1}{2}", "b", "h", font_size=48).to_corner(UR)
        self.play(Write(formula), run_time=2)
        self.wait(1)

        # Indicate b and h in formula
        arrow_b = Arrow(formula[3].get_bottom(), b_label.get_top(), color=YELLOW)
        self.play(Create(arrow_b), Indicate(formula[3], color=YELLOW))
        self.wait(0.5)
        arrow_h = Arrow(formula[4].get_bottom(), h_label.get_top(), color=GREEN)
        self.play(Create(arrow_h), Indicate(formula[4], color=GREEN))
        self.wait(1)

        # Substitute numeric values on geometry
        six = MathTex("6").set_color(YELLOW).move_to(b_label)
        two = MathTex("2").set_color(GREEN).move_to(h_label)
        self.play(Transform(b_label, six), Transform(h_label, two))
        self.wait(1)

        # Show substitution in formula
        step1 = MathTex("=", r"\tfrac{1}{2}", r"\times 6", r"\times 2", font_size=36)
        step1.next_to(formula, DOWN, aligned_edge=LEFT)
        self.play(Write(step1), run_time=2)
        self.wait(1)

        # Compute result
        step2 = MathTex("=", "6", font_size=36).next_to(step1, DOWN, aligned_edge=LEFT)
        self.play(Write(step2), run_time=1.5)
        self.wait(2)