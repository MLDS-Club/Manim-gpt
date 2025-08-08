from manim import *
import numpy as np

class PizzaFractionScene(Scene):
    def construct(self):
        # Whole pizza
        r = 2
        pizza = Circle(radius=r, color=WHITE).set_fill(ORANGE, opacity=1)
        whole_label = MathTex("1").scale(1.5).next_to(pizza, UP)
        self.play(Create(pizza), Write(whole_label))
        self.wait(2)

        # Halves
        diameter = Line(UP * r, DOWN * r, color=BLACK)
        self.play(Create(diameter))
        half_label_top = MathTex(r"\frac{1}{2}").scale(1).move_to(UP * (r / 2))
        half_label_bottom = MathTex(r"\frac{1}{2}").scale(1).move_to(DOWN * (r / 2))
        central_angle_eq = MathTex(
            r"\text{Central Angle}", "=", r"360^\circ", "/", r"2", "=", r"180^\circ"
        ).to_corner(RIGHT + UP)
        self.play(Write(half_label_top), Write(half_label_bottom))
        self.wait(1)
        self.play(Write(central_angle_eq))
        self.wait(2)
        self.play(FadeOut(central_angle_eq))

        # Quarters
        horizontal = Line(LEFT * r, RIGHT * r, color=BLACK)
        self.play(Create(horizontal))
        quarter_positions = [
            np.array([ r/2,  r/2, 0]),
            np.array([-r/2,  r/2, 0]),
            np.array([-r/2, -r/2, 0]),
            np.array([ r/2, -r/2, 0]),
        ]
        quarter_labels = VGroup(*[
            MathTex(r"\frac{1}{4}").scale(0.8).move_to(pos)
            for pos in quarter_positions
        ])
        self.play(Write(quarter_labels))
        self.wait(2)

        # Show 1/4 + 1/4 = 2/4 = 1/2
        eq = MathTex(
            r"\frac{1}{4}", "+", r"\frac{1}{4}", "=", r"\frac{2}{4}", "=", r"\frac{1}{2}"
        ).to_edge(DOWN)
        self.play(Write(eq))
        self.wait(2)

        # Highlight two quarters
        sector1 = Sector(radius=r, start_angle=0, angle=PI/2,
                         fill_color=YELLOW, fill_opacity=0.5, stroke_width=0)
        sector2 = Sector(radius=r, start_angle=PI/2, angle=PI/2,
                         fill_color=YELLOW, fill_opacity=0.5, stroke_width=0)
        sectors = VGroup(sector1, sector2)
        self.play(FadeIn(sectors))
        self.wait(2)

        # Simplify 2/4 to 1/2
        frac_2_4 = eq[4]
        frac_1_2 = eq[6]
        arrow = Arrow(frac_2_4.get_right(), frac_1_2.get_left(), buff=0.1)
        self.play(Create(arrow), run_time=1)
        self.wait(2)