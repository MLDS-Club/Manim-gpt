from manim import *

class HelicopterLiftScene(Scene):
    def construct(self):
        # Title
        title = Text("How a Helicopter Generates Lift", font_size=48).to_edge(UP)
        self.play(Write(title), run_time=2)
        self.wait(1)

        # Rotor disc and blades
        disc = Circle(radius=2, color=WHITE)
        blade1 = Line(LEFT * 2, RIGHT * 2, color=WHITE)
        blade2 = blade1.copy().rotate(PI / 2)
        rotor = VGroup(disc, blade1, blade2).move_to(DOWN)
        rotor.add_updater(lambda m, dt: m.rotate(PI * dt))
        self.add(rotor)
        self.wait(1)

        # Induced velocity arrow
        arrow_down = Arrow(
            rotor.get_center() + UP * 0.1,
            rotor.get_center() + DOWN * 3,
            buff=0,
            color=YELLOW
        )
        vi_label = MathTex("v_i", color=YELLOW).next_to(arrow_down, RIGHT)
        self.play(GrowArrow(arrow_down), Write(vi_label), run_time=1.5)
        self.wait(1)

        # Momentum theory formulas
        formula1 = MathTex(r"\dot m = \rho A v_i").to_corner(UL)
        formula2 = MathTex(r"T = 2\rho A v_i^2").next_to(formula1, DOWN, aligned_edge=LEFT)
        formula3 = MathTex(r"v_i = \sqrt{\frac{T}{2\rho A}}").next_to(formula2, DOWN, aligned_edge=LEFT)
        self.play(Write(formula1), run_time=1)
        self.wait(0.5)
        self.play(Write(formula2), run_time=1)
        self.wait(0.5)
        self.play(Write(formula3), run_time=1)
        self.wait(1)

        # Fade out formulas and arrow
        self.play(FadeOut(VGroup(formula1, formula2, formula3, arrow_down, vi_label)), run_time=1)
        self.wait(1)

        # Blade cross-section
        airfoil = Ellipse(width=2, height=0.5, color=WHITE)
        chord_line = Line(
            airfoil.get_center() + LEFT,
            airfoil.get_center() + RIGHT,
            color=YELLOW
        )
        blade_cs = VGroup(airfoil, chord_line).to_corner(UR)
        cs_label = Text("Blade Cross-section", font_size=24).next_to(blade_cs, UP)
        self.play(Create(airfoil), Create(chord_line), run_time=1.5)
        self.play(Write(cs_label), run_time=1)
        self.wait(1)

        # Relative velocity vector
        start = blade_cs.get_center() + UP * 0.8 + LEFT * 0.2
        end = blade_cs.get_center() + RIGHT * 0.2
        vrel_arrow = Arrow(start, end, buff=0, color=BLUE)
        vrel_label = MathTex(r"\vec v_{rel}", color=BLUE).scale(0.7).next_to(vrel_arrow, UP)
        self.play(GrowArrow(vrel_arrow), Write(vrel_label), run_time=1)
        self.wait(1)

        # Angle of attack
        arc = Arc(
            radius=0.6,
            start_angle=0,
            angle=-PI/4,
            color=WHITE
        ).shift(blade_cs.get_center())
        alpha_label = MathTex(r"\alpha").scale(0.7).next_to(
            arc.point_from_proportion(0.5), DOWN * 0.1 + RIGHT * 0.1
        )
        self.play(Create(arc), Write(alpha_label), run_time=1)
        self.wait(1)

        # Lift vector
        lift_arrow = Arrow(
            blade_cs.get_center(),
            blade_cs.get_center() + UP * 1,
            buff=0,
            color=GREEN
        )
        L_label = MathTex("L", color=GREEN).next_to(lift_arrow, RIGHT)
        self.play(GrowArrow(lift_arrow), Write(L_label), run_time=1)
        self.wait(2)