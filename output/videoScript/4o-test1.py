from manim import *

class AirfoilLiftScene(Scene):
    def construct(self):
        # Title
        title = Text("Lift Generation on an Airfoil", font_size=36)
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))

        # Draw simplified airfoil shape
        wing_points = [
            [-2, 0, 0],
            [-1.5, 0.3, 0],
            [0, 0.4, 0],
            [1.5, 0.3, 0],
            [2, 0, 0],
            [1.5, -0.3, 0],
            [0, -0.4, 0],
            [-1.5, -0.3, 0]
        ]
        wing = VMobject()
        wing.set_points_as_cubic_bezier([
            *wing_points[:4],
            *wing_points[3:8],
            wing_points[0]
        ])
        wing.set_color(GRAY).set_fill(WHITE, opacity=1)
        self.play(Create(wing), run_time=2)
        self.wait(1)

        # Show flow arrows
        top_arrow = Arrow(start=LEFT*4 + UP*0.8,
                          end=RIGHT*4 + UP*0.8,
                          buff=0, color=BLUE)
        bottom_arrow = Arrow(start=LEFT*4 + DOWN*0.8,
                             end=RIGHT*4 + DOWN*0.8,
                             buff=0, color=BLUE)
        vtop_label = MathTex("v_{\\text{top}}=5", color=BLUE).next_to(top_arrow, UP, buff=0.1)
        vbot_label = MathTex("v_{\\text{bottom}}=3", color=BLUE).next_to(bottom_arrow, DOWN, buff=0.1)
        self.play(GrowArrow(top_arrow), GrowArrow(bottom_arrow))
        self.play(Write(vtop_label), Write(vbot_label))
        self.wait(1)

        # Bernoulli principle
        bern = MathTex(
            "P + \\tfrac12\\rho v^2 = \\text{constant}",
            font_size=30
        ).to_edge(UP)
        self.play(Write(bern))
        self.wait(1)

        # Specific at top and bottom
        eq1 = MathTex(
            "P_{\\text{top}} + \\tfrac12\\rho v_{\\text{top}}^2",
            "=",
            "P_{\\text{bottom}} + \\tfrac12\\rho v_{\\text{bottom}}^2",
            font_size=28
        ).next_to(bern, DOWN, buff=0.5)
        self.play(Write(eq1), run_time=2)
        self.wait(1)

        # Derive pressure difference
        eq2 = MathTex(
            "P_{\\text{bottom}} - P_{\\text{top}}",
            "=",
            "\\tfrac12\\rho \\bigl(v_{\\text{top}}^2 - v_{\\text{bottom}}^2\\bigr)",
            font_size=28
        ).next_to(eq1, DOWN, buff=0.5)
        self.play(Transform(eq1.copy(), eq2), run_time=2)
        self.wait(1)

        # Show pressure arrows
        p_bottom_arrow = Arrow(start=wing.get_center() + DOWN*0.1,
                                end=wing.get_center() + DOWN*0.1 + RIGHT*0.4,
                                buff=0, color=RED)
        p_top_arrow = Arrow(start=wing.get_center() + UP*0.1,
                             end=wing.get_center() + UP*0.1 + LEFT*0.4,
                             buff=0, color=RED)
        pbot_label = MathTex("P_{\\text{bottom}}", color=RED).next_to(p_bottom_arrow, DOWN)
        ptop_label = MathTex("P_{\\text{top}}", color=RED).next_to(p_top_arrow, UP)
        self.play(GrowArrow(p_bottom_arrow), GrowArrow(p_top_arrow))
        self.play(Write(pbot_label), Write(ptop_label))
        self.wait(1)

        # Show Lift force
        lift_arrow = Arrow(start=wing.get_center(),
                           end=wing.get_center() + UP*1,
                           buff=0, color=GREEN)
        lift_label = MathTex("F_L", color=GREEN).next_to(lift_arrow.get_end(), UP)
        self.play(GrowArrow(lift_arrow), Write(lift_label))
        self.wait(2)