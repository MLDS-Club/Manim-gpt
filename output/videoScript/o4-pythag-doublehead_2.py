from manim import *

class VisualizingTheoremWithSquares(Scene):
    def construct(self):
        # Shot 1: Draw right triangle ABC
        A = np.array([-2, -1, 0])
        B = np.array([2, -1, 0])
        C = np.array([-2, 1, 0])
        triangle = Polygon(A, B, C, stroke_color=BLACK, stroke_width=4)
        label_A = Text("A", font_size=48, color=BLUE).next_to(A, DOWN+LEFT, buff=0.1)
        label_B = Text("B", font_size=48, color=BLUE).next_to(B, DOWN+RIGHT, buff=0.1)
        label_C = Text("C", font_size=48, color=BLUE).next_to(C, UP+LEFT, buff=0.1)
        self.play(FadeIn(triangle, run_time=1), FadeIn(label_A, label_B, label_C, run_time=1))
        self.wait(0.5)

        # Shot 2: Show side labels and highlight sides
        side_BC = Line(B, C, stroke_width=4)
        side_AC = Line(A, C, stroke_width=4)
        side_AB = Line(A, B, stroke_width=4)
        t_a = Tex("a = BC (hypotenuse)", font_size=36, tex_to_color_map={"a": RED})
        t_b = Tex("b = AC (vertical leg)", font_size=36, tex_to_color_map={"b": GREEN})
        t_c = Tex("c = AB (horizontal leg)", font_size=36, tex_to_color_map={"c": BLUE})
        # position offscreen left then slide in
        for t in (t_a, t_b, t_c):
            t.to_edge(DOWN)
            t.shift(LEFT * 6)
        t_b.next_to(t_a, DOWN, aligned_edge=LEFT)
        t_c.next_to(t_b, DOWN, aligned_edge=LEFT)

        self.play(t_a.animate.shift(RIGHT * 6), Create(side_BC.copy().set_color(RED)), run_time=0.5)
        self.play(t_b.animate.shift(RIGHT * 6), Create(side_AC.copy().set_color(GREEN)), run_time=0.5)
        self.play(t_c.animate.shift(RIGHT * 6), Create(side_AB.copy().set_color(BLUE)), run_time=0.5)
        self.wait(0.5)

        # Shot 3: Construct squares on each side
        # BC square (red)
        v_BC = C - B
        norm_BC = np.array([-v_BC[1], v_BC[0], 0]) / np.linalg.norm(v_BC) * np.linalg.norm(v_BC)
        sq_BC = Polygon(B, C, C + norm_BC, B + norm_BC, stroke_color=RED, stroke_width=3)
        sq_BC.set_fill(RED, opacity=0)
        # AC square (green)
        v_AC = C - A
        norm_AC = np.array([-v_AC[1], v_AC[0], 0]) / np.linalg.norm(v_AC) * np.linalg.norm(v_AC)
        sq_AC = Polygon(A, C, C + norm_AC, A + norm_AC, stroke_color=GREEN, stroke_width=3)
        sq_AC.set_fill(GREEN, opacity=0)
        # AB square (blue) below
        v_AB = B - A
        norm_AB = np.array([-v_AB[1], v_AB[0], 0]) / np.linalg.norm(v_AB) * np.linalg.norm(v_AB)
        norm_AB = -norm_AB
        sq_AB = Polygon(A, B, B + norm_AB, A + norm_AB, stroke_color=BLUE, stroke_width=3)
        sq_AB.set_fill(BLUE, opacity=0)

        self.play(Create(sq_BC), Create(sq_AC), Create(sq_AB), run_time=1)
        self.play(
            sq_BC.animate.set_fill(RED, opacity=0.4),
            sq_AC.animate.set_fill(GREEN, opacity=0.4),
            sq_AB.animate.set_fill(BLUE, opacity=0.4),
            run_time=0.5
        )
        self.wait(0.5)

        # Shot 4: Show area labels with pulse
        lab_BC = Tex("Area of red square = a^2", font_size=36, color=BLACK).next_to(sq_BC, UR)
        lab_AC = Tex("Area of green square = b^2", font_size=36, color=BLACK).next_to(sq_AC, UL)
        lab_AB = Tex("Area of blue square = c^2", font_size=36, color=BLACK).next_to(sq_AB, DOWN)
        self.play(FadeIn(lab_BC), Indicate(sq_BC, scale_factor=1.05), run_time=0.5)
        self.play(FadeIn(lab_AC), Indicate(sq_AC, scale_factor=1.05), run_time=0.5)
        self.play(FadeIn(lab_AB), Indicate(sq_AB, scale_factor=1.05), run_time=0.5)
        self.wait(0.5)

        # Shot 5: Show plus and equals, slide red & green squares
        plus = Tex("+", font_size=72).move_to((sq_BC.get_right() + sq_AC.get_top()) / 2)
        equals = Tex("=", font_size=72)
        comp_center = sq_BC.get_center() + RIGHT * 1.5
        equals.move_to((comp_center + sq_AB.get_center()) / 2)
        self.play(FadeIn(plus), FadeIn(equals))
        shift_vec = RIGHT * 1.5
        self.play(
            sq_BC.animate.shift(shift_vec),
            sq_AC.animate.shift(shift_vec),
            plus.animate.shift(RIGHT * 1.5),
            run_time=0.75
        )
        self.wait(0.5)

        # Shot 6: Show final formula
        all_objs = VGroup(
            triangle, label_A, label_B, label_C,
            t_a, t_b, t_c, side_BC, side_AC, side_AB,
            sq_BC, sq_AC, sq_AB, lab_BC, lab_AC, lab_AB,
            plus, equals
        )
        formula = Tex("a^2 + b^2 = c^2", font_size=72)
        self.play(FadeOut(all_objs), FadeIn(formula, run_time=1))
        self.wait(3)

class AlgebraicProofViaSimilarTriangles(Scene):
    def construct(self):
        # Shot 1: Draw triangle ABC
        A = np.array([-3, -1, 0])
        B = np.array([1, -1, 0])
        C = np.array([-3, 3, 0])
        triangle = Polygon(A, B, C, stroke_color=BLACK, stroke_width=3)
        label_A = Text("A", font_size=36, color=BLACK).next_to(A, DOWN+LEFT, buff=0.1)
        label_B = Text("B", font_size=36, color=BLACK).next_to(B, DOWN+RIGHT, buff=0.1)
        label_C = Text("C", font_size=36, color=BLACK).next_to(C, UP+LEFT, buff=0.1)
        self.add(triangle, label_A, label_B, label_C)
        self.wait(0.5)

        # Shot 2: Drop perpendicular CD to AB at D
        D = np.array([C[0], A[1], 0])
        line_CD = DashedLine(C, D, stroke_color=GRAY)
        label_D = Text("D", font_size=36, color=MAGENTA).next_to(D, DOWN, buff=0.1)
        self.play(Create(line_CD, run_time=0.8), FadeIn(label_D))
        self.wait(0.5)

        # Shot 3: Highlight triangles
        tri_ADC = Polygon(A, D, C, stroke_color=GREEN)
        tri_CDB = Polygon(C, D, B, stroke_color=RED)
        self.play(Indicate(triangle, color=BLACK), run_time=1)
        self.play(Indicate(tri_ADC, color=GREEN), run_time=1)
        self.play(Indicate(tri_CDB, color=RED), run_time=1)
        self.wait(0.5)

        # Shot 4: Proportionality equations
        eq1 = Tex(
            "From similarity of ", "$\\Delta ABC$", " and ", "$\\Delta ADC$", ":",
            "$AC/AB = AD/AC$", "\\\\Rightarrow b/c = d/b", "\\\\Rightarrow b^2 = c d$",
            tex_to_color_map={"b": GREEN, "c": GREEN, "d": MAGENTA},
            font_size=24
        ).to_edge(LEFT).shift(RIGHT)
        parts1 = VGroup(*[eq1[i] for i in range(5, 8)])
        for part in parts1:
            self.play(Write(part), run_time=1)
        self.wait(0.5)

        eq2 = Tex(
            "From similarity of ", "$\\Delta ABC$", " and ", "$\\Delta CDB$", ":",
            "$CB/AB = DB/CB$", "\\\\Rightarrow a/c = e/a", "\\\\Rightarrow a^2 = c e$",
            tex_to_color_map={"a": RED, "e": RED},
            font_size=24
        ).next_to(eq1, DOWN, buff=1)
        parts2 = VGroup(*[eq2[i] for i in range(5, 8)])
        for part in parts2:
            self.play(Write(part), run_time=1)
        self.wait(0.5)

        # Shot 5: Summation line
        sum_parts = ["a^2 + b^2", " = c e + c d", " = c(d + e)", " = c c", " = c^2"]
        sum_mobs = []
        for i, text in enumerate(sum_parts):
            mob = MathTex(text, tex_to_color_map={"d": MAGENTA, "e": RED}, font_size=24)
            if i == 0:
                mob.next_to(eq2, DOWN, buff=1)
            else:
                mob.next_to(sum_mobs[-1], RIGHT, buff=0.2)
            sum_mobs.append(mob)
            self.play(Write(mob), run_time=0.5)
            self.wait(0.5)
            if text.startswith(" = c(d + e)"):
                bracket = Brace(mob.submobjects[-1], direction=UP)
                self.play(GrowFromCenter(bracket), run_time=0.5)
                self.wait(0.5)
                self.play(Transform(bracket, Tex("c", font_size=24)), run_time=0.5)
                self.wait(0.5)
        self.wait(0.5)

        # Shot 6: Final wrap-up
        self.play(
            FadeOut(VGroup(
                triangle, label_A, label_B, label_C,
                line_CD, label_D, tri_ADC, tri_CDB, eq1, eq2, *sum_mobs
            )),
            run_time=1
        )
        final_title = Tex("a^2 + b^2 = c^2", font_size=80)
        subtitle = Text("Proved by similar triangles.", font_size=36, color=GREY).next_to(final_title, DOWN)
        self.play(FadeIn(final_title), FadeIn(subtitle), run_time=1)
        self.wait(3)