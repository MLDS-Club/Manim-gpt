from manim import *

class OrbitalDistanceScene(Scene):
    def construct(self):
        # Title
        title = Text("Bohr Model: Electron Orbital Radius", font_size=48)
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))
        # Derivation steps
        step1 = MathTex("F_C = \\frac{k e^2}{r^2}", color=YELLOW).to_edge(LEFT).shift(UP*2)
        step2 = MathTex("F_{centripetal} = \\frac{m v^2}{r}", color=YELLOW).next_to(step1, DOWN, aligned_edge=LEFT)
        self.play(Write(step1), Write(step2), run_time=2)
        self.wait(1)
        eq1 = MathTex("\\frac{k e^2}{r^2} = \\frac{m v^2}{r}").next_to(step2, DOWN, aligned_edge=LEFT)
        self.play(Write(eq1), run_time=2)
        self.wait(1)
        sol1 = MathTex("m v^2 r = k e^2").next_to(eq1, DOWN, aligned_edge=LEFT)
        sol2 = MathTex("m v r = n \\hbar \\quad\\Rightarrow\\quad v = \\frac{n \\hbar}{m r}").next_to(sol1, DOWN, aligned_edge=LEFT)
        sol3 = MathTex("r = \\frac{n^2 \\hbar^2}{m k e^2} = a_0 n^2").next_to(sol2, DOWN, aligned_edge=LEFT)
        self.play(Write(sol1), Write(sol2), run_time=2)
        self.wait(1)
        self.play(Write(sol3), run_time=2)
        self.wait(1)
        a0def = MathTex("a_0 = \\frac{\\hbar^2}{m k e^2} \\approx 5.29 \\times 10^{-11}\\mathrm{m}").next_to(sol3, DOWN, aligned_edge=LEFT)
        self.play(Write(a0def), run_time=2)
        self.wait(2)
        # Clear formulas, show orbit
        self.play(*[FadeOut(mob) for mob in [step1, step2, eq1, sol1, sol2, sol3, a0def]])
        # Draw orbit and electron
        orbit = Circle(radius=2, color=BLUE)
        electron = Dot(point=orbit.point_at_angle(0), color=RED)
        radius_line = always_redraw(lambda: Line(ORIGIN, electron.get_center(), color=GREEN))
        label_r = Text("r_1 = a_0", font_size=24).next_to(radius_line, RIGHT, buff=0.2)
        self.play(Create(orbit), Create(radius_line), FadeIn(electron), FadeIn(label_r))
        self.wait(1)
        # Animate electron around orbit
        self.play(MoveAlongPath(electron, orbit), rate_func=linear, run_time=4)
        self.wait(2)