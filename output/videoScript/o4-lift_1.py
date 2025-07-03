from manim import *
import numpy as np

OFF_WHITE = "#F5F5DC"

def make_airfoil():
    pts = [
        (-3,  0,    0), (-2.5,  0.3,  0), (-1.5,  0.4,  0),
        (-0.5, 0.35, 0), (0,    0.3,  0), (0.5,  0.35, 0),
        (1.5,  0.4,  0), (2.5,  0.3,  0), (3,    0,    0),
        (2.5, -0.1,  0), (1.5, -0.2,  0), (0.5, -0.15, 0),
        (0,   -0.1,  0), (-0.5,-0.15, 0), (-1.5,-0.2,  0),
        (-2.5,-0.1,  0)
    ]
    return Polygon(*[np.array(p) for p in pts],
                   color=DARK_GRAY, fill_color="#444444", fill_opacity=1, stroke_width=3)

class Scene1_AirfoilFreestream(Scene):
    def construct(self):
        bg = Rectangle(width=config.frame_width, height=config.frame_height,
                       fill_color=OFF_WHITE, fill_opacity=1).set_z_index(-1)
        axis = Line(LEFT*config.frame_width/2, RIGHT*config.frame_width/2,
                    stroke_color=LIGHT_GRAY, stroke_width=2)
        airfoil = make_airfoil()
        arrow1 = Arrow(LEFT*6+UP*0.5, LEFT*2+UP*0.5, color=BLUE, stroke_width=6)
        arrow2 = Arrow(LEFT*6+DOWN*0.5, LEFT*2+DOWN*0.5, color=BLUE, stroke_width=6)
        label1 = Text("U∞", font_size=36, color=BLUE).next_to(arrow1.get_end(), RIGHT, buff=0.2)
        label2 = Text("U∞", font_size=36, color=BLUE).next_to(arrow2.get_end(), RIGHT, buff=0.2)
        arrow1.shift(LEFT*5); label1.shift(LEFT*5)
        arrow2.shift(LEFT*5); label2.shift(LEFT*5)
        self.play(FadeIn(bg), run_time=0.5)
        self.play(FadeIn(axis), FadeIn(airfoil), run_time=0.5)
        self.play(arrow1.animate.shift(RIGHT*5),
                  label1.animate.shift(RIGHT*5),
                  arrow2.animate.shift(RIGHT*5),
                  label2.animate.shift(RIGHT*5),
                  run_time=0.7)
        self.add(arrow1, arrow2, label1, label2)
        self.wait(1.5)

class Scene2_StreamlinesTravelDistance(Scene):
    def construct(self):
        axis = Line(LEFT*config.frame_width/2, RIGHT*config.frame_width/2,
                    stroke_color=LIGHT_GRAY, stroke_width=2)
        airfoil = make_airfoil()
        self.add(axis, airfoil)
        reds = VGroup()
        for i in range(5):
            dy = 1 + 0.2*i
            curve = ParametricFunction(
                lambda t, dy=dy: np.array([t, dy+0.3*np.sin(np.pi*(t+3)/6), 0]),
                t_range=[-3,3,0.01], stroke_color="#E24A33"
            )
            reds.add(curve)
        greens = VGroup()
        for i in range(5):
            dy = -1 - 0.2*i
            curve = ParametricFunction(
                lambda t, dy=dy: np.array([t, dy-0.3*np.sin(np.pi*(t+3)/6), 0]),
                t_range=[-3,3,0.01], stroke_color="#348ABD"
            )
            greens.add(curve)
        for r in reds:
            self.play(Create(r), run_time=0.3)
        for g in greens:
            self.play(Create(g), run_time=0.3)
        dotA = Dot([-2,1,0], color=RED)
        labelA = Text("A", font_size=24).next_to(dotA, UP, buff=0.1)
        dotB = Dot([-2,-1,0], color=GREEN)
        labelB = Text("B", font_size=24).next_to(dotB, DOWN, buff=0.1)
        self.play(FadeIn(VGroup(dotA, labelA, dotB, labelB)), run_time=0.3)
        self.wait(1)

        start_up = reds[0].points[0]
        end_up   = reds[0].points[-1]
        start_dn = greens[0].points[0]
        end_dn   = greens[0].points[-1]
        arrow_up   = CurvedArrow(start_up,   end_up,   angle=PI/3,  color=BLACK)
        text_s1    = Text("Distance s₁", font_size=28).next_to(arrow_up, UP, buff=0.1)
        arrow_down = CurvedArrow(start_dn, end_dn, angle=-PI/3, color=BLACK)
        text_s2    = Text("Distance s₂", font_size=28).next_to(arrow_down, DOWN, buff=0.1)
        dash1      = DashedLine(start_up,   end_up,   dash_length=0.1, color=BLACK)
        labelL1    = Text("L₁", font_size=24).move_to((start_up+end_up)/2 + UP*0.2)
        dash2      = DashedLine(start_dn, end_dn, dash_length=0.1, color=BLACK)
        labelL2    = Text("L₂", font_size=24).move_to((start_dn+end_dn)/2 + DOWN*0.2)
        self.play(FadeIn(VGroup(arrow_up, text_s1, arrow_down, text_s2)), run_time=0.5)
        self.play(Create(dash1), Create(dash2), run_time=0.7)
        self.play(FadeIn(VGroup(labelL1, labelL2)), run_time=0.2)
        self.wait(1.5)

class Scene3_VelocityBernoulli(Scene):
    def construct(self):
        axis = Line(LEFT*config.frame_width/2, RIGHT*config.frame_width/2,
                    stroke_color=LIGHT_GRAY, stroke_width=2)
        airfoil = make_airfoil()
        self.add(axis, airfoil)
        te = np.array([3,0,0])
        v1 = Arrow(te, te+UP,    color=PURPLE, stroke_width=4)
        v2 = Arrow(te, te+DOWN,  color=PURPLE, stroke_width=4)
        l1 = Text("v₁↑", font_size=40, color=PURPLE).next_to(v1.get_end(), UP,    buff=0.1)
        l2 = Text("v₂↓", font_size=40, color=PURPLE).next_to(v2.get_end(), DOWN,  buff=0.1)
        val1 = MathTex(r"v_1 = ?", font_size=32).next_to(l1, RIGHT, buff=0.2)
        val2 = MathTex(r"v_2 = ?", font_size=32).next_to(l2, RIGHT, buff=0.2)
        self.play(FadeOut(axis, airfoil), run_time=0.7)
        self.play(FadeIn(v1, v2, l1, l2, val1, val2), run_time=0.5)
        self.wait(1)

        eq = MathTex(r"P + \tfrac{1}{2}\rho v^2 = \mathrm{constant}", font_size=36).to_edge(UP)
        box1 = Rectangle(3,1, stroke_color=BLACK, stroke_width=2).shift(LEFT*3+DOWN*1)
        txt1 = Text("Region 1", font_size=24).move_to(box1.get_top()+DOWN*0.2)
        expr1 = MathTex(r"P_1 + \tfrac{1}{2}\rho v_1^2", font_size=24).move_to(box1)
        expr1[0].set_color(GREEN); expr1[2].set_color(PURPLE)
        box2 = Rectangle(3,1, stroke_color=BLACK, stroke_width=2).shift(RIGHT*3+UP*1)
        txt2 = Text("Region 2", font_size=24).move_to(box2.get_top()+DOWN*0.2)
        expr2 = MathTex(r"P_2 + \tfrac{1}{2}\rho v_2^2", font_size=24).move_to(box2)
        expr2[0].set_color(GREEN); expr2[2].set_color(PURPLE)
        for m,d in [(box1, LEFT*5),(txt1,LEFT*5),(expr1,LEFT*5),
                    (box2,RIGHT*5),(txt2,RIGHT*5),(expr2,RIGHT*5)]:
            m.shift(d)
        self.play(Write(eq), run_time=1)
        self.play(
            box1.animate.shift(-LEFT*5), txt1.animate.shift(-LEFT*5), expr1.animate.shift(-LEFT*5),
            box2.animate.shift(-RIGHT*5), txt2.animate.shift(-RIGHT*5), expr2.animate.shift(-RIGHT*5),
            run_time=0.7
        )
        self.wait(2)

class Scene4_PressureDistributionLift(Scene):
    def construct(self):
        airfoil = make_airfoil()
        self.add(airfoil)
        normals = VGroup()
        xs = np.linspace(-2.5, 2.5, 6)
        for x in xs:
            normals.add(Line([x,0,0],[x,0.2,0], color=GRAY, stroke_width=2))
        self.play(FadeIn(normals), run_time=0.5)
        for x in xs:
            ad = Arrow([x,-0.05,0],[x,-0.3,0], color=GREEN, stroke_width=4)
            l1 = Text("P₁", font_size=20, color=GREEN).next_to(ad, DOWN, buff=0.1)
            self.play(Create(ad), Write(l1), run_time=0.3)
            au = Arrow([x,0.05,0],[x,0.25,0], color=GREEN, stroke_width=4)
            l2 = Text("P₂", font_size=20, color=GREEN).next_to(au, UP, buff=0.1)
            self.play(Create(au), Write(l2), run_time=0.3)
        delta = Text("ΔP = P₁ − P₂", font_size=40, color=GREEN).to_edge(UP)
        self.play(FadeIn(delta), run_time=0.7)
        self.wait(2)

        strip = Rectangle(0.5,0.1, fill_color=YELLOW, fill_opacity=0.5)
        strip.shift(DOWN*2)
        dA = Text("dA", font_size=30).next_to(strip, UP, buff=0.1)
        self.play(strip.animate.shift(UP*2), Write(dA), run_time=0.6)
        df = Arrow(strip.get_center(), strip.get_center()+UP*0.5, color=GREEN, stroke_width=4)
        self.play(Create(df), run_time=0.5)
        form = Text("dF = ΔP dA", font_size=34).next_to(strip, RIGHT, buff=0.5)
        self.play(Write(form), run_time=0.5)
        self.wait(1.5)

class Scene5_ResultantLiftRecap(Scene):
    def construct(self):
        airfoil = make_airfoil()
        self.add(airfoil)
        lift = Arrow([0,0,0],[0,2,0], color=TEAL, stroke_width=6)
        lbl  = Text("L (Lift)", font_size=44, color=TEAL).next_to(lift.get_end(), UP, buff=0.2)
        formula = MathTex(
            r"L = \int_A (P_1 - P_2)\,dA = \int_A \rho \frac{(v_2^2 - v_1^2)}{2}\,dA",
            font_size=38
        ).next_to(lift, DOWN, buff=1)
        self.play(GrowArrow(lift), run_time=0.6)
        self.play(Write(lbl), run_time=0.4)
        self.play(FadeIn(formula), run_time=0.8)
        self.wait(3)
        self.play(self.camera.frame.animate.scale(0.9), run_time=2)

class Scene6_Outro(Scene):
    def construct(self):
        rect = Rectangle(width=config.frame_width, height=config.frame_height,
                         color=BLACK, fill_opacity=1).set_z_index(-1)
        text = Text("Thanks for watching! Learn more in our next video.",
                    font_size=32, color=WHITE)
        self.play(FadeIn(rect), FadeIn(text), run_time=1)
        self.wait(2)