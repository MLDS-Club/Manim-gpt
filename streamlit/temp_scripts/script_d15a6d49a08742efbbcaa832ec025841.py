from manim import *

class PizzaFractionScene(Scene):
    def construct(self):
        # Scene setup
        self.camera.frame.set_height(6)  # Ensure full pizza is visible
        title = Text("Understanding Fractions with a Pizza").scale(0.9).to_edge(UP)
        self.play(Write(title), run_time=1.5)
        self.wait(0.5)

        # Define pizza parameters
        n_slices = 8
        radius = 2
        angle = TAU / n_slices

        # Draw pizza slices
        slices = VGroup(*[
            Sector(
                radius=radius,
                start_angle=i * angle,
                angle=angle,
                fill_color=GREY,
                fill_opacity=1,
                stroke_color=BLACK,
                stroke_width=2
            )
            for i in range(n_slices)
        ])
        slices.move_to(ORIGIN)
        self.play(*[Create(s) for s in slices], run_time=2, lag_ratio=0.1)
        self.wait(1)

        # Label each slice (1 through 8)
        labels = VGroup(*[
            MathTex(str(i+1)).scale(0.5).move_to(
                (radius*0.6) * np.array([
                    np.cos(i * angle + angle/2),
                    np.sin(i * angle + angle/2),
                    0
                ])
            )
            for i in range(n_slices)
        ])
        for lbl in labels:
            self.play(FadeIn(lbl), run_time=0.3)
        self.wait(1)

        # Demonstrate selection: highlight 3 slices for 3/8
        fraction_parts = 3
        selected_slices = VGroup(*[slices[i] for i in range(fraction_parts)])
        self.play(
            *[s.animate.set_fill(ORANGE, opacity=1) for s in selected_slices],
            run_time=1.5,
            lag_ratio=0.2
        )
        self.wait(1)

        # Show fraction 3/8 on screen
        frac_tex = MathTex(r"\frac{3}{8}").scale(1.2).to_edge(DOWN, buff=0.8)
        self.play(Write(frac_tex), run_time=1)
        self.wait(1)

        # Walk through simplification: 3 and 8 have no common factors
        expl = Text("3 and 8 have no common factors", font_size=36).next_to(frac_tex, UP, buff=0.5)
        self.play(Write(expl), run_time=1.2)
        self.wait(2)

        # Replace explanation with "Fraction is in simplest form"
        simplest = Text("This fraction is already in simplest form", font_size=36).move_to(expl)
        self.play(Transform(expl, simplest), run_time=1)
        self.wait(2)

        # Clear and wrap up
        self.play(FadeOut(VGroup(slices, labels, frac_tex, expl)), run_time=1.5)
        conclusion = Text("Fractions show part of a whole!", font_size=42).scale(1.1)
        self.play(Write(conclusion), run_time=1.5)
        self.wait(2)