import random
import numpy as np
from manim import *

class MonteCarloPiApproximation(Scene):
    def construct(self):
        # Setup
        plane_size = 4
        radius = plane_size / 2
        dot_radius = 0.03
        num_points = 2000
        animation_runtime = 0.05  # Time per point addition

        # Create axes and square
        axes = Axes(
            x_range=[0, plane_size, 1],
            y_range=[0, plane_size, 1],
            x_length=plane_size,
            y_length=plane_size,
            tips=False,
        ).shift(UP * 0.5) # Shift up slightly to make space for text

        square = Square(side_length=plane_size).move_to(axes.c2p(radius, radius))

        # Create quarter circle (Sector)
        circle_sector = Sector(
            radius=radius,
            angle=PI/2,
            start_angle=0,
            arc_center=axes.c2p(0, 0),
            fill_opacity=0.3,
            color=BLUE,
            stroke_width=0
        )

        # Title and explanation text
        title = Tex("Monte Carlo Approximation of ", r"$\pi$").scale(0.8).to_edge(UP)
        explanation = Tex(
            r"1. Generate random points $(x, y)$ in the square.",
            r"2. Check if $x^2 + y^2 \leq r^2$.",
            r"3. $\frac{\text{Points inside circle}}{\text{Total points}} \approx \frac{\text{Area of quarter circle}}{\text{Area of square}} = \frac{\pi r^2 / 4}{r^2} = \frac{\pi}{4}$",
            r"4. $\pi \approx 4 \times \frac{\text{Points inside}}{\text{Total points}}$"
        ).scale(0.6).next_to(axes, DOWN, buff=0.5).align_to(axes, LEFT)
        explanation.shift(RIGHT*0.5) # Adjust position

        self.play(Write(title))
        self.play(Create(axes), Create(square), Create(circle_sector))
        self.play(Write(explanation[0]))
        self.wait(1)

        # Counters and Pi display
        points_inside = 0
        total_points = 0
        points_group = VGroup() # Group for dots
        inside_dots_group = VGroup()
        outside_dots_group = VGroup()

        pi_label = Tex(r"$\pi \approx$ ", font_size=40)
        pi_value = DecimalNumber(0, num_decimal_places=5, font_size=40)
        pi_display = VGroup(pi_label, pi_value).arrange(RIGHT).next_to(explanation, DOWN, buff=0.5)

        count_label_inside = Tex("Inside: ", font_size=30)
        count_value_inside = Integer(0, font_size=30)
        count_display_inside = VGroup(count_label_inside, count_value_inside).arrange(RIGHT)

        count_label_total = Tex("Total: ", font_size=30)
        count_value_total = Integer(0, font_size=30)
        count_display_total = VGroup(count_label_total, count_value_total).arrange(RIGHT)

        counts_display = VGroup(count_display_inside, count_display_total).arrange(RIGHT, buff=0.5)
        counts_display.next_to(pi_display, DOWN, buff=0.3).align_to(pi_display, LEFT)

        self.play(Write(pi_display), Write(counts_display))
        self.wait(1)
        self.play(Write(explanation[1]))
        self.wait(1)

        # Monte Carlo Simulation
        for i in range(num_points):
            total_points += 1
            x = random.uniform(0, plane_size)
            y = random.uniform(0, plane_size)
            point_coords = axes.c2p(x, y)
            dot = Dot(point_coords, radius=dot_radius)

            # Check if inside the quarter circle (using origin at axes.c2p(0,0))
            if x**2 + y**2 <= radius**2:
                points_inside += 1
                dot.set_color(GREEN)
                inside_dots_group.add(dot)
            else:
                dot.set_color(RED)
                outside_dots_group.add(dot)

            points_group.add(dot) # Add to the main group for animation

            # Update approximation
            if total_points > 0:
                pi_approx = 4 * points_inside / total_points
            else:
                pi_approx = 0

            # Update display values - use change_value for smooth updates if possible, else set_value
            self.play(
                FadeIn(dot, scale=0.5, run_time=animation_runtime),
                pi_value.animate.set_value(pi_approx),
                count_value_inside.animate.set_value(points_inside),
                count_value_total.animate.set_value(total_points),
            )

            # Show explanation steps progressively
            if i == int(num_points * 0.3):
                 self.play(Write(explanation[2]), run_time=0.5)
            if i == int(num_points * 0.6):
                 self.play(Write(explanation[3]), run_time=0.5)


        self.wait(2) # Hold the final frame

        # Final emphasis on the formula and result
        final_pi_approx = 4 * points_inside / total_points
        final_result_tex = MathTex(
            r"\pi \approx 4 \times \frac{" + str(points_inside) + r"}{" + str(total_points) + r"} \approx " + f"{final_pi_approx:.4f}",
            font_size=48
        ).next_to(pi_display, UP, buff=1.0) # Position above the running counter

        self.play(ReplacementTransform(explanation[3].copy(), final_result_tex))
        self.play(Circumscribe(final_result_tex, color=YELLOW))
        self.wait(3)