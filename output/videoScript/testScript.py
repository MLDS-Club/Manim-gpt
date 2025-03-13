from manim import *

class CubeRootOf64(Scene):
    def construct(self):
        # Define the number
        number = 64
        cube_root = MathTex(r"\sqrt[3]{64} = ?")
        self.play(Write(cube_root))
        self.wait(1)

        # Show the prime factorization of the number
        prime_factorization = MathTex(r"64 = 2 \times 2 \times 2 \times 2 \times 2 \times 2")
        self.play(Transform(cube_root, prime_factorization))
        self.wait(1)

        # Group the factors into triples
        grouped_factors = MathTex(r"64 = (2 \times 2) \times (2 \times 2) \times (2 \times 2)")
        self.play(Transform(cube_root, grouped_factors))
        self.wait(1)

        # Simplify to 4 x 4 x 4
        simplified = MathTex(r"64 = 4 \times 4 \times 4")
        self.play(Transform(cube_root, simplified))
        self.wait(1)

        # Show the cube root
        result = MathTex(r"\sqrt[3]{64} = 4")
        self.play(Transform(cube_root, result))
        self.wait(2)