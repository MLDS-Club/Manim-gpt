from manim import *

class AppleFractionScene(Scene):
    def construct(self):
        # Title
        title = Text("Demonstrating Fractions with Apple Slices", font_size=36)
        title.to_edge(UP)
        self.play(Write(title), run_time=2)
        self.wait(0.5)

        # Parameters
        total_slices = 8
        eaten_slices = 3
        radius = 2.0

        # Draw apple slices
        slices = VGroup(*[
            Sector(
                radius=radius,
                start_angle=i * TAU / total_slices,
                angle=TAU / total_slices,
                stroke_color=WHITE,
                stroke_width=1,
                fill_color=GREEN,
                fill_opacity=0.3
            )
            for i in range(total_slices)
        ])
        slices.move_to(ORIGIN)
        self.play(
            LaggedStart(
                *[GrowFromCenter(s) for s in slices],
                lag_ratio=0.1
            ),
            run_time=2
        )
        self.wait(0.5)

        # Highlight eaten slices
        eaten = VGroup(*slices[:eaten_slices])
        self.play(
            LaggedStart(
                *[m.animate.set_fill(RED, opacity=0.8) for m in eaten],
                lag_ratio=0.1
            ),
            run_time=2
        )
        self.wait(0.5)

        # Show generic fraction formula
        formula1 = MathTex(
            r"\text{Fraction eaten} = ",
            r"\frac{\text{eaten slices}}{\text{total slices}}",
            font_size=36
        )
        formula1.next_to(slices, DOWN, buff=1)
        self.play(Write(formula1), run_time=2)
        self.wait(0.5)

        # Show numeric fraction
        formula2 = MathTex(r"\frac{3}{8}", font_size=36)
        formula2.next_to(formula1, DOWN, buff=0.5)
        formula2.set_color_by_tex("3", RED)
        formula2.set_color_by_tex("8", BLUE)
        self.play(Write(formula2), run_time=2)
        self.wait(0.5)

        # Decimal representation with ValueTracker
        tracker = ValueTracker(0)
        decimal = always_redraw(
            lambda: MathTex(
                f"= {tracker.get_value():.3f}",
                font_size=36
            ).next_to(formula2, RIGHT, buff=0.5)
        )
        self.play(FadeIn(decimal), run_time=1)
        self.play(tracker.animate.set_value(eaten_slices / total_slices), run_time=3)
        self.wait(2)