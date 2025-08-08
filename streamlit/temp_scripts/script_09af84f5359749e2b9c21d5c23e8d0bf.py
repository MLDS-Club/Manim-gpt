from manim import *
import numpy as np
from manim import rate_functions

class SpiralDrawingScene(Scene):
    def construct(self):
        # 1. Title
        title = Text("Archimedean Spiral", font_size=48).to_edge(UP)
        self.play(Write(title), run_time=1.5)
        # 2. Display formula r = a·θ
        eq = MathTex("r", "=", "a", r"\,\theta", font_size=36)
        eq[0].set_color(GREEN)
        eq[2].set_color(YELLOW)
        eq[3].set_color(BLUE)
        eq.next_to(title, DOWN, buff=0.5)
        self.play(Write(eq), run_time=1.5)
        # 3. Label components
        r_lbl = Text("radius", font_size=24, color=GREEN).next_to(eq[0], DOWN)
        a_lbl = Text("scale factor", font_size=24, color=YELLOW).next_to(eq[2], DOWN)
        th_lbl = Text("angle (rad)", font_size=24, color=BLUE).next_to(eq[3], DOWN)
        self.play(FadeIn(r_lbl), FadeIn(a_lbl), FadeIn(th_lbl), run_time=1)
        self.wait(1)
        # 4. Fade out formula & labels
        self.play(FadeOut(VGroup(title, eq, r_lbl, a_lbl, th_lbl)), run_time=1)
        self.wait(0.5)
        # 5. Setup dynamic spiral
        a = 0.2
        tracker = ValueTracker(0)
        spiral = always_redraw(lambda: ParametricFunction(
            lambda t: np.array([
                a * t * np.cos(t),
                a * t * np.sin(t),
                0
            ]),
            t_range=[0, tracker.get_value()],
            dt=0.01,
            color=WHITE
        ))
        # 6. Dot at spiral tip + traced path
        dot = Dot(color=RED)
        dot.add_updater(lambda m: m.move_to(
            np.array([
                a * tracker.get_value() * np.cos(tracker.get_value()),
                a * tracker.get_value() * np.sin(tracker.get_value()),
                0
            ])
        ))
        path = TracedPath(dot.get_center, stroke_color=RED, stroke_width=2)
        self.add(spiral, dot, path)
        # 7. Animate drawing
        self.play(tracker.animate.set_value(4 * PI),
                  run_time=8,
                  rate_func=rate_functions.ease_in_out_sine)
        self.wait(2)