import numpy as np
from manim import *

class PythagoreanScene(Scene):
    def construct(self):
        title = Text("Pythagorean Theorem").to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        h_tracker = ValueTracker(2)
        base_length = 3

        def get_vertices():
            O = ORIGIN
            A = RIGHT * base_length
            B = UP * h_tracker.get_value()
            return O, A, B

        triangle = always_redraw(
            lambda: Polygon(*get_vertices(), color=WHITE, stroke_width=4)
        )
        self.play(Create(triangle))
        self.wait(0.5)

        def right_angle():
            O, A, _ = get_vertices()
            sz = 0.25
            l1 = Line(O + RIGHT * sz, O + RIGHT * sz + UP * sz)
            l2 = Line(O + UP * sz, O + UP * sz + RIGHT * sz)
            return VGroup(l1, l2)

        self.add(always_redraw(right_angle))

        def square_on(p, q, centroid):
            v = q - p
            length = np.linalg.norm(v)
            perp = np.array([-v[1], v[0], 0.0])
            mid = (p + q) / 2
            if np.dot(perp, centroid - mid) > 0:
                perp = -perp
            perp = perp / np.linalg.norm(perp) * length
            verts = [p, q, q + perp, p + perp]
            return Polygon(*verts, color=BLUE, fill_opacity=0.25, stroke_width=3)

        def a_square_func():
            O, A, B = get_vertices()
            cent = (O + A + B) / 3
            return square_on(O, A, cent)

        def b_square_func():
            O, A, B = get_vertices()
            cent = (O + A + B) / 3
            return square_on(O, B, cent)

        def c_square_func():
            O, A, B = get_vertices()
            cent = (O + A + B) / 3
            return square_on(A, B, cent)

        a_sq = always_redraw(a_square_func)
        b_sq = always_redraw(b_square_func)
        c_sq = always_redraw(c_square_func)

        self.play(Create(a_sq), run_time=1)
        self.play(Create(b_sq), run_time=1)
        self.play(Create(c_sq), run_time=1)
        self.wait(0.5)

        def a_label_func():
            O, A, B = get_vertices()
            cent = (O + A + B) / 3
            mid = (O + A) / 2
            off = (mid - cent) / np.linalg.norm(mid - cent) * 0.3
            return MathTex("a").move_to(mid + off)

        def b_label_func():
            O, A, B = get_vertices()
            cent = (O + A + B) / 3
            mid = (O + B) / 2
            off = (mid - cent) / np.linalg.norm(mid - cent) * 0.3
            return MathTex("b").move_to(mid + off)

        def c_label_func():
            O, A, B = get_vertices()
            cent = (O + A + B) / 3
            mid = (A + B) / 2
            off = (mid - cent) / np.linalg.norm(mid - cent) * 0.3
            return MathTex("c").move_to(mid + off)

        a_lab = always_redraw(a_label_func)
        b_lab = always_redraw(b_label_func)
        c_lab = always_redraw(c_label_func)
        self.play(FadeIn(a_lab), FadeIn(b_lab), FadeIn(c_lab))
        self.wait(0.5)

        a2 = always_redraw(lambda: MathTex("a^2").move_to(a_sq.get_center()))
        b2 = always_redraw(lambda: MathTex("b^2").move_to(b_sq.get_center()))
        c2 = always_redraw(lambda: MathTex("c^2").move_to(c_sq.get_center()))
        self.play(FadeIn(a2), FadeIn(b2), FadeIn(c2))
        self.wait(0.5)

        eq = MathTex("a^2", "+", "b^2", "=", "c^2").next_to(title, DOWN, buff=0.4)
        self.play(Write(eq))
        self.wait(1)

        self.play(Circumscribe(a2, color=YELLOW), Circumscribe(eq[0], color=YELLOW))
        self.play(Circumscribe(b2, color=YELLOW), Circumscribe(eq[2], color=YELLOW))
        self.play(Circumscribe(c2, color=YELLOW), Circumscribe(eq[4], color=YELLOW))
        self.wait(0.5)

        self.play(h_tracker.animate.set_value(1), run_time=2)
        self.wait(0.5)
        self.play(h_tracker.animate.set_value(2.5), run_time=2)
        self.wait(1)

        self.play(*[FadeOut(m) for m in self.mobjects])
        self.wait()