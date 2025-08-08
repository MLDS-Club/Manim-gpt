from manim import *

class AndGateDemo(Scene):
    def construct(self):
        # 1. Title and Logical Expression
        title = Text("AND Gate Demonstration", font_size=48)
        expr = MathTex(r"Y = A \land B", font_size=48)
        expr.next_to(title, DOWN, buff=0.5)
        self.play(Write(title), Write(expr), run_time=2)
        self.wait(1)

        # 2. Draw AND gate shape (flat left side + semicircle right side)
        left_top    = Line(LEFT + UP, ORIGIN + UP, stroke_width=4)
        left_bottom = Line(LEFT + DOWN, ORIGIN + DOWN, stroke_width=4)
        semicircle  = Arc(
            radius=1,
            start_angle=PI/2,
            angle=-PI,
            arc_center=ORIGIN,
            stroke_width=4
        )
        gate = VGroup(left_top, left_bottom, semicircle)
        gate.next_to(expr, DOWN, buff=1)
        self.play(Create(gate), run_time=2)
        self.wait(1)

        # 3. Add input & output wires
        in1 = Line(gate.get_left() + UP*0.5 + LEFT, gate.get_left() + UP*0.5, stroke_width=4)
        in2 = Line(gate.get_left() + DOWN*0.5 + LEFT, gate.get_left() + DOWN*0.5, stroke_width=4)
        out = Line(gate.get_right(), gate.get_right() + RIGHT, stroke_width=4)
        self.play(Create(in1), Create(in2), Create(out), run_time=2)

        # 4. Label wires
        lblA = Tex("A", font_size=36).next_to(in1, LEFT,  buff=0.2)
        lblB = Tex("B", font_size=36).next_to(in2, LEFT,  buff=0.2)
        lblY = Tex("Y", font_size=36).next_to(out, RIGHT, buff=0.2)
        self.play(Write(lblA), Write(lblB), Write(lblY), run_time=1)
        self.wait(1)

        # 5. ValueTrackers for dynamic input values
        a_val = ValueTracker(0)
        b_val = ValueTracker(0)

        dot_in1 = always_redraw(lambda: Dot(
            in1.get_start(),
            radius=0.08,
            color=GREEN if a_val.get_value() > 0.5 else GREY
        ))
        dot_in2 = always_redraw(lambda: Dot(
            in2.get_start(),
            radius=0.08,
            color=GREEN if b_val.get_value() > 0.5 else GREY
        ))
        dot_out = always_redraw(lambda: Dot(
            out.get_end(),
            radius=0.08,
            color=GREEN if (a_val.get_value()>0.5 and b_val.get_value()>0.5) else GREY
        ))
        self.add(dot_in1, dot_in2, dot_out)
        self.wait(1)

        # 6. Truth table creation
        table_entries = [
            ["A","B","Y"],
            ["0","0","0"],
            ["0","1","0"],
            ["1","0","0"],
            ["1","1","1"],
        ]
        table = Matrix(table_entries).scale(0.7).to_corner(UR)
        self.play(Create(table), run_time=2)
        self.wait(1)

        # 7. Animate each row of the truth table
        entries = table.get_entries()
        cols = 3
        combos = [(0,0),(0,1),(1,0),(1,1)]
        for i, (aval, bval) in enumerate(combos, start=1):
            row = VGroup(*entries[i*cols:(i+1)*cols])
            highlight = SurroundingRectangle(row, color=YELLOW, buff=0.1)
            self.play(Create(highlight), run_time=0.5)
            self.play(
                a_val.animate.set_value(aval),
                b_val.animate.set_value(bval),
                run_time=1
            )
            self.wait(0.5)
            self.play(FadeOut(highlight), run_time=0.5)

        self.wait(2)