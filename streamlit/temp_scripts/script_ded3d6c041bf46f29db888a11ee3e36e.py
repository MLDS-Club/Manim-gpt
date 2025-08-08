from manim import *

class TorqueWheelScene(Scene):
    def construct(self):
        # Draw wheel and axle
        wheel = Circle(radius=2, color=WHITE)
        axle = Dot(ORIGIN, color=GRAY)
        self.play(Create(wheel), FadeIn(axle), run_time=2)
        self.wait()

        # Show radius vector r
        r_line = Line(ORIGIN, 2 * RIGHT, color=YELLOW)
        r_label = MathTex("r").set_color(YELLOW).next_to(r_line.get_midpoint(), DOWN)
        self.play(Create(r_line), Write(r_label), run_time=1.5)
        self.wait()

        # Show force arrow F tangent to rim
        force_point = 2 * RIGHT
        force_arrow = Arrow(force_point, force_point + 1.5 * UP, color=RED, buff=0)
        F_label = MathTex("F").set_color(RED).next_to(force_arrow.get_end(), RIGHT)
        self.play(GrowArrow(force_arrow), Write(F_label), run_time=1.5)
        self.wait()

        # Animate torque vector tau out of plane
        tau_len = ValueTracker(0)
        tau_arrow = always_redraw(
            lambda: Arrow(
                ORIGIN,
                OUT * tau_len.get_value(),
                color=BLUE,
                buff=0,
            )
        )
        tau_label = always_redraw(
            lambda: MathTex(r"\tau").set_color(BLUE).next_to(
                tau_arrow.get_end(), UP
            )
        )
        self.add(tau_arrow, tau_label)
        self.play(tau_len.animate.set_value(1.5), run_time=2)
        self.wait()

        # Formula derivation on screen
        step1 = MathTex(r"\tau = r \times F", color=WHITE).to_corner(UR)
        step2 = MathTex(r"= (2)(F)\sin(90^\circ)", color=WHITE).next_to(
            step1, DOWN, aligned_edge=LEFT
        )
        step3 = MathTex(r"= 2F", color=WHITE).next_to(
            step2, DOWN, aligned_edge=LEFT
        )
        self.play(Write(step1))
        self.wait(0.5)
        self.play(Write(step2))
        self.wait(0.5)
        self.play(Write(step3))
        self.wait(2)

        # Rotate wheel to illustrate effect of torque
        self.play(
            Rotate(
                wheel,
                angle=-PI / 2,
                about_point=ORIGIN,
                rate_func=linear,
            ),
            run_time=3,
        )
        self.wait(2)
```

Explanation of Scenes:
1. We draw a wheel (circle) and its axle (dot).
2. We add the radius vector r to the right.
3. We show a tangent force F upward on the rim.
4. We animate the resulting torque vector τ coming out of the page.
5. We derive τ = r × F = (2)(F)sin90° = 2F step-by-step.
6. Finally, we rotate the wheel around its center to show how torque causes rotation.