from manim import *
import numpy as np

class VectorAdditionScene(Scene):
    def construct(self):
        # Title
        title = Text("Vector Addition", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # Given vectors text
        given = Text("Given vectors:", font_size=36).next_to(title, DOWN)
        self.play(Write(given))
        self.wait(0.5)

        # Display vector components
        a_tex = MathTex(r"\vec{a} = \begin{pmatrix}2\\1\end{pmatrix}", font_size=36)
        b_tex = MathTex(r"\vec{b} = \begin{pmatrix}1\\2\end{pmatrix}", font_size=36)
        a_tex.next_to(given, DOWN, buff=0.5).to_edge(LEFT)
        b_tex.next_to(a_tex, RIGHT, buff=2)
        self.play(Write(a_tex), Write(b_tex))
        self.wait(1)

        # Draw arrows for vectors a and b
        a_vec = Arrow(ORIGIN, np.array([2, 1, 0]), buff=0, color=BLUE)
        b_vec = Arrow(ORIGIN, np.array([1, 2, 0]), buff=0, color=GREEN)
        self.play(GrowArrow(a_vec), GrowArrow(b_vec))
        a_label = MathTex(r"\vec{a}", font_size=36, color=BLUE).next_to(a_vec.get_end(), UR, buff=0.1)
        b_label = MathTex(r"\vec{b}", font_size=36, color=GREEN).next_to(b_vec.get_end(), UR, buff=0.1)
        self.play(Write(a_label), Write(b_label))
        self.wait(1)

        # Geometric addition: translate b to head of a
        b_vec_translated = b_vec.copy().shift(np.array([2, 1, 0]))
        self.play(Create(b_vec_translated))
        b_label2 = b_label.copy().next_to(b_vec_translated.get_end(), UR, buff=0.1)
        self.play(Write(b_label2))
        self.wait(1)

        # Draw resultant vector r from origin to a + b
        r_end = np.array([3, 3, 0])
        r_vec = Arrow(ORIGIN, r_end, buff=0, color=RED)
        self.play(GrowArrow(r_vec))
        r_label = MathTex(r"\vec{r}", font_size=36, color=RED).next_to(r_vec.get_end(), UR, buff=0.1)
        self.play(Write(r_label))
        self.wait(1)

        # Show vector equation r = a + b
        eq1 = MathTex(r"\vec{r} = \vec{a} + \vec{b}", font_size=36)
        eq1.to_edge(DOWN)
        self.play(Write(eq1))
        self.wait(1)

        # Show component form symbolically
        eq2 = MathTex(
            r"\begin{pmatrix}r_x\\r_y\end{pmatrix}"
            r" = "
            r"\begin{pmatrix}a_x\\a_y\end{pmatrix}"
            r" + "
            r"\begin{pmatrix}b_x\\b_y\end{pmatrix}",
            font_size=36
        )
        eq2.next_to(eq1, UP, buff=0.5)
        self.play(Write(eq2))
        self.wait(1)

        # Show numeric substitution
        eq3 = MathTex(
            r"\begin{pmatrix}r_x\\r_y\end{pmatrix}"
            r" = "
            r"\begin{pmatrix}2\\1\end{pmatrix}"
            r" + "
            r"\begin{pmatrix}1\\2\end{pmatrix}"
            r" = "
            r"\begin{pmatrix}3\\3\end{pmatrix}",
            font_size=36
        )
        eq3.next_to(eq2, UP, buff=0.5)
        self.play(Write(eq3))
        self.wait(2)