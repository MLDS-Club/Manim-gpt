from manim import *
import numpy as np

class TriangleAreaCalculationScene(Scene):
    def construct(self):
        # 1. Define triangle vertices
        A = np.array([-4, -2, 0])
        B = np.array([4, -2, 0])
        C = np.array([0, 2, 0])

        # 2. Draw triangle
        triangle = Polygon(A, B, C, color=WHITE)
        self.play(Create(triangle), run_time=2)

        # 3. Label vertices A, B, C
        labelA = MathTex("A").next_to(A, DOWN + LEFT)
        labelB = MathTex("B").next_to(B, DOWN + RIGHT)
        labelC = MathTex("C").next_to(C, UP)
        self.play(Write(labelA), Write(labelB), Write(labelC), run_time=1)
        self.wait(1)

        # 4. Draw and label base b = AB
        base_arrow = DoubleArrow(A, B, color=YELLOW)
        label_b    = MathTex("b").set_color(YELLOW).next_to(base_arrow, DOWN)
        self.play(GrowFromCenter(base_arrow), Write(label_b), run_time=1.5)
        self.wait(1)

        # 5. Compute projection foot D of C onto AB for height h
        AB = B - A
        AC = C - A
        proj_len = np.dot(AC, AB) / np.dot(AB, AB)
        D = A + proj_len * AB

        # 6. Mark foot D and draw height line CD
        foot     = Dot(D, color=GREEN)
        labelD   = MathTex("D").next_to(foot, DOWN)
        height   = DashedVMobject(Line(C, D), color=GREEN)
        label_h  = MathTex("h").set_color(GREEN).next_to(height, RIGHT)
        self.play(GrowFromCenter(foot), Write(labelD), run_time=1)
        self.play(Create(height),       Write(label_h), run_time=1.5)
        self.wait(1)

        # 7. Right‐angle marker at D
        right_angle = RightAngle(Line(D, C), Line(D, A),
                                 length=0.3, quadrant=(1,1), color=GREEN)
        self.play(Create(right_angle), run_time=1)
        self.wait(1)

        # 8. Show area formula
        formula = MathTex(r"\text{Area} \;=\; \tfrac12\,b\,h")\
                      .to_edge(DOWN)
        self.play(Write(formula), run_time=2)
        self.wait(2)