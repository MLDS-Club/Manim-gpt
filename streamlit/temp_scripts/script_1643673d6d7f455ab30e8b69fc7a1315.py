from manim import *

class XORGateScene(Scene):
    def construct(self):
        # Title
        title = MathTex("XOR Gate", font_size=48).to_edge(UP)
        self.play(Write(title), run_time=1)

        # XOR gate shape
        gate = RoundedRectangle(width=1.5, height=2.5, corner_radius=0.2, color=WHITE)
        gate.shift(LEFT * 0.5)
        gate_symbol = MathTex(r"\oplus", font_size=72).move_to(gate.get_center())
        self.play(Create(gate), Write(gate_symbol), run_time=1)

        # Wires and labels
        A_pt = LEFT * 3 + UP * 0.6
        B_pt = LEFT * 3 + DOWN * 0.6
        OUT_pt = RIGHT * 3

        wireA = Line(A_pt, gate.get_left() + UP * 0.6, color=WHITE)
        wireB = Line(B_pt, gate.get_left() + DOWN * 0.6, color=WHITE)
        wireO = Line(gate.get_right(), OUT_pt, color=WHITE)
        lblA = MathTex("A", font_size=36).next_to(A_pt, LEFT)
        lblB = MathTex("B", font_size=36).next_to(B_pt, LEFT)
        lblO = MathTex(r"A\oplus B", font_size=36).next_to(OUT_pt, RIGHT)
        self.play(Create(VGroup(wireA, wireB, wireO)), Write(VGroup(lblA, lblB, lblO)), run_time=1)

        # Logic formula
        formula = MathTex(
            r"A\oplus B", "=", r"(A\land \neg B)", r"\lor", r"(\neg A\land B)",
            font_size=36
        ).to_edge(DOWN)
        self.play(Write(formula), run_time=1)
        self.wait(1)

        # Truth table
        data = [
            ["A", "B", r"A\oplus B"],
            ["0", "0", "0"],
            ["0", "1", "1"],
            ["1", "0", "1"],
            ["1", "1", "0"],
        ]
        table = Table(
            data,
            include_outer_lines=True,
            element_to_mobject=MathTex,
        ).scale(0.7)
        table.next_to(formula, DOWN, buff=1)
        self.play(Create(table), run_time=1)
        self.wait(1)

        # Output display
        tracker = ValueTracker(0)
        output_num = always_redraw(lambda: MathTex(
            str(int(tracker.get_value())), font_size=36
        ).next_to(OUT_pt, RIGHT).set_color(YELLOW))
        self.add(output_num)

        # Demonstration cases
        cases = [
            {"A":0,"B":0,"nA":1,"nB":1,"a1":0,"a2":0,"o":0},
            {"A":0,"B":1,"nA":1,"nB":0,"a1":0,"a2":1,"o":1},
            {"A":1,"B":0,"nA":0,"nB":1,"a1":1,"a2":0,"o":1},
            {"A":1,"B":1,"nA":0,"nB":0,"a1":0,"a2":0,"o":0},
        ]
        rows = table.get_rows()

        for i, case in enumerate(cases, start=1):
            # highlight row
            hl = SurroundingRectangle(rows[i], color=YELLOW)
            self.play(Create(hl), run_time=0.5)

            # stepwise logic
            L1 = MathTex(f"A = {case['A']}, B = {case['B']}", font_size=28).to_edge(LEFT).shift(DOWN*1.5)
            L2 = MathTex(
                f"¬B = {case['nB']}", f",  ¬A = {case['nA']}",
                font_size=28
            ).next_to(L1, DOWN, buff=0.2)
            L3 = MathTex(
                f"A∧¬B = {case['a1']}", f",  ¬A∧B = {case['a2']}",
                font_size=28
            ).next_to(L2, DOWN, buff=0.2)
            L4 = MathTex(f"{case['a1']} ∨ {case['a2']} = {case['o']}", font_size=28).next_to(L3, DOWN, buff=0.2)

            self.play(Write(L1), Write(L2), Write(L3), Write(L4), run_time=1.5)
            self.play(tracker.animate.set_value(case["o"]), run_time=0.5)
            self.wait(1)

            # clear
            self.play(FadeOut(VGroup(L1, L2, L3, L4, hl)), run_time=0.5)

        self.wait(2)