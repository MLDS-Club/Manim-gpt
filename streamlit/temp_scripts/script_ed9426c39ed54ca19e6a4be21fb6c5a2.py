from manim import *

class MassDistributionRocketScene(Scene):
    def construct(self):
        # Draw rocket components
        bottom = Rectangle(width=1, height=2).set_fill(BLUE, opacity=1).set_stroke(WHITE, width=1).shift(DOWN)
        middle = Rectangle(width=1, height=1.5).set_fill(YELLOW, opacity=1).set_stroke(WHITE, width=1).shift(UP*0.75)
        nose = Polygon(
            [-0.5,1.5,0], [0.5,1.5,0], [0,2.5,0]
        ).set_fill(GRAY, opacity=1).set_stroke(WHITE, width=1)
        fin_left = Polygon(
            [-0.5,-1,0], [-1.5,-2,0], [-0.5,-2,0]
        ).set_fill(RED, opacity=1).set_stroke(WHITE, width=1)
        fin_right = Polygon(
            [0.5,-1,0], [1.5,-2,0], [0.5,-2,0]
        ).set_fill(RED, opacity=1).set_stroke(WHITE, width=1)
        rocket = VGroup(bottom, middle, nose, fin_left, fin_right).move_to(ORIGIN)

        # Animate rocket drawing
        self.play(
            Create(bottom),
            Create(middle),
            Create(nose),
            Create(fin_left),
            Create(fin_right),
            run_time=2
        )
        self.wait(1)

        # Label masses m1, m2, m3
        m1_label = MathTex(r"m_1").next_to(bottom, LEFT)
        m2_label = MathTex(r"m_2").next_to(middle, LEFT)
        m3_label = MathTex(r"m_3").next_to(nose, RIGHT)
        self.play(Write(m1_label), Write(m2_label), Write(m3_label), run_time=1)
        self.wait(1)

        # Show center positions y1, y2, y3
        y1 = -1
        y2 = 0.75
        y3 = 2.0
        y1_label = MathTex(r"y_1=-1").next_to(m1_label, DOWN)
        y2_label = MathTex(r"y_2=0.75").next_to(m2_label, DOWN)
        y3_label = MathTex(r"y_3=2").next_to(m3_label, DOWN)
        self.play(Write(y1_label), Write(y2_label), Write(y3_label), run_time=1)
        self.wait(1)

        # Display COM formula
        com_formula = MathTex(
            r"y_{COM} = \frac{m_1 y_1 + m_2 y_2 + m_3 y_3}{m_1 + m_2 + m_3}"
        ).to_corner(UR)
        self.play(Write(com_formula), run_time=2)
        self.wait(1)

        # Initial numeric substitution
        subs = MathTex(
            r"= \frac{1 \cdot (-1) + 0.5 \cdot 0.75 + 0.2 \cdot 2}{1 + 0.5 + 0.2}"
        ).next_to(com_formula, DOWN)
        self.play(Write(subs), run_time=2)
        self.wait(1)

        result_val = (-1 + 0.375 + 0.4) / (1 + 0.5 + 0.2)
        result = MathTex(f"= {result_val:.3f}").next_to(subs, DOWN)
        self.play(Write(result), run_time=1)
        self.wait(1)

        # ValueTrackers for dynamic mass m1
        m1_tracker = ValueTracker(1.0)
        m2_val = 0.5
        m3_val = 0.2

        # Dynamic COM dot and formula
        def compute_com():
            return (m1_tracker.get_value() * y1 + m2_val * y2 + m3_val * y3) / (
                m1_tracker.get_value() + m2_val + m3_val
            )
        com_dot = always_redraw(lambda: Dot(color=RED).move_to(
            rocket.get_center() + UP * compute_com()
        ))
        com_text = always_redraw(lambda: MathTex(
            f"y_{{COM}}={compute_com():.3f}"
        ).to_corner(UR))
        self.add(com_dot, com_text)
        self.wait(1)

        # Animate fuel consumption (m1 decreases)
        self.play(
            m1_tracker.animate.set_value(0.1),
            run_time=4,
            rate_func=linear
        )
        self.wait(2)