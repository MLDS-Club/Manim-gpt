from manim import *

class SineOf30(Scene):
    def construct(self):
        # Create a unit circle
        circle = Circle(radius=1.5)
        self.play(Create(circle))

        # Create axes
        axes = Axes(x_range=[-2, 2], y_range=[-2, 2])
        self.play(Create(axes))

        # Add labels for the axes
        x_label = axes.get_x_axis_label("x")
        y_label = axes.get_y_axis_label("y")
        self.play(Write(x_label), Write(y_label))

        # Create a 30-degree angle line
        angle = 30 * DEGREES
        line = Line(ORIGIN, circle.point_at_angle(angle), color=YELLOW)
        self.play(Create(line))

        # Create a brace for the angle
        angle_brace = Angle(axes.x_axis, line, radius=0.5, other_angle=False)
        self.play(Create(angle_brace))

        # Add a label for the angle
        angle_text = MathTex(r"30^\circ").next_to(angle_brace, UR, buff=0.1)
        self.play(Write(angle_text))

        # Create a vertical line for the sine value
        sine_line = Line(line.get_end(), [line.get_end()[0],0,0], color=GREEN)
        self.play(Create(sine_line))

        # Add a label for the sine value
        sine_label = MathTex(r"\sin(30^\circ)", color=GREEN).next_to(sine_line, RIGHT)
        self.play(Write(sine_label))

        # Calculate the sine value
        sine_value = np.sin(angle)

        # Display the sine value
        sine_value_text = MathTex(r"\sin(30^\circ) = 0.5").to_edge(UP, buff=1)
        self.play(Write(sine_value_text))

        self.wait(2)