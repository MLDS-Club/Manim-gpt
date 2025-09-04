from manim import *
import numpy as np

class NeuralNetworkTrainingScene(Scene):
    def construct(self):
        # Segment 1 Shot 1.1
        self.camera.background_color = DARK_GRAY
        left_nodes = VGroup(*[
            Circle(radius=0.2, color=BLUE, fill_opacity=0).move_to([-3, y, 0])
            for y in [1, 0, -1]
        ])
        middle_nodes = VGroup(*[
            Circle(radius=0.2, color=GREEN, fill_opacity=0).move_to([0, y, 0])
            for y in [1.5, 0.5, -0.5, -1.5]
        ])
        right_node = Circle(radius=0.2, color=RED, fill_opacity=0).move_to([3, 0, 0])
        self.play(FadeIn(left_nodes), run_time=0.8)
        self.play(FadeIn(middle_nodes), run_time=0.8)
        self.play(FadeIn(right_node), run_time=0.8)
        self.wait(0.3)

        # Segment 1 Shot 1.2
        arrows = []
        for inp in left_nodes:
            for hid in middle_nodes:
                arr = Arrow(inp.get_center(), hid.get_center(),
                            buff=0, color=WHITE, stroke_width=2, tip_length=0.1)
                arrows.append(arr)
                self.play(Create(arr), run_time=0.02)
        for hid in middle_nodes:
            arr = Arrow(hid.get_center(), right_node.get_center(),
                        buff=0, color=WHITE, stroke_width=2, tip_length=0.1)
            arrows.append(arr)
            self.play(Create(arr), run_time=0.02)
        self.wait(1)

        # Segment 2 Shot 2.1
        network = VGroup(left_nodes, middle_nodes, right_node, *arrows)
        self.play(*(m.animate.set_opacity(0.5) for m in network), run_time=0.5)
        x1_node = left_nodes[1]  # position y=0
        self.play(x1_node.animate.set_opacity(1), run_time=0.5)
        x1_label = MathTex("x_1", font_size=36, color=WHITE).next_to(x1_node, UP, buff=0.1)
        self.play(FadeIn(x1_label), run_time=0.5)

        # Segment 2 Shot 2.2
        x1_arrows = [arr for arr in arrows if np.allclose(arr.get_start(), x1_node.get_center())]
        weight_labels = VGroup()
        for j, arr in enumerate(x1_arrows, start=1):
            self.play(arr.animate.set_stroke(width=4, color=WHITE), run_time=0.4)
            label = MathTex(f"w_{{1{j}}}", font_size=30, color=YELLOW)
            label.move_to(arr.get_start())
            weight_labels.add(label)
            self.play(label.animate.move_to(arr.get_center()), run_time=0.4)

        # Segment 2 Shot 2.3
        z_eq = MathTex("z = w \\cdot x + b", font_size=40, color=WHITE).to_edge(UP, buff=0.5)
        h_eq = MathTex("h = \\sigma(z)", font_size=36, color=GRAY).next_to(z_eq, DOWN, buff=0.2)
        self.play(Write(z_eq), Write(h_eq), run_time=0.6)
        for lbl in weight_labels:
            arr2z = Arrow(lbl.get_center(), z_eq.get_left() + RIGHT * 0.2,
                          buff=0, color=WHITE)
            self.play(Create(arr2z), run_time=0.4)
        bias_circle = Circle(radius=0.1, color=PINK, fill_opacity=1).move_to(
            middle_nodes[1].get_center() + RIGHT * 0.5)
        self.play(FadeIn(bias_circle), run_time=0.4)
        self.wait(1.5)

        # Segment 3 Shot 3.1
        self.play(*(m.animate.set_opacity(0.3) for m in network), run_time=0.5)
        y_label = MathTex("y", font_size=44, color=WHITE).next_to(right_node, RIGHT, buff=0.2)
        yhat_label = MathTex("\\hat y", font_size=44, color=YELLOW)
        yhat_start = yhat_label.copy().move_to(y_label.get_center() + DOWN)
        yhat_label.move_to(right_node.get_center() + DOWN * 0.3 + RIGHT * 0.2)
        self.play(FadeIn(y_label), run_time=0.5)
        self.play(yhat_start.animate.move_to(yhat_label.get_center()), run_time=0.5)

        # Segment 3 Shot 3.2
        loss_eq = MathTex("L = \\tfrac12 (y - \\hat y)^2", font_size=48, color=WHITE).to_edge(UP)
        loss_text = Text("Loss", font_size=24, color=GRAY).next_to(loss_eq, DOWN, buff=0.2)
        self.play(Write(loss_eq), run_time=0.7)
        self.play(Write(loss_text), run_time=0.3)
        self.wait(2)

        # Segment 4 Shot 4.1
        bp1 = Arrow(loss_eq.get_bottom(), yhat_label.get_top(), buff=0, color=RED)
        bp2 = Arrow(yhat_label.get_bottom(), middle_nodes[1].get_top(), buff=0, color=RED)
        bp3 = Arrow(middle_nodes[1].get_bottom(), weight_labels[0].get_top(), buff=0, color=RED)
        self.play(Create(bp1), Create(bp2), Create(bp3), run_time=0.5)

        # Segment 4 Shot 4.2
        term1 = MathTex(
            "\\frac{\\partial L}{\\partial w} = (",
            "\\frac{\\partial L}{\\partial \\hat y}", ")",
            font_size=36
        )
        term1.set_color_by_tex("\\frac{\\partial L}{\\partial \\hat y}", RED)
        term2 = MathTex("\\frac{\\partial \\hat y}{\\partial z}", font_size=36, color=ORANGE)
        term3 = MathTex("\\frac{\\partial z}{\\partial w}", font_size=36, color=YELLOW)
        stacked = VGroup(term1, term2, term3).arrange(DOWN, center=True).shift(DOWN)
        for term in stacked:
            term.shift(RIGHT * 6)
            self.play(term.animate.shift(LEFT * 6), run_time=0.5)
            self.wait(0.4)

        # Segment 4 Shot 4.3
        dLdy = MathTex("\\hat y - y", font_size=36, color=RED).next_to(term1, RIGHT, buff=0.5)
        dydz = MathTex("\\sigma'(z)", font_size=36, color=ORANGE).next_to(term2, RIGHT, buff=0.5)
        dzdw = MathTex("x", font_size=36, color=YELLOW).next_to(term3, RIGHT, buff=0.5)
        self.play(FadeIn(dLdy), FadeIn(dydz), FadeIn(dzdw), run_time=0.6)
        self.play(
            dLdy.animate.set_stroke(width=3),
            dydz.animate.set_stroke(width=3),
            dzdw.animate.set_stroke(width=3)
        )
        self.wait(1)

        # Segment 5 Shot 5.1
        grad_final = MathTex(
            "\\frac{\\partial L}{\\partial w} = x \\cdot \\sigma'(z) \\cdot (\\hat y - y)",
            font_size=42, color=WHITE
        )
        update_rule = MathTex(
            "w \\leftarrow w - \\eta \\cdot \\frac{\\partial L}{\\partial w}",
            font_size=40, color="#00FFFF"
        )
        self.play(Write(grad_final), run_time=0.8)
        self.wait(0.5)
        self.play(FadeIn(update_rule), run_time=0.5)

        # Segment 5 Shot 5.2
        self.play(*(m.animate.set_opacity(1) for m in network), run_time=0.5)
        line = x1_arrows[1]
        self.play(line.animate.set_color(WHITE), run_time=0.3)
        val_old = MathTex("w=0.5", font_size=30, color=YELLOW).next_to(line.get_center(), UP, buff=0.2)
        self.play(FadeIn(val_old), run_time=0.5)
        val_new = MathTex("w=0.45", font_size=30, color=GREEN).next_to(line.get_center(), UP, buff=0.2)
        self.play(FadeOut(val_old), FadeIn(val_new), run_time=1)
        self.play(Indicate(line), run_time=1)
        self.wait(1)

        # Segment 5 Shot 5.3
        overlays = VGroup(
            x1_label, weight_labels, z_eq, h_eq, bias_circle,
            y_label, yhat_label, loss_eq, loss_text,
            bp1, bp2, bp3, stacked, dLdy, dydz, dzdw,
            grad_final, update_rule, val_new
        )
        self.play(FadeOut(overlays), run_time=0.5)
        bullets = VGroup(
            Text("1. Forward pass → ŷ", font_size=32, color=WHITE),
            Text("2. Compute loss L", font_size=32, color=WHITE),
            Text("3. Backprop chain rule", font_size=32, color=WHITE),
            Text("4. Weight update", font_size=32, color=WHITE)
        ).arrange(DOWN, center=False, aligned_edge=LEFT).move_to(DOWN * 2)
        for b in bullets:
            self.play(Write(b), run_time=0.5)
        self.wait(3)
        self.play(FadeOut(bullets), FadeOut(network), run_time=1)