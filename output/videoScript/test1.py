from manim import *

class FrustumVolume(ThreeDScene):
    def construct(self):
        # Define frustum parameters
        r_top = 2
        r_bottom = 4
        height = 5

        # Calculate volume
        volume = (1/3) * PI * height * (r_bottom**2 + r_bottom * r_top + r_top**2)

        # Create 3D axes
        axes = ThreeDAxes()

        # Create frustum
        frustum = Prism(dimensions=[r_bottom*2, r_top*2, height])
        frustum.set_fill(BLUE, opacity=0.5)

        # Create labels
        r_top_label = MathTex("r_{top} = 2").to_edge(UP).shift(LEFT*2)
        r_bottom_label = MathTex("r_{bottom} = 4").next_to(r_top_label, DOWN)
        height_label = MathTex("h = 5").next_to(r_bottom_label, DOWN)
        volume_label = MathTex(f"V = \\frac{{1}}{{3}} \\pi h (r_{{bottom}}^2 + r_{{bottom}}r_{{top}} + r_{{top}}^2)").next_to(height_label, DOWN)
        volume_value = MathTex(f"V \\approx {volume:.2f}").next_to(volume_label, DOWN)

        # Initial setup
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
        self.add(axes)

        # Show frustum and labels
        self.play(Create(frustum))
        self.play(Write(r_top_label), Write(r_bottom_label), Write(height_label))
        self.wait(1)

        # Show volume formula and value
        self.play(Write(volume_label))
        self.play(Write(volume_value))
        self.wait(2)

        self.move_camera(phi=60*DEGREES, theta=-60*DEGREES)
        self.wait(1)