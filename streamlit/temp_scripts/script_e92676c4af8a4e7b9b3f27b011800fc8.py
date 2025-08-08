from manim import *
import numpy as np

class KnightMoveScene(Scene):
    def construct(self):
        # Draw chessboard
        board = VGroup()
        colors = [WHITE, LIGHT_GRAY]
        for row in range(8):
            for col in range(8):
                square = Square(side_length=1, stroke_color=BLACK, stroke_width=2)
                square.set_fill(colors[(row + col) % 2], opacity=1)
                square.move_to(np.array([col - 3.5, row - 3.5, 0]))
                board.add(square)
        # File labels (a–h)
        files = ["a","b","c","d","e","f","g","h"]
        file_labels = VGroup()
        for i, f in enumerate(files):
            lbl = Text(f, font_size=24, color=BLACK)
            lbl.move_to(np.array([i - 3.5, -4 + 0.2, 0]))
            file_labels.add(lbl)
        # Rank labels (1–8)
        ranks = [str(i) for i in range(1,9)]
        rank_labels = VGroup()
        for j, r in enumerate(ranks):
            lbl = Text(r, font_size=24, color=BLACK)
            lbl.move_to(np.array([-4 + 0.2, j - 3.5, 0]))
            rank_labels.add(lbl)

        # Render board and labels
        self.play(
            *[Create(sq) for sq in board],
            *[Write(lbl) for lbl in file_labels],
            *[Write(lbl) for lbl in rank_labels],
            run_time=2
        )
        self.wait(1)

        # Place knight at d4
        start_file = "d"
        start_rank = "4"
        start_col = files.index(start_file)
        start_row = ranks.index(start_rank)
        start_pos = np.array([start_col - 3.5, start_row - 3.5, 0])

        knight = Text("N", font_size=48, color=BLUE).move_to(start_pos)
        knight_coord = Text(f"{start_file}{start_rank}", font_size=24, color=BLUE)
        knight_coord.next_to(knight, UP, buff=0.1)
        self.play(FadeIn(knight), Write(knight_coord), run_time=1)
        self.wait(1)

        # Highlight all legal knight moves from d4
        offsets = [(2,1),(1,2),(-1,2),(-2,1),(-2,-1),(-1,-2),(1,-2),(2,-1)]
        for dx, dy in offsets:
            col = start_col + dx
            row = start_row + dy
            if 0 <= col < 8 and 0 <= row < 8:
                target = np.array([col - 3.5, row - 3.5, 0])
                # translucent highlight square
                highlight = Square(1).set_fill(YELLOW, opacity=0.5).set_stroke(width=0)
                highlight.move_to(target)
                # arrow from origin to target
                arrow = Arrow(start_pos, target, buff=0, color=YELLOW)
                # coordinate label
                coord = Text(f"{files[col]}{ranks[row]}", font_size=24, color=YELLOW)
                coord.next_to(highlight, UP, buff=0.1)

                self.play(FadeIn(highlight), GrowArrow(arrow), Write(coord), run_time=1)
                self.wait(0.5)
                self.play(FadeOut(highlight), FadeOut(arrow), FadeOut(coord), run_time=0.5)

        self.wait(2)