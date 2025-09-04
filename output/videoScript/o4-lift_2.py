from manim import *
import math

# Global background color
config.background_color = WHITE

class NetworkArchitectureOverview(Scene):
    def construct(self):
        # 1.1 Fade-in Title
        title = Text("Backpropagation in Neural Networks", font_size=72, color="#014421")
        self.play(FadeIn(title, run_time=1))
        self.wait(2)
        self.play(FadeOut(title, run_time=0.5))

        # 1.2 Show 3-Layer Network
        neuron_radius = 0.3
        input_ys = [1.5, 0.5, -0.5]
        hidden_ys = [1.5, 0.5, -0.5, -1.5]
        output_ys = [1.5, -0.5]

        input_neurons = VGroup(*[
            Circle(radius=neuron_radius, color=DARK_SLATE_BLUE, fill_color=WHITE, fill_opacity=1)
            .move_to(LEFT * 3 + UP * y)
            for y in input_ys
        ])
        hidden_neurons = VGroup(*[
            Circle(radius=neuron_radius, color=DARK_SLATE_BLUE, fill_color=WHITE, fill_opacity=1)
            .move_to(ORIGIN + UP * y)
            for y in hidden_ys
        ])
        output_neurons = VGroup(*[
            Circle(radius=neuron_radius, color=DARK_SLATE_BLUE, fill_color=WHITE, fill_opacity=1)
            .move_to(RIGHT * 3 + UP * y)
            for y in output_ys
        ])

        self.play(FadeIn(input_neurons, run_time=0.5))
        self.play(FadeIn(hidden_neurons, run_time=0.5))
        self.play(FadeIn(output_neurons, run_time=0.5))

        # Connections
        connections = VGroup()
        for i in input_neurons:
            for h in hidden_neurons:
                connections.add(Line(i.get_center(), h.get_center(), stroke_width=1, color=GRAY))
        for h in hidden_neurons:
            for o in output_neurons:
                connections.add(Line(h.get_center(), o.get_center(), stroke_width=1, color=GRAY))
        self.play(Create(connections, run_time=1))

        # 1.3 Label Weights and Biases
        weight_labels = VGroup()
        # Input->Hidden
        for i_idx, i in enumerate(input_neurons, start=1):
            for h_idx, h in enumerate(hidden_neurons, start=1):
                wl = MathTex(f"w_{{{i_idx}{h_idx}}}", font_size=24, color=BLUE)
                wl.next_to(Line(i.get_center(), h.get_center()), UP * 0.1)
                weight_labels.add(wl)
        # Hidden->Output
        for h_idx, h in enumerate(hidden_neurons, start=1):
            for o_idx, o in enumerate(output_neurons, start=1):
                wl = MathTex(f"w_{{{h_idx}{o_idx}}}", font_size=24, color=BLUE)
                wl.next_to(Line(h.get_center(), o.get_center()), UP * 0.1)
                weight_labels.add(wl)

        bias_labels = VGroup()
        for idx, neuron in enumerate(hidden_neurons, start=1):
            bl = MathTex(f"b_{{{idx}}}", font_size=24, color=RED)
            bl.next_to(neuron, RIGHT, buff=0.1)
            bias_labels.add(bl)
        for idx, neuron in enumerate(output_neurons, start=1):
            bl = MathTex(f"b_{{{idx+4}}}", font_size=24, color=RED)
            bl.next_to(neuron, RIGHT, buff=0.1)
            bias_labels.add(bl)

        # Animate weights fade-in
        for wl in weight_labels:
            self.play(FadeIn(wl, run_time=0.05), run_time=0.05)
        # Animate biases pop-in
        for bl in bias_labels:
            self.play(GrowFromCenter(bl, run_time=0.1), run_time=0.1)

        # Zoom out slightly
        self.play(self.camera.frame.animate.scale(1.05), run_time=1)
        self.wait(3)


class ForwardPassComputation(Scene):
    def construct(self):
        # 2.1 Introduce Input Vector x
        vector = MathTex(r"x = \begin{pmatrix} x_1 \\ x_2 \\ x_3 \end{pmatrix}", font_size=36, color=BLACK)
        vector.move_to(LEFT * 7)
        self.play(vector.animate.move_to(LEFT * 5), run_time=0.8)

        # re-create hidden neurons for reference
        neuron_radius = 0.3
        hidden_ys = [1.5, 0.5, -0.5, -1.5]
        hidden_neurons = VGroup(*[
            Circle(radius=neuron_radius, color=DARK_SLATE_BLUE, fill_color=WHITE, fill_opacity=1)
            .move_to(ORIGIN + UP * y)
            for y in hidden_ys
        ])
        self.add(hidden_neurons)

        # 2.2 Compute Hidden Layer Pre-activations z
        glow = Circle(radius=neuron_radius + 0.1, stroke_width=4, color=YELLOW).move_to(hidden_neurons[0])
        self.play(Create(glow), run_time=0.3)
        z1_eq = MathTex(
            r"z_1 = w_{11}x_1 + w_{21}x_2 + w_{31}x_3 + b_1",
            font_size=32, color=DARK_SLATE_GRAY
        )
        z1_eq.next_to(glow, RIGHT, buff=1)
        self.play(Write(z1_eq), run_time=1)

        arrows = VGroup(*[
            Arrow(start=i.get_center(), end=glow.get_center(), buff=0, color="#FFD54F", stroke_width=3)
            for i in [Circle().move_to(LEFT * 3 + UP * y) for y in [1.5, 0.5, -0.5]]
        ])
        self.play(Create(arrows), run_time=1)

        # 2.3 Activation Function a = σ(z)
        sigmoid_eq = MathTex(r"\sigma(z_1) = \frac{1}{1 + e^{-z_1}}", font_size=32, color=BLACK)
        sigmoid_eq.next_to(z1_eq, DOWN, buff=0.5)
        axes = Axes(
            x_range=[-6, 6, 2], y_range=[0, 1, 0.5],
            width=4, height=2, axis_config={"color": GRAY}
        ).move_to(DOWN * 3)
        curve = axes.plot(lambda x: 1 / (1 + math.exp(-x)), color=CRIMSON)
        sigmoid_plot = VGroup(axes, curve)
        sigmoid_plot.scale(0)
        self.play(sigmoid_plot.animate.scale(1), run_time=0.7)
        self.play(FadeIn(sigmoid_eq, run_time=0.5))

        # 2.4 Propagate to All Hidden Neurons
        self.play(FadeOut(glow), FadeOut(arrows), FadeOut(z1_eq), FadeOut(sigmoid_eq))
        formulas = VGroup()
        for idx, neuron in enumerate(hidden_neurons, start=1):
            glow_j = Circle(radius=neuron_radius + 0.1, stroke_width=4, color=YELLOW).move_to(neuron)
            self.play(Create(glow_j), run_time=0.3)
            z_j = MathTex(
                fr"z_{idx} = \sum_i w_{{i{idx}}} x_i + b_{idx}",
                font_size=28, color=GRAY
            ).next_to(neuron, UP, buff=0.3)
            a_j = MathTex(fr"a_{idx} = \sigma(z_{idx})", font_size=28, color=GRAY).next_to(z_j, UP, buff=0.1)
            self.play(Write(z_j), Write(a_j), run_time=0.3)
            formulas.add(z_j, a_j)
            self.play(FadeOut(glow_j), run_time=0.1)
        compact = MathTex(r"a^{(1)} = \sigma\bigl(W^{(1)}x + b^{(1)}\bigr)", font_size=36, color=NAVY)
        compact.to_edge(DOWN, buff=1)
        self.play(Write(compact), self.camera.frame.animate.scale(1.1), run_time=1)
        self.wait(2)


class ComputingTheLoss(Scene):
    def construct(self):
        # Assume network remains on screen
        # 3.1 Show Output Activation a^(2)
        neuron_radius = 0.3
        output_ys = [1.5, -0.5]
        output_neurons = VGroup(*[
            Circle(radius=neuron_radius, color=DARK_SLATE_BLUE, fill_color=WHITE, fill_opacity=1)
            .move_to(RIGHT * 3 + UP * y)
            for y in output_ys
        ])
        self.add(output_neurons)
        glow_out = VGroup(*[
            Circle(radius=neuron_radius + 0.1, stroke_width=4, color=LIGHT_GREEN).move_to(o)
            for o in output_neurons
        ])
        self.play(FadeIn(glow_out, run_time=0.5))
        pred_eq = MathTex(r"a^{(2)} = \sigma\bigl(W^{(2)}a^{(1)} + b^{(2)}\bigr)", font_size=32, color=DARK_GREEN)
        pred_eq.to_edge(UP, buff=1)
        self.play(FadeIn(pred_eq, run_time=1))

        # 3.2 Introduce True Label y
        true_y = MathTex(r"y = \begin{pmatrix} y_1 \\ y_2 \end{pmatrix}", font_size=36, color=RED)
        true_y.move_to(RIGHT * 7)
        self.play(true_y.animate.move_to(RIGHT * 5), run_time=0.8)

        # 3.3 Define Loss Function L
        loss = MathTex(r"L = \tfrac12 \|a^{(2)} - y\|^2", font_size=48, color=BLACK)
        loss.move_to(ORIGIN)
        self.play(Write(loss, run_time=1))
        box = SurroundingRectangle(loss, color=RED, stroke_width=2)
        self.play(Create(box, run_time=0.5))
        self.wait(2)


class BackpropagationGradientComputation(Scene):
    def construct(self):
        # 4.1 Error at Output: δ^(2)
        loss = MathTex(r"L = \tfrac12 \|a^{(2)} - y\|^2", font_size=48, color=BLACK)
        loss.to_edge(UP)
        self.add(loss)
        arrow_down = Arrow(
            start=loss.get_bottom() + DOWN * 0.1,
            end=RIGHT * 3 + DOWN * 2,
            color=FIREBRICK, stroke_width=3
        )
        delta2 = MathTex(r"\delta^{(2)} = \frac{\partial L}{\partial z^{(2)}}", font_size=36, color=FIREBRICK)
        delta2.next_to(arrow_down, RIGHT, buff=0.5)
        self.play(Create(arrow_down, run_time=0.7))
        self.play(FadeIn(delta2, run_time=0.8))

        # 4.2 Compute δ^(2) Expression
        term1 = MathTex(r"a^{(2)} - y", font_size=32, color=BLACK).to_edge(LEFT, buff=1)
        term2 = MathTex(r"\sigma'(z^{(2)})", font_size=32, color=BLACK).to_edge(RIGHT, buff=1)
        self.play(term1.animate.shift(RIGHT * 2), term2.animate.shift(LEFT * 2), run_time=0.6)
        dot = MathTex(r"\odot", font_size=32, color=BLACK).move_to(ORIGIN)
        self.play(FadeIn(dot, run_time=0.3))

        # 4.3 Propagate Error to Hidden Layer
        hidden_ys = [1.5, 0.5, -0.5, -1.5]
        hidden_neurons = VGroup(*[
            Circle(radius=0.3, color=DARK_SLATE_BLUE, fill_color=WHITE, fill_opacity=1)
            .move_to(ORIGIN + UP * y)
            for y in hidden_ys
        ])
        output_ys = [1.5, -0.5]
        output_neurons = VGroup(*[
            Circle(radius=0.3, color=DARK_SLATE_BLUE, fill_color=WHITE, fill_opacity=1)
            .move_to(RIGHT * 3 + UP * y)
            for y in output_ys
        ])
        arrows_back = VGroup()
        for o in output_neurons:
            for h in hidden_neurons:
                arrows_back.add(Arrow(start=o.get_center(), end=h.get_center(), buff=0, color=ORANGE))
        self.play(Create(arrows_back, run_time=1.2))
        wt_label = MathTex(r"(W^{(2)})^T", font_size=28, color=ORANGE).to_edge(UP, buff=1)
        self.play(Write(wt_label, run_time=0.5))
        delta1 = MathTex(
            r"\delta^{(1)} = \bigl((W^{(2)})^T \delta^{(2)}\bigr) \odot \sigma'(z^{(1)})",
            font_size=32, color=NAVY
        ).to_edge(DOWN, buff=1)
        self.play(FadeIn(delta1, run_time=0.7))

        # 4.4 Chain Rule Visual Breakdown
        box1 = SurroundingRectangle(MathTex(r"\partial L/\partial a^{(2)} = a^{(2)} - y",
                                            font_size=24), color=LIGHT_BLUE).shift(RIGHT * 4 + UP * 1)
        box2 = SurroundingRectangle(MathTex(r"\partial a^{(2)}/\partial z^{(2)} = \sigma'(z^{(2)})",
                                            font_size=24), color=LIGHT_CORAL).next_to(box1, DOWN, buff=0.5)
        box3 = SurroundingRectangle(MathTex(r"\partial z^{(2)}/\partial W^{(2)} = a^{(1)T}",
                                            font_size=24), color=LIGHT_GOLD).next_to(box2, DOWN, buff=0.5)
        arr12 = Arrow(box1.get_bottom(), box2.get_top(), buff=0.1, color=BLACK)
        arr23 = Arrow(box2.get_bottom(), box3.get_top(), buff=0.1, color=BLACK)
        lbl_chain1 = MathTex("chain", font_size=20).next_to(arr12, RIGHT, buff=0.1)
        lbl_chain2 = MathTex("chain", font_size=20).next_to(arr23, RIGHT, buff=0.1)
        self.play(
            box1.animate.shift(RIGHT * 0.2),
            run_time=0.5
        )
        self.add(box2, box3)
        self.play(
            box2.animate.shift(RIGHT * 0.2),
            run_time=0.5
        )
        self.play(
            box3.animate.shift(RIGHT * 0.2),
            run_time=0.5
        )
        self.play(Create(arr12), FadeIn(lbl_chain1), run_time=0.3)
        self.play(Create(arr23), FadeIn(lbl_chain2), run_time=0.3)
        self.wait(3)


class WeightUpdateStep(Scene):
    def construct(self):
        # 5.1 Show Gradient Formulas
        gradW = MathTex(r"\frac{\partial L}{\partial W^{(l)}} = \delta^{(l)} (a^{(l-1)})^T",
                        font_size=40, color=DARK_PURPLE)
        gradb = MathTex(r"\frac{\partial L}{\partial b^{(l)}} = \delta^{(l)}",
                        font_size=40, color=DARK_PURPLE).next_to(gradW, DOWN, buff=0.3)
        self.play(Write(gradW), Write(gradb), run_time=1)

        # 5.2 Gradient Descent Update
        update = MathTex(r"W^{(l)} \leftarrow W^{(l)} - \eta \frac{\partial L}{\partial W^{(l)}}",
                         font_size=44, color=BLACK)
        update.next_to(gradb, DOWN, buff=0.5)
        self.play(update.animate.shift(UP * 0), run_time=0.8)
        eta = update.get_part_by_tex(r"\eta")
        self.play(eta.animate.set_color(ORANGE).scale(1.2), run_time=0.2)
        self.play(eta.animate.set_color(ORANGE).scale(0.8333), run_time=0.2)

        # 5.3 Illustrative Weight Change
        w_label = MathTex(r"w_{11} = 0.5", font_size=36, color=GOLD).move_to(LEFT * 2 + UP * 1)
        self.play(FadeIn(w_label), run_time=0.5)
        example = MathTex(r"0.5 - 0.1 \cdot 0.2 = 0.48", font_size=36, color=BLACK).next_to(w_label, RIGHT, buff=1)
        self.play(Write(example), run_time=1)
        new_w = MathTex(r"w_{11} = 0.48", font_size=36, color=GOLD).move_to(w_label)
        self.play(Transform(w_label, new_w), run_time=0.7)

        self.wait(3)
        self.play(FadeOut(*self.mobjects), run_time=1)


class FinalRecapSlide(Scene):
    def construct(self):
        bullets = VGroup(*[
            Text(item, font_size=30, color=BLACK, font="Arial")
            for item in [
                "Forward pass",
                "Compute loss",
                "Backward pass (compute δ)",
                "Weight update"
            ]
        ]).arrange(DOWN, aligned_edge=LEFT).to_edge(LEFT)
        for b in bullets:
            self.play(FadeIn(b, run_time=0.5))
            self.wait(0.5)
        self.wait(2)
        self.play(FadeOut(bullets, run_time=1))
        self.wait()