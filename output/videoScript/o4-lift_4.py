from manim import *
import numpy as np

class WingAirflowComparison(Scene):
    def construct(self):
        #################################
        # Segment 1: Wing Cross-Section and Basic Airflow
        #################################

        # Shot 1: Clean Slate
        plane = NumberPlane(
            x_range=[-8, 8, 1],
            y_range=[-4, 4, 1],
            background_line_style={
                "stroke_color": GREY,
                "stroke_width": 1,
                "stroke_opacity": 0.2,
            },
        )
        self.play(FadeIn(plane, run_time=1))
        self.wait()

        # Shot 2: Draw the Airfoil (NACA 0012 style)
        def thickness(x, c=6, t=0.12):
            return 5 * t * c * (
                0.2969 * np.sqrt(x / c)
                - 0.1260 * (x / c)
                - 0.3516 * (x / c) ** 2
                + 0.2843 * (x / c) ** 3
                - 0.1015 * (x / c) ** 4
            )

        upper = ParametricFunction(
            lambda u: np.array([
                -3 + 6 * u,
                thickness(6 * u),
                0
            ]),
            t_range=[0, 1],
            color=WHITE,
            stroke_width=4,
        )
        lower = ParametricFunction(
            lambda u: np.array([
                -3 + 6 * u,
                -thickness(6 * u),
                0
            ]),
            t_range=[1, 0],
            color=WHITE,
            stroke_width=4,
        )
        airfoil = VGroup(upper, lower)
        lead_pt = airfoil.get_left()
        trail_pt = airfoil.get_right()
        leading_label = Text("Leading edge", font_size=36, color=YELLOW_E).next_to(lead_pt, UP)
        trailing_label = Text("Trailing edge", font_size=36, color=YELLOW_E).next_to(trail_pt, DOWN)
        self.play(Write(airfoil), Write(leading_label), Write(trailing_label), run_time=2)
        self.wait()

        # Shot 3: Introduce Streamlines
        y_levels = [0.5, 1.0, 1.5, 2.0]
        above_streams = VGroup(*[
            Line(start=[-30, y, 0], end=[-10, y, 0], color=Color("#87CEEB"), stroke_width=2, stroke_opacity=0.5)
            for y in y_levels
        ])
        below_streams = VGroup(*[
            Line(start=[-30, -y, 0], end=[-10, -y, 0], color=Color("#AFEEEE"), stroke_width=2, stroke_opacity=0.5)
            for y in y_levels
        ])
        self.play(
            *[stream.animate.shift(RIGHT * 20) for stream in above_streams],
            *[stream.animate.shift(RIGHT * 20) for stream in below_streams],
            run_time=1
        )
        self.wait(1.5)

        # Shot 4: Speed Difference Hint
        t_tracker = ValueTracker(0)
        t_tracker.add_updater(lambda m, dt: m.set_value(m.get_value() + dt))
        def pulse(mob):
            mob.set_stroke(width=2 + np.sin(2 * PI * t_tracker.get_value() / 0.8))
        for s in above_streams:
            s.add_updater(pulse)
        caption1 = Text("Faster flow → Lower pressure", font_size=28, color=WHITE).to_edge(DOWN)
        self.add(t_tracker)
        self.play(FadeIn(caption1))
        self.wait(2)
        for s in above_streams:
            s.remove_updater(pulse)
        t_tracker.clear_updaters()

        #################################
        # Segment 2: Takeoff Configuration and Airflow Patterns
        #################################
        self.clear()

        # Shot 1: Wing at Takeoff Attitude
        # Redefine airfoil
        upper2 = upper.copy()
        lower2 = lower.copy()
        wing = VGroup(upper2, lower2)
        # Flaps
        flap1 = Rectangle(width=1.2, height=0.2, color=WHITE).next_to(lower2.get_right(), LEFT, buff=0)
        flap2 = Rectangle(width=1.2, height=0.2, color=WHITE).next_to(upper2.get_right(), LEFT, buff=0)
        for f in (flap1, flap2):
            f.rotate(-15 * DEGREES, about_point=f.get_left())
        wing_and_flaps = VGroup(wing, flap1, flap2).rotate(8 * DEGREES, about_point=np.array([-1.5, 0, 0]))
        label2 = Text("Flaps Down", font_size=32, color=ORANGE).next_to(wing_and_flaps, DOWN + RIGHT)
        wing_and_flaps.shift(RIGHT * 10)
        self.play(wing_and_flaps.animate.shift(LEFT * 10), FadeIn(label2), run_time=1)
        self.wait()

        # Shot 2: High-speed Streamlines
        y2_above = np.linspace(0.4 * 3 / 2, 0.4 * -3 / -2, 6)
        y2_below = np.linspace(-0.8 * 3 / 2, -0.8 * -3 / -2, 6)
        arrows = VGroup()
        for y in y2_above:
            arr = Arrow(start=wing_and_flaps.get_left() + np.array([-10, y, 0]),
                        end=wing_and_flaps.get_left() + np.array([10, y, 0]),
                        stroke_width=2, color=CYAN)
            arrows.add(arr)
        for y in y2_below:
            arr = Arrow(start=wing_and_flaps.get_left() + np.array([-10, y, 0]),
                        end=wing_and_flaps.get_left() + np.array([10, y, 0]),
                        stroke_width=2, color=BLUE_E)
            arrows.add(arr)
        self.play(*[GrowFromEdge(a, edge=LEFT) for a in arrows], run_time=1.5)
        self.wait()

        # Shot 3: Pressure Zones
        red_fill = Rectangle(width=6, height=2, fill_color=RED, fill_opacity=0.3, stroke_opacity=0).shift(wing_and_flaps.get_center() + DOWN)
        blue_fill = Rectangle(width=6, height=2, fill_color=BLUE, fill_opacity=0.3, stroke_opacity=0).shift(wing_and_flaps.get_center() + UP)
        lbl_high = Text("High Pressure", font_size=30, color=RED).next_to(red_fill, UP)
        lbl_low = Text("Low Pressure", font_size=30, color=BLUE).next_to(blue_fill, UP)
        self.play(FadeIn(red_fill), FadeIn(blue_fill), run_time=1)
        lbl_high.shift(DOWN)
        lbl_low.shift(DOWN)
        self.play(lbl_high.animate.shift(UP), lbl_low.animate.shift(UP))
        self.wait(2)

        # Shot 4: Vortex Tip Formation (Optional Detail)
        tips = [np.array([-3, 0, 0]), np.array([3, 0, 0])]
        vortices = VGroup()
        for tip in tips:
            circle = Circle(radius=0.1, color=WHITE).move_to(tip)
            swirl1 = Arc(radius=0.15, start_angle=PI/2, angle=-2 * PI, color=PURPLE)
            swirl2 = Arc(radius=0.25, start_angle=PI/2, angle=-2 * PI, color=PURPLE)
            swirl = VGroup(circle, swirl1, swirl2).move_to(tip)
            swirl.add_updater(lambda m, dt, p=tip: m.rotate(60 * DEGREES * dt, about_point=p))
            lbl = Text("Tip Vortex", font_size=28, color=PURPLE).next_to(tip, RIGHT)
            vortices.add(VGroup(swirl, lbl))
        self.play(*[FadeIn(v[0]) for v in vortices], run_time=1)
        for v in vortices:
            self.add(v[0])
            self.play(FadeIn(v[1]), run_time=0.5)
        self.wait(2)

        #################################
        # Segment 3: Landing Configuration and Airflow Patterns
        #################################
        self.clear()

        # Shot 1: Wing at Landing Attitude
        upper3 = upper.copy()
        lower3 = lower.copy()
        wing3 = VGroup(upper3, lower3).rotate(12 * DEGREES, about_point=np.array([-1.5, 0, 0]))
        # Flaps 30°
        f1 = Rectangle(width=1.2, height=0.2, color=WHITE).next_to(lower3.get_right(), LEFT, buff=0)
        f2 = Rectangle(width=1.2, height=0.2, color=WHITE).next_to(upper3.get_right(), LEFT, buff=0)
        for f in (f1, f2):
            f.rotate(-30 * DEGREES, about_point=f.get_left())
        # Slats
        s1 = Rectangle(width=0.4, height=0.2, color=WHITE).next_to(upper3.get_left(), RIGHT, buff=0)
        slats = VGroup(s1)
        hl = Text("High-Lift Devices", font_size=32, color=GREEN_SCREEN).next_to(wing3, UP)
        self.play(FadeIn(wing3), run_time=1)
        self.play(FadeIn(slats), run_time=0.5)
        self.play(Write(hl), run_time=0.5)
        self.wait()

        # Shot 2: Dense Turbulent Flow
        main_streams = VGroup()
        for y in np.linspace(0.4 * 4, 0.4, 8):
            main_streams.add(Arrow(wing3.get_left() + np.array([-10, y, 0]),
                                   wing3.get_left() + np.array([10, y, 0]),
                                   color=CYAN, stroke_width=2))
        for y in np.linspace(-0.8 * 3, -0.8, 6):
            main_streams.add(Arrow(wing3.get_left() + np.array([-10, y, 0]),
                                   wing3.get_left() + np.array([10, y, 0]),
                                   color=BLUE_E, stroke_width=2))
        turb = VGroup(*[
            Line(start=wing3.get_right() + np.array([0, -0.5 + 0.2 * i, 0]),
                 end=wing3.get_right() + np.array([0.5, -0.3 + 0.2 * i, 0]),
                 color=LIGHT_BLUE)
            for i in range(4)
        ])
        self.play(*[GrowFromEdge(s, LEFT) for s in main_streams], run_time=1)
        # flicker turbulence
        for _ in range(4):
            self.play(FadeIn(turb), run_time=0.25)
            self.play(FadeOut(turb), run_time=0.25)
        self.wait()

        # Shot 3: Enhanced Wingtip Vortices
        tips2 = [-3, 3]
        vort2 = VGroup()
        for x in tips2:
            sw = Arc(radius=0.5, start_angle=PI/2, angle=-4 * PI, color=PURPLE).move_to([x, 0, 0])
            sw.add_updater(lambda m, dt, p=np.array([x,0,0]): m.rotate(90 * DEGREES * dt, about_point=p))
            trail = Line(start=[x,0,0], end=[x+6,0,0], color=PURPLE, stroke_opacity=0.6)
            vort2.add(VGroup(sw, trail))
        self.play(*[GrowFromEdge(v[1], LEFT) for v in vort2], run_time=2)
        for v in vort2:
            self.add(v[0])
        self.wait(2)

        # Shot 4: Pressure Map Overlay (pseudo-heatmap)
        heatmap = VGroup()
        for i in range(20):
            rect = Rectangle(width=6/20, height=1.5,
                             fill_color=interpolate_color(GREEN, RED, i/19),
                             fill_opacity=0.7, stroke_opacity=0)
            rect.next_to(wing3.get_left() + RIGHT * (i * 6/20 + 6/40), UP, buff=0)
            heatmap.add(rect)
        legend = VGroup(
            Rectangle(width=3, height=0.3, fill_color=BLUE, fill_opacity=1, stroke_opacity=0),
            Rectangle(width=3, height=0.3, fill_color=RED, fill_opacity=1, stroke_opacity=0),
            Text("Pressure", font_size=24, color=WHITE)
        ).arrange(DOWN, buff=0.1).to_corner(DL)
        self.play(FadeIn(heatmap), FadeIn(legend), run_time=0.8)
        self.wait(2)

        #################################
        # Segment 4: Takeoff vs. Landing Comparison
        #################################
        self.clear()

        # Shot 1: Split-Screen Setup
        left_box = Square(side_length=4, color=WHITE).shift(LEFT * 3)
        right_box = Square(side_length=4, color=WHITE).shift(RIGHT * 3)
        divider = Line(ORIGIN + UP * 2, ORIGIN + DOWN * 2, color=WHITE)
        # reuse simplified wings/demo
        demo_takeoff = wing_and_flaps.copy().move_to(left_box.get_center())
        demo_landing = wing3.copy().move_to(right_box.get_center())
        self.play(
            left_box.animate.shift(LEFT * 0), right_box.animate.shift(RIGHT * 0),
            Create(divider), run_time=1
        )
        self.play(FadeIn(demo_takeoff), FadeIn(demo_landing))
        self.wait()

        # Shot 2: Streamline Overlay
        lbl_to = Text("Takeoff", font_size=36, color=WHITE).next_to(left_box, UP)
        lbl_ld = Text("Landing", font_size=36, color=WHITE).next_to(right_box, UP)
        # simple pulsing on takeoff streams
        demo_ar_to = arrows.copy().move_to(left_box.get_center())
        demo_ar_ld = main_streams.copy().move_to(right_box.get_center())
        for l in demo_ar_to:
            l.add_updater(lambda m, dt: m.set_stroke(opacity=0.5 + 0.5 * np.sin(2 * PI * dt)))
        for l in demo_ar_ld:
            l.add_updater(lambda m, dt: m.set_opacity(0.5 + 0.5 * np.sin(2 * PI * dt)))
        self.play(FadeIn(lbl_to), FadeIn(lbl_ld), run_time=0.5)
        self.add(demo_ar_to, demo_ar_ld)
        self.wait()

        # Shot 3: Key Metrics Table
        table_data = [
            ["Parameter", "Takeoff vs. Landing"],
            ["Angle of Attack", "8° vs. 12°"],
            ["Flap Deflection", "15° vs. 30°"],
            ["Vortex Strength", "Medium vs. High"],
        ]
        table = Table(
            table_data,
            include_outer_lines=False,
            line_config={"stroke_opacity": 0},
            element_to_mobject=lambda text: Text(text, font_size=24 if text not in table_data[0] else 28, color=YELLOW)
        ).scale(1.2).to_edge(DOWN)
        for i, row in enumerate(table_data):
            if i == 0:
                continue
            self.play(FadeIn(table.get_rows()[i]), run_time=0.5)
        self.wait(3)

        # Shot 4: Conclusion and Call-Out
        dim = FullScreenRectangle(fill_color=BLACK, fill_opacity=0.6)
        highlight = Circle(radius=0.7, color=PURE_PURPLE, stroke_width=6).move_to(right_box.get_center())
        conclusion = Text("Managing airflow is crucial for safe takeoff and landing.", font_size=34, color=WHITE).to_edge(UP)
        self.play(FadeIn(dim), Create(highlight), Write(conclusion), run_time=1)
        for _ in range(2):
            self.play(highlight.animate.set_stroke(opacity=0), highlight.animate.set_stroke(opacity=1), run_time=0.5)
        self.wait(3)