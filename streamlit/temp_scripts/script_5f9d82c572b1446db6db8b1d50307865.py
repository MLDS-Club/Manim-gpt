from manim import *
import numpy as np

class PizzaFractionsScene(Scene):
    def construct(self):
        # Title
        title = Text("Fractions with Pizza", font_size=48)
        self.play(Write(title), run_time=2)
        self.wait(1)
        self.play(title.animate.to_edge(UP), run_time=1)
        self.wait(1)

        # Draw pizza base
        pizza = Circle(radius=2, color=ORANGE, fill_opacity=1)
        self.play(Create(pizza), run_time=2)
        self.wait(1)

        # Demonstrate 1/2
        half_cut = VGroup(
            Line(ORIGIN, np.array([2, 0, 0])),
            Line(ORIGIN, np.array([-2, 0, 0]))
        )
        half_slice = Sector(angle=PI, radius=2, start_angle=0, outer_radius=2,
                            color=YELLOW, fill_opacity=0.7)
        self.play(Create(half_cut), run_time=1)
        self.play(FadeIn(half_slice), run_time=1)
        half_label = MathTex(r"1", r"/", r"2", font_size=36).next_to(pizza, DOWN)
        self.play(Write(half_label), run_time=1)
        num_lbl = Text("numerator", font_size=24, color=WHITE)\
                  .set_stroke(BLACK, 1).next_to(half_label[0], UP, buff=0.1)
        den_lbl = Text("denominator", font_size=24, color=WHITE)\
                  .set_stroke(BLACK, 1).next_to(half_label[2], DOWN, buff=0.1)
        self.play(Write(num_lbl), Write(den_lbl), run_time=1)
        self.wait(2)
        self.play(FadeOut(half_cut), FadeOut(half_slice),
                  FadeOut(half_label), FadeOut(num_lbl), FadeOut(den_lbl))
        self.wait(1)

        # Demonstrate 1/3
        angles3 = [0, 2*PI/3, 4*PI/3]
        cuts3 = VGroup(*[
            Line(ORIGIN, [2*np.cos(a), 2*np.sin(a), 0]) for a in angles3
        ])
        sectors3 = VGroup(*[
            Sector(angle=2*PI/3, radius=2, start_angle=a,
                   color=c, fill_opacity=0.7)
            for a, c in zip(angles3, [BLUE, GREEN, RED])
        ])
        self.play(Create(cuts3), run_time=1)
        self.play(FadeIn(sectors3), run_time=1)
        third_label = MathTex(r"1", r"/", r"3", font_size=36).next_to(pizza, DOWN)
        self.play(Write(third_label), run_time=1)
        self.wait(2)
        self.play(FadeOut(cuts3), FadeOut(sectors3), FadeOut(third_label))
        self.wait(1)

        # Demonstrate 1/4
        angles4 = [k * PI/2 for k in range(4)]
        cuts4 = VGroup(*[
            Line(ORIGIN, [2*np.cos(a), 2*np.sin(a), 0]) for a in angles4
        ])
        sectors4 = VGroup(*[
            Sector(angle=PI/2, radius=2, start_angle=a,
                   color=c, fill_opacity=0.7)
            for a, c in zip(angles4, [TEAL, PINK, PURPLE, YELLOW])
        ])
        self.play(Create(cuts4), run_time=1)
        self.play(FadeIn(sectors4), run_time=1)
        quarter_label = MathTex(r"1", r"/", r"4", font_size=36).next_to(pizza, DOWN)
        self.play(Write(quarter_label), run_time=1)
        self.wait(2)
        self.play(FadeOut(cuts4), FadeOut(sectors4), FadeOut(quarter_label))
        self.wait(1)

        # Summary
        summary = MathTex(
            r"\frac{1}{2},\;\frac{1}{3},\;\frac{1}{4}", font_size=36
        ).to_edge(DOWN)
        self.play(Write(summary), run_time=2)
        self.wait(2)