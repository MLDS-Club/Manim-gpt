from manim import *
import numpy as np

class TakeoffLandingVisualization(ThreeDScene):
    def construct(self):
        # Segment 1 - Shot 1
        airfoil = Polygon(
            [-1.5, 0, 0], [-1.0, 0.2, 0], [-0.5, 0.25, 0], [0.0, 0.3, 0],
            [0.5, 0.25, 0], [1.0, 0.2, 0], [1.5, 0, 0], [1.0, -0.1, 0],
            [0.0, -0.15, 0], [-1.0, -0.1, 0],
            color=BLACK, fill_color=GRAY, fill_opacity=1
        ).rotate(5*DEGREES)
        le_label = Text("Leading Edge", color=WHITE, font_size=36).next_to(airfoil, LEFT+UP)
        te_label = Text("Trailing Edge", color=WHITE, font_size=36).next_to(airfoil, RIGHT+UP)
        ground = VGroup(
            Rectangle(width=12, height=0.2, fill_color=LIGHT_GRAY, fill_opacity=1),
            Line([-6, -2, 0], [6, -2, 0], color=DARK_GRAY)
        ).shift(DOWN*6)
        airfoil.shift(UP*3); le_label.shift(UP*3); te_label.shift(UP*3)

        self.play(FadeIn(airfoil, run_time=1.5), FadeIn(le_label, run_time=1.5), FadeIn(te_label, run_time=1.5))
        self.play(ground.animate.shift(UP*4), run_time=1)
        self.wait(1)

        # Segment 1 - Shot 2
        arrows = VGroup(*[
            Arrow(
                start=np.array([-8, y, 0]), end=np.array([-6, y, 0]),
                tip_length=0.15, stroke_width=3, color="#75C6E1"
            ).set_stroke(color="#75C6E1")
            for y in np.linspace(-0.5, 1.5, 10)
        ])
        for arr in arrows:
            arr.tip.set_color(WHITE)
        v_label = Text("V∞ = 80 m/s", color=WHITE, font_size=32).to_edge(UP)
        self.add(airfoil, le_label, te_label, ground)
        self.play(arrows.animate.shift(RIGHT*2), run_time=1)
        self.add(v_label)
        self.play(arrows.animate.shift(RIGHT*2), self.camera.frame.animate.shift(RIGHT*2), run_time=3, rate_func=linear)

        # Segment 1 - Shot 3
        self.play(FadeOut(arrows, run_time=0.5), FadeOut(v_label, run_time=0.5))
        underside = Polygon(
            [-1.5, -0.1, 0], [-1.5, 0, 0], [1.5, 0, 0], [1.5, -0.1, 0],
            fill_color="#49A078", fill_opacity=0.5, stroke_opacity=0
        ).move_to(airfoil.get_center())
        overside = Polygon(
            [-1.5, 0, 0], [-1.5, 0.3, 0], [1.5, 0.3, 0], [1.5, 0, 0],
            fill_color="#FF6961", fill_opacity=0.5, stroke_opacity=0
        ).move_to(airfoil.get_center())
        high_label = Text("High Pressure", color="#0366A6", font_size=28).next_to(underside, DOWN)
        low_label = Text("Low Pressure", color="#8B0000", font_size=28).next_to(overside, UP)

        above_curves = VGroup(*[
            CubicBezier(
                start_point=np.array([-6, y, 0]),
                control1=np.array([-2, y, 0]), control2=np.array([2, y+0.5, 0]),
                end_point=np.array([6, y, 0])
            ).set_color("#0366A6")
            for y in np.linspace(0.6, 1.4, 5)
        ])
        below_curves = VGroup(*[
            CubicBezier(
                start_point=np.array([-6, y, 0]),
                control1=np.array([-2, y, 0]), control2=np.array([2, y-0.3, 0]),
                end_point=np.array([6, y, 0])
            ).set_color("#49A078")
            for y in np.linspace(-0.6, -0.2, 5)
        ])

        self.play(
            self.camera.frame.animate.scale(1/1.2),
            FadeIn(underside, overside, high_label, low_label, run_time=1),
            Create(above_curves[0], run_time=0.8),
            Create(below_curves[0], run_time=0.8)
        )
        self.wait(0.2)
        for i in range(1, 5):
            self.play(Create(above_curves[i], run_time=0.8), Create(below_curves[i], run_time=0.8))
            self.wait(0.2)
        self.wait(2)

        # Segment 1 - Shot 4
        gline = DashedLine([-6, -1.2, 0], [6, -1.2, 0], color=YELLOW).shift(DOWN*6)
        glabel = Text("Ground Effect Zone", color=YELLOW, font_size=28).next_to(gline, UP).shift(DOWN*6)
        self.play(gline.animate.shift(UP*4.8), glabel.animate.shift(UP*4.8), run_time=1)
        self.play(underside.animate.set_fill(opacity=0.8), run_time=0.25)
        self.play(underside.animate.set_fill(opacity=0.5), run_time=0.25)
        self.wait(2)
        self.play(self.camera.frame.animate.shift(DOWN*0.5), run_time=1)

        # Segment 1 - Shot 5
        wing_back = airfoil.copy().set_color(GRAY).set_opacity(0.5)
        self.play(FadeIn(wing_back, run_time=0.7))
        vortex_left = Circle(radius=0.4, color=BLUE).move_to([-1.5, 0, 0])
        vortex_right = Circle(radius=0.4, color=RED).move_to([1.5, 0, 0])
        v_labelL = Text("Wingtip Vortex", font_size=24).next_to(vortex_left, DOWN)
        v_labelR = Text("Wingtip Vortex", font_size=24).next_to(vortex_right, DOWN)
        self.play(Create(vortex_left, run_time=1), Create(vortex_right, run_time=1))
        self.play(vortex_left.animate.rotate(PI/2, run_time=3), vortex_right.animate.rotate(-PI/2, run_time=3))
        self.play(self.camera.frame.animate.rotate(-10*DEGREES, axis=UP), run_time=2)

        self.play(FadeOut(VGroup(*[m for m in self.mobjects if m is not airfoil])), run_time=1)
        self.play(FadeOut(airfoil, run_time=1))
        self.wait(0.5)

        # Segment 2 - Shot 1
        wing2 = Polygon(*airfoil.get_vertices(), color=BLACK, fill_color=GRAY, fill_opacity=1).rotate(7*DEGREES).shift(UP*3)
        flap = Polygon([1.0, -0.05, 0], [1.0, 0.05, 0], [1.5, 0.05, 0], [1.5, -0.05, 0],
                       fill_color=DARK_GRAY, fill_opacity=1).rotate(-25*DEGREES, about_point=[1.5,0,0])
        hinge = Circle(radius=0.03, fill_color=BLACK).move_to([1.5,0,0])
        flap_label = Text("Flaps Down: +25°", color=WHITE, font_size=32).next_to(flap, DOWN)
        self.play(FadeIn(wing2, flap, hinge, flap_label, run_time=1))
        self.wait(1)

        # Segment 2 - Shot 2
        arc = Arc(radius=0.7, start_angle=0, angle=7*DEGREES, color=YELLOW).shift([-1.5,0,0])
        arc_label = Text("AOA +7°", color=YELLOW, font_size=32).next_to(arc, RIGHT)
        self.play(Create(arc, run_time=1), Write(arc_label, run_time=1))
        arrows2 = VGroup(*[
            Arrow(start=[-8, y, 0], end=[-6.5, y, 0], stroke_width=4, color=WHITE)
            for y in [-0.2,0.0,0.2,0.4]
        ])
        v2_label = Text("V∞ = 50 m/s", color=WHITE, font_size=32).next_to(arrows2, UP)
        self.play(FadeIn(arrows2), run_time=1)
        self.add(v2_label)
        self.play(arrows2.animate.shift(RIGHT*2), run_time=2)
        self.play(self.camera.frame.animate.scale(1/0.9), run_time=1)

        # Segment 2 - Shot 3
        band = Rectangle(width=0.6, height=0.005, fill_color=YELLOW, fill_opacity=1).move_to([-0.6,0.18,0])
        self.play(band.animate.stretch(4,1), run_time=1.5)
        bubble = Ellipse(width=0.4, height=0.2, fill_color=PINK, fill_opacity=1).move_to([0.0,0.15,0])
        self.play(Transform(band, bubble), run_time=1)
        red_arrows = VGroup(*[
            Arrow(start=[0.5+0.2*i,0.1,0], end=[0.6+0.2*i,0.1,0], color=RED, stroke_width=3)
            for i in range(3)
        ])
        for arr in red_arrows:
            self.play(FadeIn(arr), run_time=0.3)
            self.wait(0.3)
        self.wait(2)
        self.play(self.camera.frame.animate.shift(RIGHT*0.5), run_time=1)

        # Segment 2 - Shot 4
        wake_line = Line([1.5,0,0],[5,0,0], color=LIGHT_GRAY, stroke_opacity=0.5)
        vortices = VGroup(*[
            Circle(radius=0.2, color=(GREEN if i%2==0 else ORANGE)).move_to([1.5+0.5*i,0,0])
            for i in range(6)
        ])
        for v in vortices:
            self.play(Create(v), run_time=0.5)
            self.wait(0.4)
        self.add(wake_line)
        self.wait(2)
        self.play(VGroup(wake_line, vortices).animate.shift(RIGHT*6), run_time=1)
        self.play(self.camera.frame.animate.scale(1/0.9), run_time=1)

        # Segment 2 - Shot 5
        L = Arrow(start=[0,0,0], end=[0,1,0], color=GREEN)
        D = Arrow(start=[0,0,0], end=[-0.6,0,0], color=RED)
        L_label = Text("L", color=GREEN, font_size=30).next_to(L.get_end(), UP)
        D_label = Text("D", color=RED, font_size=30).next_to(D.get_end(), LEFT)
        self.play(FadeIn(L, run_time=0.7))
        self.play(FadeIn(D, run_time=0.7))
        self.play(self.camera.frame.animate.shift(UP*0.5), run_time=1)
        self.wait(3)

        # End Title
        end = Text("End of Visualization", color=WHITE, font_size=48)
        self.play(FadeOut(VGroup(*self.mobjects)), run_time=1)
        self.add(end)
        self.wait(2)