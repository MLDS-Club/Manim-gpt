from manim import *

class FrustumVolume(ThreeDScene):
    def construct(self):
        # Define frustum parameters
        top_radius = 2
        bottom_radius = 4
        height = 5

        # Create frustum
        frustum = Prism(dimensions=[2 * bottom_radius, 2 * bottom_radius, 0.1]).set_color(BLUE)
        top_circle = Circle(radius=top_radius).set_color(YELLOW).move_to([0,0,height])
        bottom_circle = Circle(radius=bottom_radius).set_color(YELLOW)

        def get_frustum(alpha):
            h = interpolate(0, height, alpha)
            r = interpolate(bottom_radius, top_radius, alpha)
            c = Circle(radius=r).set_color(YELLOW).move_to([0,0,h])
            return Surface(
                lambda u, v: [
                    (bottom_radius + (top_radius-bottom_radius) * v/height) * np.cos(u),
                    (bottom_radius + (top_radius-bottom_radius) * v/height) * np.sin(u),
                    v
                ],
                u_range=[0, 2 * PI],
                v_range=[0,h]
            ).set_color(BLUE)

        frustum = always_redraw(lambda: get_frustum(1))

        # Create axes
        axes = ThreeDAxes()
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)

        # Show frustum creation
        self.add(axes)
        self.play(Create(bottom_circle))
        self.play(Create(frustum), run_time=3)
        self.play(Create(top_circle))

        self.wait(1)

        # Calculate volume
        volume = (1/3) * PI * height * (top_radius**2 + top_radius * bottom_radius + bottom_radius**2)

        # Display volume
        volume_text = MathTex(r"V = \frac{1}{3} \pi h (r_1^2 + r_1 r_2 + r_2^2)").to_edge(UP)
        volume_value = MathTex(r"V = \frac{1}{3} \pi (5) (2^2 + 2 \cdot 4 + 4^2)").next_to(volume_text, DOWN)
        volume_result = MathTex(f"V \\approx {volume:.2f} \\text{{ m}}^3").next_to(volume_value, DOWN)

        self.play(Write(volume_text))
        self.play(Write(volume_value))
        self.play(Write(volume_result))

        self.wait(2)