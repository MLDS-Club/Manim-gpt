from manim import *
import numpy as np
import math

# Custom colors
ROYAL_BLUE = "#4169E1"
GREY_E = "#E5E5E5"

class Introduction(Scene):
    def construct(self):
        # Shot 1.1 (0–3s)
        title = Text("The Pythagorean Theorem", font_size=72, weight="BOLD", color=WHITE)
        title.set_stroke(BLACK, width=1)
        self.play(FadeIn(title, run_time=1.5))
        self.wait(1.5)

        # Shot 1.2 (3–8s)
        self.play(FadeOut(title, run_time=1))
        A = np.array([-3, 0, 0])
        B = A + UP * 2
        C = A + RIGHT * 3
        line1 = Line(A, B, stroke_color=ROYAL_BLUE)
        line2 = Line(A, C, stroke_color=ROYAL_BLUE)
        line3 = Line(B, C, stroke_color=ROYAL_BLUE)
        self.play(Create(line1, run_time=0.5))
        self.play(Create(line2, run_time=0.5))
        self.play(Create(line3, run_time=0.5))
        self.wait(2)

        # Shot 1.3 (8–12s)
        label_a = Text("a", font_size=48, color=WHITE).move_to((A + B)/2 + LEFT*0.3)
        label_b = Text("b", font_size=48, color=WHITE).move_to((A + C)/2 + DOWN*0.3)
        label_c = Text("c", font_size=48, color=YELLOW).move_to((B + C)/2 + RIGHT*0.3)
        right_angle = RightAngle(line1, line2, length=0.3, quadrant=(1, -1), color=WHITE)
        self.play(
            Write(label_a, run_time=0.4),
            Write(label_b, run_time=0.4),
            Write(label_c, run_time=0.4),
            FadeIn(right_angle, run_time=0.4)
        )
        self.wait(3.6)

        # Shot 1.4 (12–20s)
        eq = MathTex("a^2 + b^2 = ?", font_size=60, color=WHITE).shift(DOWN*4)
        self.play(eq.animate.shift(UP*3), run_time=1)
        self.wait(7)

class BuildingSquares(Scene):
    def construct(self):
        # Keep triangle
        A = np.array([-3, 0, 0])
        B = A + UP * 2
        C = A + RIGHT * 3
        tri = VGroup(Line(A, B, color=WHITE), Line(A, C, color=WHITE), Line(B, C, color=WHITE))
        self.add(tri)

        # Shot 2.1 (0–5s): red square on a
        sq_a = Square(side_length=2).set_fill(RED, opacity=0.3).set_stroke(RED, width=2)
        sq_a.rotate(PI/2).move_to((A + B)/2 + LEFT)
        self.play(FadeIn(sq_a, run_time=1))
        self.wait(4)

        # Shot 2.2 (5–10s): green square on b
        sq_b = Square(side_length=3).set_fill(GREEN, opacity=0.3).set_stroke(GREEN, width=2)
        sq_b.move_to((A + C)/2 + DOWN*1.5)
        self.play(GrowFromPoint(sq_b, A, run_time=1))
        self.wait(4)

        # Shot 2.3 (10–15s): blue square on c
        c_len = Line(B, C).get_length()
        sq_c = Square(side_length=c_len).set_fill(BLUE, opacity=0.3).set_stroke(BLUE, width=2)
        angle = Line(B, C).get_angle()
        normal = np.array([-np.sin(angle), np.cos(angle), 0])
        sq_c.rotate(angle).move_to((B + C)/2 + normal*(c_len/2))
        sq_c_off = sq_c.copy().shift(RIGHT*5)
        self.add(sq_c_off)
        self.play(ReplacementTransform(sq_c_off, sq_c, run_time=1))
        self.wait(4)

        # Shot 2.4 (15–25s): highlights and text
        self.play(Indicate(sq_a, color=RED), run_time=0.5)
        self.play(Indicate(sq_b, color=GREEN), run_time=0.5)
        self.wait(0.5)
        self.play(Indicate(sq_c, color=BLUE), run_time=0.5)
        algebra = MathTex("a^2 + b^2 = ?~~~vs.~~~c^2", font_size=48, color=WHITE).to_edge(DOWN)
        self.play(Write(algebra, run_time=1))
        self.wait(8)

class RearrangementProof(Scene):
    def construct(self):
        # Shot 3.1 (0–3s): title
        title = Text("Proof by Rearrangement", font_size=60, color=WHITE)
        self.play(FadeIn(title, run_time=1))
        self.wait(2)
        self.play(FadeOut(title, run_time=1))

        # Shot 3.2 (3–10s): big square and 4 triangles
        big_sq = Square(side_length=6).set_stroke(GREY_E, width=2).move_to(ORIGIN)
        self.play(Create(big_sq, run_time=1))
        a, b = 2, 3
        tri_proto = Polygon(ORIGIN, UP*a, RIGHT*b, color=WHITE)
        for corner, ang in zip([DL, DR, UR, UL], [0, PI/2, PI, 3*PI/2]):
            tri = tri_proto.copy().rotate(ang, about_point=ORIGIN)
            tri.shift(big_sq.get_corner(corner))
            self.play(FadeIn(tri, run_time=0.5))
        self.wait(1)

        # Shot 3.3 (10–16s): center square c
        c_val = math.hypot(a, b)
        center_sq = Square(side_length=c_val).set_fill(YELLOW, opacity=0.3).set_stroke(YELLOW, width=2).move_to(ORIGIN)
        self.play(ShowCreation(center_sq), run_time=0.5)
        self.play(Indicate(center_sq, color=YELLOW), run_time=0.5)
        label_c = Text("c", font_size=48, color=WHITE).next_to(center_sq, RIGHT, buff=0.1)
        self.play(Write(label_c, run_time=0.5))
        self.wait(2)

        # Shot 3.4 (16–26s): algebra derivation
        self.play(
            big_sq.animate.set_opacity(0.5),
            *[m.animate.set_opacity(0.5) for m in self.mobjects if isinstance(m, (Polygon, Line, Square, Text))],
        )
        lines = [
            "(a + b)^2 = 4 \\cdot (1/2 ab) + c^2",
            "a^2 + 2ab + b^2 = 2ab + c^2",
            "a^2 + b^2 = c^2",
        ]
        algebra = VGroup(*[MathTex(l, font_size=36, color=WHITE) for l in lines])
        for i, line in enumerate(algebra):
            line.to_corner(UR).shift(DOWN*(i*0.6))
            self.play(Write(line, run_time=1))
            self.wait(0.5)
        self.wait(2)

        # Shot 3.5 (26–40s): final statement and zoom
        self.play(FadeOut(algebra, run_time=1))
        self.play(
            big_sq.animate.set_opacity(1),
            *[m.animate.set_opacity(1) for m in self.mobjects if isinstance(m, (Polygon, Line, Square, Text))],
        )
        final_txt = Text("Therefore, in any right triangle, a^2 + b^2 = c^2.", font_size=48, color=WHITE).to_edge(DOWN)
        check = Text("✔", font_size=48, color=GREEN).next_to(final_txt, LEFT, buff=0.5)
        self.play(FadeIn(final_txt, run_time=1))
        self.play(FadeIn(check, scale_factor=1.5, run_time=1))
        self.wait(0.5)
        self.play(self.camera.frame.animate.scale(0.9), run_time=4)
        self.wait(2)

class NumericalExamples(Scene):
    def construct(self):
        # Shot 4.1 (0–8s): 3-4-5 triangle
        A = np.array([-1, 0, 0])
        B = A + UP * 3
        C = A + RIGHT * 4
        lines = VGroup(
            Line(A, B, stroke_color=BLUE),
            Line(A, C, stroke_color=GREEN),
            Line(B, C, stroke_color=YELLOW),
        )
        self.play(Create(lines, run_time=1))
        lab3 = Text("3", font_size=36, color=BLUE).move_to((A+B)/2 + LEFT*0.3)
        lab4 = Text("4", font_size=36, color=GREEN).move_to((A+C)/2 + DOWN*0.3)
        lab5 = Text("5", font_size=36, color=YELLOW).move_to((B+C)/2 + RIGHT*0.3)
        self.play(FadeIn(lab3), FadeIn(lab4), FadeIn(lab5))
        self.wait(2)

        # Shot 4.2 (8–16s): arithmetic
        eq1 = MathTex("3^2 + 4^2 =", font_size=36).to_edge(UR)
        eq2 = MathTex("9 + 16 = 25", font_size=36).next_to(eq1, DOWN, aligned_edge=LEFT)
        eq3 = MathTex("c = \\sqrt{25} = 5", font_size=36).next_to(eq2, DOWN, aligned_edge=LEFT)
        self.play(Write(eq1, run_time=0.8)); self.wait(0.4)
        self.play(Write(eq2, run_time=0.8)); self.wait(0.4)
        self.play(Write(eq3, run_time=0.8)); self.wait(2)

        # Shot 4.3 (16–25s): icons
        roof_icon = Rectangle(width=1, height=0.5, color=WHITE)
        ladder_icon = Line(LEFT, RIGHT, color=WHITE)
        icons = VGroup(roof_icon, ladder_icon).arrange(RIGHT, buff=1).to_edge(DOWN)
        cap1 = Text("roof pitch", font_size=24, color=WHITE).next_to(roof_icon, DOWN)
        cap2 = Text("ladder height", font_size=24, color=WHITE).next_to(ladder_icon, DOWN)
        self.play(FadeOut(lines, eq1, eq2, eq3, lab3, lab4, lab5), run_time=1)
        self.play(FadeIn(icons, cap1, cap2), run_time=1)
        self.wait(3)

        # Final Frame (25s+): closing text
        final1 = MathTex("a^2 + b^2 = c^2", font_size=72, color=WHITE)
        final2 = Text("The Pythagorean Theorem", font_size=36, color=WHITE).next_to(final1, DOWN)
        self.play(FadeIn(final1, final2))
        self.wait(3)
        self.play(FadeOut(final1, final2))