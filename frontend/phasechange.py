from manim import *

class XorGate(Scene):
    def construct(self):
        # Gate dimensions and coordinates
        left_x = -2
        right_x = 1.5
        top_y = 1.5
        bottom_y = -1.5
        input_x = left_x - 1
        output_x = right_x + 1

        # Input lines
        input_A = Line([input_x, top_y, 0], [left_x, top_y, 0])
        input_B = Line([input_x, bottom_y, 0], [left_x, bottom_y, 0])
        # Output line
        output_line = Line([right_x, 0, 0], [output_x, 0, 0])

        # XOR gate curves: two back curves and the front OR curves
        back1 = CubicBezier(
            [left_x + 0.3, top_y, 0],
            [left_x - 1, top_y, 0],
            [left_x - 1, bottom_y, 0],
            [left_x + 0.3, bottom_y, 0],
        )
        back2 = CubicBezier(
            [left_x, top_y, 0],
            [left_x - 1, top_y, 0],
            [left_x - 1, bottom_y, 0],
            [left_x, bottom_y, 0],
        )
        front_upper = CubicBezier(
            [left_x, top_y, 0],
            [1, top_y + 0.5, 0],
            [right_x, top_y - 0.5, 0],
            [right_x, 0, 0],
        )
        front_lower = CubicBezier(
            [right_x, 0, 0],
            [right_x, bottom_y + 0.5, 0],
            [1, bottom_y - 0.5, 0],
            [left_x, bottom_y, 0],
        )
        gate = VGroup(back1, back2, front_upper, front_lower)
        gate.set_stroke(width=4)

        # Labels for inputs and output
        label_A = Tex("A").next_to(input_A.get_start(), LEFT)
        label_B = Tex("B").next_to(input_B.get_start(), LEFT)
        label_out = MathTex(r"A \oplus B").next_to(output_line.get_end(), RIGHT)

        # Assemble scene
        self.add(input_A, input_B, output_line, gate, label_A, label_B, label_out)
        self.wait()