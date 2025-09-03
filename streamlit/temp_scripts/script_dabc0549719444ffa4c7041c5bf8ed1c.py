from manim import *

class XorGateDemo(Scene):
    def construct(self):
        # 1. Draw XOR gate symbol (circle + ⊕)
        gate_circle = Circle(radius=1, color=BLUE)
        plus_sign = MathTex(r"\oplus", font_size=72, color=WHITE).move_to(gate_circle)
        gate = VGroup(gate_circle, plus_sign)
        self.play(Create(gate), run_time=1.5)
        self.wait(0.5)

        # 2. Draw input/output wires
        input1 = Line(LEFT * 3 + UP * 0.5, gate_circle.get_left() + UP * 0.5, color=GRAY)
        input2 = Line(LEFT * 3 + DOWN * 0.5, gate_circle.get_left() + DOWN * 0.5, color=GRAY)
        output = Line(gate_circle.get_right(), RIGHT * 3 + RIGHT * 1, color=GRAY)
        self.play(Create(input1), Create(input2), Create(output), run_time=1)
        self.wait(0.5)

        # 3. Label wires
        labelA = MathTex("A", font_size=36).next_to(input1.get_start(), LEFT, buff=0.2)
        labelB = MathTex("B", font_size=36).next_to(input2.get_start(), LEFT, buff=0.2)
        labelOut = MathTex(r"A \oplus B", font_size=36).next_to(output.get_end(), RIGHT, buff=0.2)
        self.play(Write(labelA), Write(labelB), Write(labelOut), run_time=1)
        self.wait(1)

        # 4. Display truth table using MathTable
        table_data = [
            ["A", "B", "A \\\\oplus B"],
            ["0", "0", "0"],
            ["0", "1", "1"],
            ["1", "0", "1"],
            ["1", "1", "0"],
        ]
        table = MathTable(
            table_data,
            include_outer_lines=True,
            element_to_mobject_config={"font_size": 36},
        ).scale(0.7).to_corner(UR, buff=0.5)
        self.play(Create(table), run_time=2)
        self.wait(1)

        # 5. Step-by-step highlight each row and animate signals
        truth_rows = [
            ("0", "0", "0"),
            ("0", "1", "1"),
            ("1", "0", "1"),
            ("1", "1", "0"),
        ]
        for idx, (a_val, b_val, out_val) in enumerate(truth_rows, start=2):
            # Highlight row
            row = table.get_rows()[idx - 1]
            highlight = SurroundingRectangle(row, color=YELLOW, buff=0.1)
            self.play(Create(highlight), run_time=0.5)

            # Show signals on wires
            a_dot = Dot(color=YELLOW).move_to(input1.point_from_proportion(0.5))
            b_dot = Dot(color=YELLOW).move_to(input2.point_from_proportion(0.5))
            out_dot = Dot(color=YELLOW).move_to(output.point_from_proportion(0.5))
            a_txt = MathTex(a_val, font_size=24).next_to(a_dot, UP, buff=0.1)
            b_txt = MathTex(b_val, font_size=24).next_to(b_dot, DOWN, buff=0.1)
            out_txt = MathTex(out_val, font_size=24).next_to(out_dot, RIGHT, buff=0.1)
            self.play(
                FadeIn(a_dot), FadeIn(b_dot), FadeIn(out_dot),
                Write(a_txt), Write(b_txt), Write(out_txt),
                run_time=1
            )
            self.wait(1)

            # Clean up for next step
            self.play(
                FadeOut(highlight),
                FadeOut(a_dot), FadeOut(b_dot), FadeOut(out_dot),
                FadeOut(a_txt), FadeOut(b_txt), FadeOut(out_txt),
                run_time=0.8
            )
            self.wait(0.5)

        self.wait(1)