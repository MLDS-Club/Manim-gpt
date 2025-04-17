from manim import *
import numpy as np
import random

class WingLiftVisualization(Scene):
    def construct(self):
        # RANDOMLY CHOSEN VALUES
        # Wind speed
        v_mph = 500 # miles per hour
        v = v_mph * 0.44704  # m/s conversion
        # Chord length of wing (front to back)
        c = random.choice([1.5, 2.0, 2.5]) # meters
        # Wingspan (tip to tip)
        b = random.choice([28, 32, 36]) # meters
        # Air density at sea level
        rho = 1.225 # kg/m^3
        # Typical lift coefficient for an airliner wing at takeoff
        Cl = round(random.uniform(1.1, 1.3), 2)
        # Area
        S = c * b

        top_buffer = 0.75
        left = -6
        right = 6
        bot = -3
        top = 3

        # Title
        title = Text("How much upward force on an airplane wing in 500 mph winds?", font_size=38)
        title.to_edge(UP)
        self.play(Write(title), run_time=1.3)
        self.wait(0.4)

        # Draw a wing (airfoil shape)
        airfoil = VMobject()
        airfoil.set_points_smoothly([
            [-3, 0, 0], [-2, 0.45, 0], [1.7, 1, 0],  [3, 0.4, 0],
            [3, -0.3, 0], [1.5, -0.5, 0], [-2, -0.2, 0], [-3, 0, 0]
        ])
        airfoil.set_color(GRAY_C).set_fill(GRAY_E, opacity=0.5).set_stroke(WHITE, width=2)
        airfoil.shift(DOWN*0.5)

        # Annotate chord and span
        chord_line = always_redraw(lambda: Line([-3, 0, 0], [3, 0, 0], color=BLUE, stroke_width=4).shift(DOWN*0.5))
        chord_label = MathTex("c", font_size=36, color=BLUE).next_to(chord_line, UP, buff=0.1)
        span_brace = Brace(airfoil, direction=LEFT, color=TEAL)
        span_label = MathTex("b", font_size=36, color=TEAL).next_to(span_brace, LEFT, buff=0.1)
        
        self.play(FadeIn(airfoil), FadeIn(chord_line), FadeIn(chord_label), FadeIn(span_brace), FadeIn(span_label), run_time=1)
        self.wait(0.3)

        # Streamlines above and below airfoil
        def wind_field(pos):
            # Add stream curvature: slightly up over the wing, slightly down below
            x, y = pos[0], pos[1]
            if abs(y) < 0.8 and -3.2 < x < 3.2:
                turn = 0.6 * (np.exp(-4*(y-0.39)**2) - np.exp(-4*(y+0.39)**2))
            else:
                turn = 0
            return np.array([3, turn, 0])
        
        stream = StreamLines(
            wind_field, 
            x_range=[left, right, 0.32], 
            y_range=[bot + 0.8, top - top_buffer, 0.18],
            color_scheme=lambda v: v[1],  # Color by vertical component
            max_anchors_per_line=24,
            virtual_time=1.5,
            stroke_width=2.5
        )
        stream.move_to(DOWN*0.5)
        self.play(Create(stream), run_time=2.0)
        self.wait(0.5)
        
        # Overlay: Show high/low pressure regions
        high_press_circle = Circle(radius=0.2, color="#ff6666", fill_opacity=0.55).move_to([-1.7, -0.9, 0])
        low_press_circle = Circle(radius=0.4, color="#66ccff", fill_opacity=0.35).move_to([1.6, 1, 0])

        high_press_label = MathTex(r"\text{High }P", font_size=34, color=BLACK).move_to(high_press_circle)
        low_press_label = MathTex(r"\text{Low }P", font_size=34, color=BLACK).move_to(low_press_circle)

        self.play(
            FadeIn(high_press_circle), FadeIn(high_press_label), 
            FadeIn(low_press_circle), FadeIn(low_press_label), run_time=0.7)
        self.wait(0.3)

        # Remove visual clutter before equations
        self.play(*[FadeOut(mob) for mob in [chord_line, chord_label, span_brace, span_label, high_press_circle, high_press_label, low_press_circle, low_press_label]], run_time=0.7)

        # Show the lift equation
        eq1 = MathTex(
            r"L = C_L \cdot \frac{1}{2} \rho v^2 S",
            font_size=48
        ).to_edge(UP).shift(DOWN*0.1)
        variables1 = VGroup(
            MathTex(r"C_L\: \text{(lift coefficient)}", font_size=34, color="#FFC857"),
            MathTex(r"\rho = 1.225\; \mathrm{kg/m}^3", font_size=34, color="#348AA7"),
            MathTex(r"v = " + f"{v:.1f}" + r"\; \mathrm{m/s}", font_size=34, color="#525174"),
            MathTex(r"S = c \times b\: \text{(area)}", font_size=34, color="#F76E5C"),
        )
        variables1.arrange(DOWN, aligned_edge=LEFT).next_to(eq1, DOWN, buff=0.43).align_to(eq1, LEFT)

        self.play(Write(eq1), run_time=0.9)
        self.play(LaggedStartMap(FadeIn, variables1, lag_ratio=0.21), run_time=1.2)
        self.wait(0.8)

        # Substitute concrete values
        eq2 = MathTex(
            rf"L = {Cl} \cdot \frac12 \cdot {rho} \cdot ({v:.1f})^2 \cdot {S:.1f}",
            font_size=48
        ).next_to(eq1, DOWN, buff=0.91).align_to(eq1, LEFT)
        eq_arrow = Arrow(eq1.get_bottom(), eq2.get_top(), color=YELLOW).scale(0.8)
        self.play(
            GrowArrow(eq_arrow),
            Write(eq2),
            run_time=1.2
        )
        self.wait(0.65)

        # Step-by-step computation, appearing below
        step1 = MathTex(
            r"{L} = " + f"{Cl:.2f} \\times 0.5 \\times {rho} \\times {v:.1f}^2 \\times {S:.1f}",
            font_size=44
        )
        intermediate_val = 0.5 * rho * v**2 * S
        step2 = MathTex(
            r"= " + f"{Cl:.2f}\\times " + f"{intermediate_val:,.0f}",
            font_size=44
        )
        L_val = Cl * 0.5 * rho * v**2 * S
        step3 = MathTex(
            r"= " + f"{L_val:,.0f}~\mathrm{{N}}",
            font_size=52,
            color="#6D9C3D"
        )

        VGroup(step1, step2, step3).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        step1.next_to(eq2, DOWN, buff=0.4).align_to(eq2, LEFT)
        step2.next_to(step1, DOWN, buff=0.15).align_to(step1, LEFT)
        step3.next_to(step2, DOWN, buff=0.23).align_to(step2, LEFT)

        # Animate these stepwise
        self.play(FadeIn(step1), run_time=0.9)
        self.wait(0.4)
        self.play(FadeIn(step2), run_time=0.9)
        self.wait(0.6)
        self.play(FadeIn(step3), Indicate(step3, color=YELLOW), run_time=1.0)
        self.wait(1.1)

        # Call-out with value
        lift_newtons = L_val
        lift_pounds = lift_newtons / 4.448  # approx N to lb
        lift_box = VGroup(
            Text("Total upward force on one wing:", font_size=32),
            MathTex(
                rf"{lift_newtons:,.0f}\;N~~ (\approx {lift_pounds:,.0f}\;\mathrm{{lb}})",
                font_size=50, color=GREEN_B
            )
        ).arrange(DOWN, aligned_edge=LEFT)
        rect = SurroundingRectangle(lift_box, color=GREEN_B, buff=0.35)
        lift_box.next_to(step3, DOWN, buff=1.05)
        
        self.play(FadeIn(lift_box), Create(rect), run_time=1.1)
        self.wait(2.3)

        # Fade out everything, focus on FLOW
        to_fade = self.mobjects.copy()
        self.play(*[FadeOut(m) for m in to_fade if m is not stream], run_time=0.9)
        self.wait(0.2)

        # Animate flow around airfoil again, zooming in
        self.camera.frame.save_state()
        self.play(self.camera.frame.animate.set(width=7).move_to(airfoil), run_time=1.2)
        self.wait(0.2)
        # Add labels: Fast flow + Low pressure, Slow flow + High pressure
        top_label = Text("Fast flow\nLow pressure", font_size=32, color=BLUE).next_to(airfoil, UP+RIGHT, buff=0.34)
        bot_label = Text("Slow flow\nHigh pressure", font_size=32, color=RED_B).next_to(airfoil, DOWN+LEFT, buff=0.34)
        self.play(FadeIn(top_label), FadeIn(bot_label), run_time=0.8)
        self.wait(1.7)

        # End
        self.wait(0.5)
        self.play(*[FadeOut(m) for m in self.mobjects], Restore(self.camera.frame), run_time=1.2)

        outro = Text("Lift comes from\npressure difference\ncreated by airflow!", font_size=44, color=YELLOW).move_to(ORIGIN)
        self.play(Write(outro), run_time=1.3)
        self.wait(1.5)