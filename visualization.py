
from manim import *

# --------------------------------------------------
# Kodowanie Huffmana – animacja na podstawie slajdów
# Manim Community Edition
# --------------------------------------------------

class HuffmanAnimation(Scene):

    def construct(self):

        self.camera.background_color = BLACK

        WHITE_COLOR = WHITE

        # Funkcja tworząca pojedynczy węzeł-symbol
        def symbol_node(symbol, frequency, radius=0.43):
            circle = Circle(
                radius=radius,
                color=WHITE_COLOR,
                stroke_width=2
            )

            arrow = Text(
                symbol,
                font_size=35,
                color=WHITE_COLOR
            )
            arrow.move_to(circle.get_center())

            number = Text(
                str(frequency),
                font_size=27,
                color=WHITE_COLOR
            )
            number.next_to(circle, DOWN, buff=0.12)

            return VGroup(circle, arrow, number)

        # Funkcja tworząca węzeł drzewa
        def tree_node(value, position, leaf=False):
            if leaf:
                shape = Rectangle(
                    width=1.05,
                    height=0.85,
                    color=WHITE,
                    stroke_width=2
                )
            else:
                shape = Circle(
                    radius=0.38,
                    color=WHITE,
                    stroke_width=2
                )

            shape.move_to(position)

            label = Text(
                str(value),
                font_size=25,
                color=WHITE
            )
            label.move_to(shape.get_center())

            return VGroup(shape, label)

        # Funkcja rysująca połączenie węzłów
        def connection(start, end, label=None, label_pos=None):
            line = Line(
                start,
                end,
                color=WHITE,
                stroke_width=2
            )

            result = VGroup(line)

            if label:
                txt = Text(
                    label,
                    font_size=20,
                    color=WHITE
                )
                txt.move_to(label_pos)
                result.add(txt)

            return result

        # ==========================================
        # ETAP 1 – Początkowy ciąg symboli
        # ==========================================

        arrows = ["↑", "↑", "←", "↓", "↓",
                  "←", "↑", "→", "↓", "↑",
                  "→", "↑"]

        sequence = VGroup()

        for i, symbol in enumerate(arrows):
            arrow = Text(symbol, font_size=45, color=WHITE)
            arrow.move_to(
                LEFT * 5.2 + RIGHT * i * 0.95
            )
            sequence.add(arrow)

        self.play(
            LaggedStart(
                *[FadeIn(x) for x in sequence],
                lag_ratio=0.12
            ),
            run_time=3
        )
        self.wait(1)

        self.play(FadeOut(sequence))

        # ==========================================
        # ETAP 2 – Częstotliwości symboli
        # ==========================================

        symbols = ["↑", "←", "↓", "→"]
        frequencies = [5, 2, 3, 2]

        nodes = VGroup()

        positions = [
            LEFT * 4.5,
            LEFT * 1.5,
            RIGHT * 1.5,
            RIGHT * 4.5
        ]

        for symbol, freq, pos in zip(
            symbols, frequencies, positions
        ):
            node = symbol_node(symbol, freq)
            node.move_to(pos)
            nodes.add(node)

        self.play(
            LaggedStart(
                *[Create(n[0]) for n in nodes],
                *[FadeIn(n[1:]) for n in nodes],
                lag_ratio=0.3
            ),
            run_time=3
        )

        self.wait(2)

        # ==========================================
        # ETAP 3 – Sortowanie częstotliwości
        # ==========================================

        sorted_symbols = [
            ("←", 2),
            ("→", 2),
            ("↓", 3),
            ("↑", 5)
        ]

        sorted_nodes = VGroup()

        for i, (symbol, freq) in enumerate(sorted_symbols):
            node = symbol_node(symbol, freq)
            node.move_to(positions[i])
            sorted_nodes.add(node)

        self.play(
            Transform(nodes, sorted_nodes),
            run_time=2
        )

        self.wait(1)

        # ==========================================
        # ETAP 4 – Połączenie dwóch najmniejszych
        # 2 + 2 = 4
        # ==========================================

        self.play(FadeOut(nodes))

        left_leaf = symbol_node("←", 2, 0.30)
        right_leaf = symbol_node("→", 2, 0.30)

        left_leaf.move_to(LEFT * 2 + DOWN * 1.4)
        right_leaf.move_to(RIGHT * 2 + DOWN * 1.4)

        parent = symbol_node("← →", 4, 0.65)
        parent.move_to(DOWN * 0.1)

        branches = VGroup(
            Line(
                parent.get_bottom(),
                left_leaf.get_top(),
                color=WHITE
            ),
            Line(
                parent.get_bottom(),
                right_leaf.get_top(),
                color=WHITE
            )
        )

        self.play(
            FadeIn(parent),
            FadeIn(left_leaf),
            FadeIn(right_leaf),
            run_time=2
        )

        self.play(Create(branches))
        self.wait(2)

        # ==========================================
        # ETAP 5 – Połączenie 3 + 4 = 7
        # ==========================================

        self.play(
            FadeOut(left_leaf),
            FadeOut(right_leaf),
            FadeOut(branches)
        )

        parent7 = symbol_node("↓ ← →", 7, 0.7)
        parent7.move_to(DOWN * 0.1)

        down3 = symbol_node("↓", 3, 0.35)
        down3.move_to(LEFT * 2 + DOWN * 1.5)

        self.play(
            Transform(parent, parent7),
            FadeIn(down3),
            run_time=2
        )

        branch3 = Line(
            parent.get_bottom(),
            down3.get_top(),
            color=WHITE
        )

        self.play(Create(branch3))
        self.wait(2)

        # ==========================================
        # ETAP 6 – Połączenie 5 + 7 = 12
        # ==========================================

        self.play(
            FadeOut(parent),
            FadeOut(down3),
            FadeOut(branch3)
        )

        node5 = symbol_node("↑", 5, 0.45)
        node7 = symbol_node("↓ ← →", 7, 0.6)

        node5.move_to(LEFT * 2)
        node7.move_to(RIGHT * 2)

        root12 = symbol_node("↑ ↓ ← →", 12, 0.8)
        root12.move_to(UP * 1.7)

        self.play(
            FadeIn(node5),
            FadeIn(node7),
            FadeIn(root12),
            run_time=2
        )

        root_branches = VGroup(
            Line(root12.get_bottom(), node5.get_top()),
            Line(root12.get_bottom(), node7.get_top())
        )

        self.play(Create(root_branches))
        self.wait(2)

        # ==========================================
        # ETAP 7 – Finalne drzewo Huffmana
        # ==========================================

        self.play(
            FadeOut(node5),
            FadeOut(node7),
            FadeOut(root12),
            FadeOut(root_branches)
        )

        # Pozycje węzłów
        p12 = UP * 2.8

        p5 = LEFT * 2.1 + UP * 1.2
        p7 = RIGHT * 1.4 + UP * 1.2

        p3 = LEFT * 0.1 + DOWN * 0.4
        p4 = RIGHT * 2.0 + DOWN * 0.4

        p_left = RIGHT * 1.1 + DOWN * 1.8
        p_right = RIGHT * 3.0 + DOWN * 1.8

        # Węzły wewnętrzne
        root = tree_node(12, p12)
        n7 = tree_node(7, p7)
        n4 = tree_node(4, p4)

        # Liście
        leaf5 = tree_node("↑ (5)", p5, leaf=True)
        leaf3 = tree_node("↓ (3)", p3, leaf=True)
        leaf2a = tree_node("← (2)", p_left, leaf=True)
        leaf2b = tree_node("→ (2)", p_right, leaf=True)

        # Krawędzie drzewa
        edges = VGroup(
            connection(
                p12 + DOWN * 0.38,
                p5 + UP * 0.42,
                "L = 0",
                LEFT * 2.3 + UP * 2.0
            ),
            connection(
                p12 + DOWN * 0.38,
                p7 + UP * 0.38,
                "R = 1",
                RIGHT * 0.3 + UP * 2.0
            ),
            connection(
                p7 + DOWN * 0.38,
                p3 + UP * 0.42,
                "L = 0",
                LEFT * 0.5 + UP * 0.35
            ),
            connection(
                p7 + DOWN * 0.38,
                p4 + UP * 0.38,
                "R = 1",
                RIGHT * 2.0 + UP * 0.35
            ),
            connection(
                p4 + DOWN * 0.38,
                p_left + UP * 0.42,
                "L = 0",
                RIGHT * 0.7 + DOWN * 0.8
            ),
            connection(
                p4 + DOWN * 0.38,
                p_right + UP * 0.42,
                "R = 1",
                RIGHT * 3.1 + DOWN * 0.8
            )
        )

        # Animowane rysowanie drzewa
        self.play(Create(root), run_time=1)

        self.play(
            Create(edges[0]),
            Create(edges[1]),
            FadeIn(leaf5),
            FadeIn(n7),
            run_time=2
        )

        self.play(
            Create(edges[2]),
            Create(edges[3]),
            FadeIn(leaf3),
            FadeIn(n4),
            run_time=2
        )

        self.play(
            Create(edges[4]),
            Create(edges[5]),
            FadeIn(leaf2a),
            FadeIn(leaf2b),
            run_time=2
        )

        self.wait(3)

        # ==========================================
        # ETAP 8 – Kody binarne
        # ==========================================

        self.play(
            FadeOut(edges),
            FadeOut(root),
            FadeOut(n7),
            FadeOut(n4),
            FadeOut(leaf5),
            FadeOut(leaf3),
            FadeOut(leaf2a),
            FadeOut(leaf2b)
        )

        title = Text(
            "Kody Huffmana",
            font_size=42,
            color=WHITE
        )
        title.to_edge(UP)

        results = VGroup(
            Text("↑     0", font_size=38),
            Text("↓     10", font_size=38),
            Text("←     110", font_size=38),
            Text("→     111", font_size=38)
        )

        results.arrange(
            DOWN,
            aligned_edge=LEFT,
            buff=0.4
        )

        self.play(Write(title))

        for result in results:
            self.play(Write(result), run_time=1)

        self.wait(4)

        self.play(
            FadeOut(title),
            FadeOut(results)
        )
