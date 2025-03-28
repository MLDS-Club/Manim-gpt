from manim import *
import random

class MonteCarloPi(Scene):
    def construct(self):
        # Title
        title = Text("Approximating Pi using Monte Carlo").to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Setup square and circle centered at origin
        center_point = ORIGIN + LEFT * 2.5 # Shift setup to the left
        # Use radius=2 for circle, side_length=4 for square to make calculations easy (pi*r^2 / (2r)^2 = pi*4 / 16 = pi/4)
        radius = 2.0
        square_side = 2 * radius

        square = Square(side_length=square_side, stroke_width=3, color=BLUE).move_to(center_point)
        circle = Circle(radius=radius, stroke_width=3, color=YELLOW).move_to(center_point)

        # Create axes for context
        axes = Axes(
            x_range=[-radius*1.1, radius*1.1, 1], # Extend range slightly
            y_range=[-radius*1.1, radius*1.1, 1],
            x_length=square_side * 1.1, # Match visual size
            y_length=square_side * 1.1,
            axis_config={"include_numbers": True, "stroke_width": 2, "font_size": 20},
            tips=False, # Remove arrow tips for cleaner look
        ).move_to(center_point)

        setup_group = VGroup(axes, square, circle)
        self.play(Create(axes), Create(square), Create(circle))
        self.wait(0.5)

        # Simulation Setup
        n_points = 1000 # Number of points
        points_inside_circle = 0
        dot_radius = 0.03
        update_frequency = 25 # Update text every 25 points

        # Text for counts and Pi approximation
        total_label = Text("Total Points:", font_size=24)
        inside_label = Text("Points Inside:", font_size=24)
        pi_label = MathTex(r"\pi \approx", font_size=30)

        # Use Integer for counts, DecimalNumber for pi approx
        total_count = Integer(0, font_size=24)
        inside_count = Integer(0, font_size=24)
        pi_value = DecimalNumber(0.0, num_decimal_places=5, font_size=30)

        # Arrange text elements using VGroup and arrange
        stat_total = VGroup(total_label, total_count).arrange(RIGHT, buff=0.15)
        stat_inside = VGroup(inside_label, inside_count).arrange(RIGHT, buff=0.15)
        stat_pi = VGroup(pi_label, pi_value).arrange(RIGHT, buff=0.15)

        stats_group = VGroup(stat_total, stat_inside, stat_pi).arrange(
            DOWN, aligned_edge=LEFT, buff=0.25
        ).next_to(setup_group, RIGHT, buff=0.5)

        self.play(Write(stats_group))
        self.wait(0.5)

        # Simulation Loop
        dots_group = VGroup() # Group to hold all dots

        # Use ValueTrackers for smooth updates of the numbers
        vt_total = ValueTracker(0)
        vt_inside = ValueTracker(0)
        vt_pi = ValueTracker(0.0)

        # Link Integer/DecimalNumber to ValueTrackers using updaters
        total_count.add_updater(lambda m: m.set_value(int(vt_total.get_value())))
        inside_count.add_updater(lambda m: m.set_value(int(vt_inside.get_value())))
        pi_value.add_updater(lambda m: m.set_value(vt_pi.get_value()))

        # Add the number Mobjects to the scene so the updaters take effect
        self.add(total_count, inside_count, pi_value)

        anim_list = [] # Store dot creation animations to play in batches

        for i in range(1, n_points + 1):
            # Generate random point within the square [-radius, radius] x [-radius, radius]
            x = random.uniform(-radius, radius)
            y = random.uniform(-radius, radius)
            dot_pos = axes.coords_to_point(x, y)
            dot = Dot(point=dot_pos, radius=dot_radius)

            # Check if inside circle (radius r)
            if x**2 + y**2 <= radius**2:
                points_inside_circle += 1
                dot.set_color(GREEN)
            else:
                dot.set_color(RED)

            dots_group.add(dot)
            # Create animation for the dot, don't play yet
            anim_list.append(FadeIn(dot, scale=0.3, run_time=0.05)) # Fast fade in for each dot

            # Update counts and Pi approximation periodically using ValueTrackers
            if i % update_frequency == 0 or i == n_points:
                pi_approx = 4 * points_inside_circle / i if i > 0 else 0.0

                # Play dot animations accumulated so far along with number updates
                self.play(*anim_list, # Unpack the list of dot animations
                          vt_total.animate.set_value(i),
                          vt_inside.animate.set_value(points_inside_circle),
                          vt_pi.animate.set_value(pi_approx),
                          run_time=0.2 # Adjust run_time for the combined update animation
                         )
                anim_list = [] # Reset animation list for the next batch

        # Ensure all remaining dots are animated if n_points is not a multiple of update_frequency
        if anim_list:
             self.play(*anim_list, run_time=0.1) # Play any remaining dot animations

        # Remove updaters after simulation is complete
        total_count.remove_updater()
        inside_count.remove_updater()
        pi_value.remove_updater()
        self.wait(1)

        # Final Pi approximation formula explanation
        explanation_text = VGroup(
             MathTex(r"\frac{\text{Points Inside}}{\text{Total Points}}", r"\approx", r"\frac{\text{Area(Circle)}}{\text{Area(Square)}}", font_size=28),
             # Break down the area ratio calculation
             MathTex(r"\frac{\text{Area(Circle)}}{\text{Area(Square)}}", r"=", r"\frac{\pi r^2}{(2r)^2}", r"=", r"\frac{\pi r^2}{4 r^2}", r"=", r"\frac{\pi}{4}", font_size=28),
             # Final formula for Pi
             MathTex(r"\implies \pi \approx 4 \times \frac{\text{Points Inside}}{\text{Total Points}}", font_size=28)
        ).arrange(DOWN, buff=0.3).next_to(stats_group, DOWN, buff=0.4, aligned_edge=LEFT)

        # Animate the explanation step-by-step
        self.play(Write(explanation_text[0]))
        self.wait(1.5)
        self.play(Write(explanation_text[1]))
        self.wait(2)
        self.play(Write(explanation_text[2]))

        self.wait(3)