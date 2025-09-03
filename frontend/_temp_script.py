from manim import *
import numpy as np

class OrGate(Scene):
    def construct(self):
        # Define key points
        TL = np.array([-1.5,  1.5, 0])
        BL = np.array([-1.5, -1.5, 0])
        TR = np.array([ 2.0,  1.5, 0])
        BR = np.array([ 2.0, -1.5, 0])
        # Control points for smooth Bezier arcs
        top_ctrl1    = np.array([ 0.0,  2.5, 0])
        top_ctrl2    = np.array([ 1.5,  2.5, 0])
        right_ctrl1  = np.array([ 3.0,  1.5, 0])
        right_ctrl2  = np.array([ 3.0, -1.5, 0])
        bottom_ctrl1 = np.array([ 1.5, -2.5, 0])
        bottom_ctrl2 = np.array([ 0.0, -2.5, 0])
        left_ctrl1   = np.array([-0.5,  0.3, 0])
        left_ctrl2   = np.array([-0.5, -0.3, 0])

        # Gate outline (four CubicBezier segments)
        top   = CubicBezier(TL, top_ctrl1,    top_ctrl2,    TR).set_stroke(width=4)
        right = CubicBezier(TR, right_ctrl1,  right_ctrl2,  BR).set_stroke(width=4)
        bot   = CubicBezier(BR, bottom_ctrl1, bottom_ctrl2, BL).set_stroke(width=4)
        left  = CubicBezier(BL, left_ctrl1,   left_ctrl2,   TL).set_stroke(width=4)
        gate_outline = VGroup(top, right, bot, left)

        # Input/output lines
        in_A = Line(np.array([-3.0,  1.0, 0]), TL, stroke_width=4)
        in_B = Line(np.array([-3.0, -1.0, 0]), BL, stroke_width=4)
        outY = Line(np.array([ 2.0,  0.0, 0]), np.array([3.5, 0.0, 0]), stroke_width=4)

        # Labels
        lbl_A = Tex("A").next_to(in_A.get_start(), LEFT)
        lbl_B = Tex("B").next_to(in_B.get_start(), LEFT)
        lbl_Y = Tex("Y").next_to(outY.get_end(), RIGHT)

        # Compose and show
        self.add(gate_outline, in_A, in_B, outY, lbl_A, lbl_B, lbl_Y)
        self.wait(2)
```

This Manim 0.19.0 scene hand‑draws a smooth OR‑gate outline with cubic Bézier curves, adds input/output wires, and labels A, B, and Y.