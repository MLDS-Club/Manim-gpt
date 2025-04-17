from manim import *

class LiftDemoScene(Scene):
    def construct(self):
        # Title
        title = Text("How Wings Generate Lift", font_size=48)
        self.play(Write(title), run_time=2)
        self.wait(1)
        self.play(title.animate.to_edge(UP), run_time=1)
        self.wait(1)

        # Draw airfoil using CubicBezier
        p0 = LEFT * 2 + DOWN * 0.5
        p1 = LEFT * 1 + UP * 0.2
        p2 = RIGHT * 1 + UP * 0.2
        p3 = RIGHT * 2 + DOWN * 0.5
        wing = CubicBezier(p0, p1, p2, p3).set_fill(GRAY, 1).set_stroke(BLACK, 2)
        wing_label = MathTex(r"\text{Airfoil}").scale(0.7).next_to(wing, DOWN)
        self.play(Create(wing), Write(wing_label), run_time=2)
        self.wait(1)

        # Streamlines
        s0 = LEFT * 4 + UP
        s1 = LEFT * 2 + UP * 1.2
        s2 = RIGHT * 2 + UP * 1.2
        s3 = RIGHT * 4 + UP
        top_stream = CubicBezier(s0, s1, s2, s3).set_stroke(BLUE, 2)
        b0 = LEFT * 4 + DOWN
        b1 = LEFT * 2 + DOWN * 0.8
        b2 = RIGHT * 2 + DOWN * 0.8
        b3 = RIGHT * 4 + DOWN
        bottom_stream = CubicBezier(b0, b1, b2, b3).set_stroke(GREEN, 2)
        self.play(Create(top_stream), Create(bottom_stream), run_time=2)
        self.wait(1)

        # Airflow dots and velocity labels
        dot_top = Dot(color=BLUE).move_to(top_stream.get_start())
        dot_bottom = Dot(color=GREEN).move_to(bottom_stream.get_start())
        v2_label = MathTex(r"v_2").scale(0.7).set_color(BLUE)
        v2_label.next_to(top_stream.point_from_proportion(0.3), UP, buff=0.1)
        v1_label = MathTex(r"v_1").scale(0.7).set_color(GREEN)
        v1_label.next_to(bottom_stream.point_from_proportion(0.3), DOWN, buff=0.1)
        self.play(FadeIn(dot_top), FadeIn(dot_bottom), Write(v2_label), Write(v1_label))
        self.wait(0.5)
        self.play(
            MoveAlongPath(dot_top, top_stream, rate_func=linear, run_time=4),
            MoveAlongPath(dot_bottom, bottom_stream, rate_func=linear, run_time=6)
        )
        self.wait(1)

        # Bernoulli equation
        eq = MathTex(r"p + \tfrac{1}{2}\rho v^2 = C").to_corner(UR)
        self.play(Write(eq), run_time=2)
        self.wait(1)

        # Pressure regions and labels
        top_region = Rectangle(width=4, height=0.2)
        top_region.move_to(wing.get_center()).shift(UP * 0.3).set_fill(BLUE, 0.3).set_stroke(width=0)
        low_region = Rectangle(width=4, height=0.2)
        low_region.move_to(wing.get_center()).shift(DOWN * 0.3).set_fill(RED, 0.3).set_stroke(width=0)
        p2 = MathTex(r"p_2").set_color(BLUE).next_to(top_region, UP, buff=0.1)
        p1 = MathTex(r"p_1").set_color(RED).next_to(low_region, DOWN, buff=0.1)
        self.play(FadeIn(top_region), FadeIn(low_region), Write(p2), Write(p1))
        self.wait(1)

        # Pressure difference derivation
        deriv = MathTex(
            r"\Delta p", r"=", r"p_1", r"-", r"p_2", r"=",
            r"\tfrac{1}{2}\rho", r"(", r"v_2^2", r"-", r"v_1^2", r")"
        ).scale(0.7).to_corner(DR)
        deriv[2].set_color(RED)
        deriv[4].set_color(BLUE)
        deriv[8].set_color(YELLOW)
        deriv[10].set_color(YELLOW)
        self.play(Write(deriv), run_time=3)
        self.wait(1)

        # Lift arrow
        lift_arrow = Arrow(
            start=wing.get_center() + DOWN * 0.2,
            end=wing.get_center() + UP * 1.2,
            buff=0
        ).set_color(RED)
        lift_label = MathTex(r"\text{Lift}").scale(0.7).set_color(RED).next_to(lift_arrow, RIGHT)
        self.play(GrowArrow(lift_arrow), Write(lift_label))
        self.wait(2)