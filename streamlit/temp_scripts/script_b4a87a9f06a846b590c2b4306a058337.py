from manim import (
    Scene, Circle, Square, Dot,
    ValueTracker, always_redraw,
    MathTex, Create, Write
)
from manim import WHITE, YELLOW, GREEN, RED, UL, UR, DOWN
import random

class MonteCarloPiDemo(Scene):
    def construct(self):
        # 1. Draw square and inscribed circle
        square = Square(side_length=2, color=WHITE)
        circle = Circle(radius=1, color=YELLOW)
        self.play(Create(square), Create(circle), run_time=2)
        self.wait(1)

        # 2. Show formula π ≈ 4 * (In/Total)
        formula = MathTex(
            r"\pi \approx 4 \times \frac{\text{In}}{\text{Total}}",
            font_size=36
        ).to_edge(DOWN)
        self.play(Write(formula), run_time=1)
        self.wait(1)

        # 3. Set up ValueTrackers for counts
        count_in = ValueTracker(0)
        count_total = ValueTracker(0)

        # 4. Dynamic text: In count (top-left)
        in_text = always_redraw(lambda: MathTex(
            f"In: {int(count_in.get_value())}",
            font_size=24, color=GREEN
        ).to_corner(UL))

        # 5. Dynamic text: Out count (below In)
        out_text = always_redraw(lambda: MathTex(
            f"Out: {int(count_total.get_value() - count_in.get_value())}",
            font_size=24, color=RED
        ).next_to(in_text, DOWN))

        # 6. Dynamic text: π approximation (top-right)
        pi_text = always_redraw(lambda: MathTex(
            r"\pi \approx "
            + (
                f"{4*count_in.get_value()/count_total.get_value():.4f}"
                if count_total.get_value() > 0 else "?"
            ),
            font_size=24
        ).to_corner(UR))

        # 7. Add trackers and dynamic texts to scene
        self.add(count_in, count_total)
        self.add(in_text, out_text, pi_text)
        self.wait(1)

        # 8. Monte Carlo sampling
        N = 200
        for _ in range(N):
            x, y = random.uniform(-1,1), random.uniform(-1,1)
            inside = x*x + y*y <= 1
            point = Dot(
                point=[x, y, 0],
                radius=0.02,
                color=(GREEN if inside else RED)
            )
            self.add(point)
            count_total.increment_value(1)
            if inside:
                count_in.increment_value(1)
            self.wait(0.05)

        self.wait(2)