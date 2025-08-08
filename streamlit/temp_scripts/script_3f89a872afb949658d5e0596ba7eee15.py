from manim import *

class XorGateDemo(Scene):
    def construct(self):
        # Title
        title = Text("XOR Gate Demonstration", font_size=60)
        title.to_edge(UP)
        self.play(Write(title), run_time=1.5)

        # Truth table setup
        table_data = [
            ["A", "B", "Y"],
            ["0", "0", "0"],
            ["0", "1", "1"],
            ["1", "0", "1"],
            ["1", "1", "0"],
        ]
        table = MathTable(
            table_data,
            include_outer_lines=True,
            line_config={"stroke_width": 2}
        ).scale(0.8)
        table.next_to(title, DOWN, buff=1)
        self.play(Create(table), run_time=1)

        # Highlight rows + input/output indicator circles
        row_tracker = ValueTracker(0)
        highlight = always_redraw(lambda: SurroundingRectangle(
            table.get_rows()[int(row_tracker.get_value()) + 1],
            color=YELLOW, buff=0.1
        ))
        self.play(Create(highlight), run_time=1)

        circles = VGroup(*[Circle(radius=0.3) for _ in range(3)])
        circles.arrange(RIGHT, buff=1.2).next_to(table, RIGHT, buff=2)
        labels = VGroup(*[Text(l, font_size=30) for l in ["A","B","Y"]])
        for circ, lbl in zip(circles, labels):
            lbl.next_to(circ, UP)
        self.play(FadeIn(circles), Write(labels), run_time=1)

        # Circle fill updater based on current truth‐table row
        row_vals = [(0,0,0), (0,1,1), (1,0,1), (1,1,0)]
        for i, circ in enumerate(circles):
            circ.add_updater(lambda m, i=i: m.set_fill(
                GREEN if row_vals[int(row_tracker.get_value())][i] else GREY_B,
                opacity=1
            ))

        # Step through each row
        for i in range(4):
            self.play(row_tracker.animate.set_value(i), run_time=1)
            self.wait(0.5)
        self.wait(1)

        # Clean up table and markers
        self.play(FadeOut(highlight), FadeOut(table),
                  FadeOut(circles), FadeOut(labels), run_time=1)
        self.wait(0.5)

        # Draw XOR gate outline
        back_arc = Arc(radius=2, start_angle=PI/2, angle=-PI)
        front_arc = Arc(radius=1.5, start_angle=PI/2, angle=-PI).shift(RIGHT*0.5)
        top_line = Line(back_arc.get_start(), front_arc.get_start())
        bottom_line = Line(back_arc.get_end(),   front_arc.get_end())
        ctrl1 = front_arc.get_start() + RIGHT
        ctrl2 = front_arc.get_end()   + RIGHT
        right_curve = CubicBezier(front_arc.get_start(), ctrl1, ctrl2, front_arc.get_end())
        gate = VGroup(back_arc, front_arc, top_line, bottom_line, right_curve)
        gate.set_color(WHITE).move_to(ORIGIN)
        self.play(Create(gate), run_time=2)
        self.wait(0.5)

        # Input lines
        in1_pt, in2_pt = top_line.get_midpoint(), bottom_line.get_midpoint()
        in1 = Line(in1_pt + LEFT*3, in1_pt)
        in2 = Line(in2_pt + LEFT*3, in2_pt)
        self.play(Create(in1), Create(in2), run_time=1)

        # Output arrow
        out_pt = front_arc.get_end()
        out_arrow = Arrow(out_pt, out_pt + RIGHT*3, buff=0)
        self.play(GrowArrow(out_arrow), run_time=1)
        self.wait(0.5)

        # Label inputs/outputs
        lblA = Text("A", font_size=30).next_to(in1.get_start(), LEFT)
        lblB = Text("B", font_size=30).next_to(in2.get_start(), LEFT)
        lblY = Text("Y", font_size=30).next_to(out_arrow.get_end(), RIGHT)
        self.play(Write(lblA), Write(lblB), Write(lblY), run_time=1)
        self.wait(1)

        # Show logic expression
        expr = MathTex(r"Y", "=", r"A", r"\oplus", r"B", "=", r"A(1-B)", "+", r"(1-A)B")\
               .scale(0.8).to_edge(DOWN)
        self.play(Write(expr), run_time=2)
        self.wait(2)
```

Explanation:
- Step‐by‐step: truth table is built, rows highlighted, input/output circles fill per row.
- Then cleans up and draws the XOR gate shape using two arcs, connecting lines, and a cubic Bezier.
- Inputs/outputs labeled and logic formula is shown at the bottom.
- Uses `ValueTracker`, `always_redraw`, clear transitions, appropriate pacing, and Manim 0.19.0‐compatible APIs.