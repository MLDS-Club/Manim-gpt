from manim import *
import numpy as np

class VectorAdditionScene(VectorScene):
    def construct(self):
        # 1. Draw coordinate plane
        plane = self.add_plane(animate=True)
        self.wait(1)

        # 2. Define vectors a and b
        a = np.array([2, 1, 0])
        b = np.array([1, 2, 0])

        # 3. Display vector definitions
        eq1 = MathTex(
            r"\vec{a} = \begin{pmatrix}2 \\ 1\end{pmatrix}", 
            r"\quad",
            r"\vec{b} = \begin{pmatrix}1 \\ 2\end{pmatrix}"
        ).to_edge(UP)
        self.play(Write(eq1), run_time=2)
        self.wait(1)

        # 4. Draw vector a from origin
        vec_a = self.add_vector(a, color=BLUE)
        label_a = self.label_vector(vec_a, MathTex(r"\vec{a}"), at_tip=True)
        self.wait(1)

        # 5. Draw vector b from origin
        vec_b = self.add_vector(b, color=GREEN)
        label_b = self.label_vector(vec_b, MathTex(r"\vec{b}"), at_tip=True)
        self.wait(1)

        # 6. Move vector b head-to-tail to a
        self.play(
            vec_b.animate.shift(a),
            label_b.animate.shift(a),
            run_time=2
        )
        self.wait(1)

        # 7. Draw resultant vector r = a + b
        r = a + b
        vec_r = self.add_vector(r, color=YELLOW)
        label_r = self.label_vector(
            vec_r, 
            MathTex(r"\vec{a} + \vec{b} = \vec{r}"), 
            at_tip=True
        )
        self.wait(1)

        # 8. Show component-wise sum
        eq2 = MathTex(
            r"\vec{a} + \vec{b} =",
            r"\begin{pmatrix}2 \\ 1\end{pmatrix} + \begin{pmatrix}1 \\ 2\end{pmatrix}",
            r"= \begin{pmatrix}3 \\ 3\end{pmatrix}"
        ).next_to(eq1, DOWN, buff=0.5)
        self.play(Write(eq2), run_time=3)
        self.wait(2)
```

This script meets all requirements:
- Calls `add_plane`, `add_vector`, `label_vector` from `VectorScene`.
- Provides step-by-step annotation and pacing.
- Uses Manim v0.19 compatible APIs.
- Named `VectorAdditionScene` with a single `construct()` method.
- Approved via `executeManim` without errors.