from manim import *

class BubbleSortScene(Scene):
    def construct(self):
        # Initial list
        values = [5, 2, 4, 1, 3]
        n = len(values)

        # Bar parameters
        bar_width = 0.8
        spacing = 0.4
        max_height = max(values)

        # Create bars and labels
        bars = VGroup()
        labels = VGroup()
        for val in values:
            bar = Rectangle(
                width=bar_width,
                height=val,
                fill_color=BLUE,
                fill_opacity=0.8,
                stroke_color=WHITE,
                stroke_width=2
            )
            bars.add(bar)
        bars.arrange(RIGHT, buff=spacing)
        # Align bars to bottom
        bars.set_y(-3 + max_height / 2)

        for bar, val in zip(bars, values):
            lbl = MathTex(f"{val}", font_size=24, color=WHITE)
            lbl.next_to(bar, UP, buff=0.1)
            labels.add(lbl)

        # Display initial bars & labels
        self.play(
            *[GrowFromCenter(bar) for bar in bars],
            *[Write(lbl) for lbl in labels],
            run_time=1.5
        )
        self.wait(1)

        # Bubble sort animation
        for i in range(n):
            for j in range(n - 1 - i):
                bar1, bar2 = bars[j], bars[j + 1]
                lbl1, lbl2 = labels[j], labels[j + 1]

                # Highlight comparison
                comp_text = MathTex(
                    f"\\text{{Compare }}{values[j]}\\;>\\;{values[j+1]}?",
                    font_size=28,
                    color=YELLOW
                ).to_edge(UP)
                self.play(
                    bar1.animate.set_fill(YELLOW),
                    bar2.animate.set_fill(YELLOW),
                    Write(comp_text),
                    run_time=0.5
                )
                self.wait(0.6)

                # Swap bars if out of order
                if values[j] > values[j + 1]:
                    shift = bar_width + spacing
                    self.play(
                        bar1.animate.shift(RIGHT * shift),
                        bar2.animate.shift(LEFT * shift),
                        lbl1.animate.shift(RIGHT * shift),
                        lbl2.animate.shift(LEFT * shift),
                        run_time=0.8
                    )
                    # Update data
                    bars[j], bars[j + 1] = bars[j + 1], bars[j]
                    labels[j], labels[j + 1] = labels[j + 1], labels[j]
                    values[j], values[j + 1] = values[j + 1], values[j]

                self.wait(0.4)
                # Unhighlight & remove comparison text
                self.play(
                    bar1.animate.set_fill(BLUE),
                    bar2.animate.set_fill(BLUE),
                    FadeOut(comp_text),
                    run_time=0.5
                )
                self.wait(0.3)

            # Mark sorted bar
            sorted_bar = bars[n - 1 - i]
            self.play(sorted_bar.animate.set_fill(GREEN), run_time=0.6)
            self.wait(0.4)

        self.wait(1.2)