from manim import *

class PythagoreanTheoremScene(Scene):
    def construct(self):
        # ------------------------------------------------------------
        # 1) Title
        # ------------------------------------------------------------
        title = Tex("The Pythagorean Theorem", font_size=60)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # ------------------------------------------------------------
        # 2) Draw a 3–4–5 right triangle and label its sides
        # ------------------------------------------------------------
        a_len, b_len = 3, 4           # legs
        A = ORIGIN                    # right angle at A
        B = RIGHT * b_len
        C = UP * a_len

        triangle = Polygon(A, B, C, color=WHITE)
        right_angle = Square(0.35, stroke_width=2).move_to(
            A + 0.175 * RIGHT + 0.175 * UP
        )

        self.play(Create(triangle), FadeIn(right_angle))
        self.wait(0.5)

        label_a = MathTex("a", font_size=48).next_to((A + C) / 2, LEFT)
        label_b = MathTex("b", font_size=48).next_to((A + B) / 2, DOWN)
        label_c = MathTex("c", font_size=48).next_to((B + C) / 2, RIGHT)

        self.play(Write(label_a), Write(label_b), Write(label_c))
        self.wait()

        # ------------------------------------------------------------
        # 3) State the theorem
        # ------------------------------------------------------------
        theorem_eq = MathTex("a^2 + b^2 = c^2", font_size=60)
        theorem_eq.next_to(triangle, DOWN, buff=0.8)
        self.play(Write(theorem_eq))
        self.wait()

        # ------------------------------------------------------------
        # 4) Visualise the areas a² , b² , c²
        # ------------------------------------------------------------
        sq_a = Square(1, color=BLUE, fill_color=BLUE, fill_opacity=0.4)
        sq_b = Square(1, color=GREEN, fill_color=GREEN, fill_opacity=0.4)
        sq_c = Square(1, color=PURPLE, fill_color=PURPLE, fill_opacity=0.4)

        pair = VGroup(sq_a, sq_b).arrange(RIGHT, aligned_edge=DOWN)
        sq_c.next_to(pair, RIGHT)
        squares = VGroup(pair, sq_c).scale(0.9)
        squares.next_to(theorem_eq, DOWN, buff=0.8)

        label_a2 = MathTex("a^2", font_size=40).move_to(sq_a.get_center())
        label_b2 = MathTex("b^2", font_size=40).move_to(sq_b.get_center())
        label_c2 = MathTex("c^2", font_size=40).move_to(sq_c.get_center())

        self.play(FadeIn(squares), Write(VGroup(label_a2, label_b2, label_c2)))
        self.play(Circumscribe(sq_a), Circumscribe(label_a))
        self.play(Circumscribe(sq_b), Circumscribe(label_b))
        self.play(Circumscribe(sq_c), Circumscribe(label_c))
        self.wait()

        # ------------------------------------------------------------
        # 5) Substitute numeric values
        # ------------------------------------------------------------
        sub_eq = MathTex(f"{a_len}^2 + {b_len}^2 = c^2", font_size=60)
        sub_eq.next_to(theorem_eq, DOWN, buff=1.1)
        self.play(TransformMatchingTex(theorem_eq.copy(), sub_eq))
        self.wait()

        # ------------------------------------------------------------
        # 6) Compute each square
        # ------------------------------------------------------------
        comp_eq = MathTex(f"{a_len**2} + {b_len**2} = c^2", font_size=60)
        comp_eq.next_to(sub_eq, DOWN)
        self.play(Write(comp_eq))
        self.wait()

        # ------------------------------------------------------------
        # 7) Add the squares
        # ------------------------------------------------------------
        sum_eq = MathTex(f"{a_len**2 + b_len**2} = c^2", font_size=60)
        sum_eq.next_to(comp_eq, DOWN)
        self.play(Write(sum_eq))
        self.wait()

        # ------------------------------------------------------------
        # 8) Solve for c
        # ------------------------------------------------------------
        solve_c = MathTex("c = \\sqrt{25} = 5", font_size=60)
        solve_c.next_to(sum_eq, DOWN)
        self.play(Write(solve_c))
        self.wait(1.2)

        # ------------------------------------------------------------
        # 9) Replace symbolic side labels with numbers
        # ------------------------------------------------------------
        num_a = MathTex(str(a_len), color=BLUE, font_size=48).move_to(label_a)
        num_b = MathTex(str(b_len), color=GREEN, font_size=48).move_to(label_b)
        num_c = MathTex("5",        color=PURPLE, font_size=48).move_to(label_c)

        self.play(
            ReplacementTransform(label_a, num_a),
            ReplacementTransform(label_b, num_b),
            ReplacementTransform(label_c, num_c),
        )
        self.wait()

        # ------------------------------------------------------------
        # 10) Concluding remark
        # ------------------------------------------------------------
        concl = Tex(
            "Thus, a right triangle with legs 3 and 4\nhas a hypotenuse of 5!",
            font_size=46,
        )
        concl.to_edge(DOWN)
        self.play(Write(concl))
        self.wait(3)