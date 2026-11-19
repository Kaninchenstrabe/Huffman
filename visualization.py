from manim import *
import numpy as np

# --------------------------------------------------
# Kodowanie Huffmana – płynna animacja budowy drzewa
# Manim Community Edition v0.22.1
# --------------------------------------------------


class HuffmanAnimation(Scene):
    TIME_SCALE = 2.0  # 2.0 = twice as long (half speed)

    def play(self, *args, **kwargs):
        kwargs["run_time"] = kwargs.get("run_time", 1.0) * self.TIME_SCALE
        return super().play(*args, **kwargs)

    def wait(self, duration=1.0, *args, **kwargs):
        return super().wait(duration * self.TIME_SCALE, *args, **kwargs)

    def construct(self):
        self.camera.background_color = BLACK

        NODE_RADIUS = 0.46
        FILL_BLUE = "#0D2B52"
        BORDER_BLUE = BLUE_B
        EDGE_COLOR = BLUE_A

        # Tworzy niebieski węzeł o stałym promieniu:
        # - w środku wyłącznie symbole (automatycznie ułożone i przeskalowane)
        # - pod kołem liczba wystąpień
        def create_node(symbols, freq, pos=ORIGIN):
            circle = Circle(
                radius=NODE_RADIUS,
                fill_color=FILL_BLUE,
                fill_opacity=1.0,
                stroke_color=BORDER_BLUE,
                stroke_width=3.0,
            )
            circle.move_to(pos)
            circle.set_z_index(2)

            n = len(symbols)
            sym_list = []
            if n == 1:
                t = Text(symbols[0], font_size=32, color=WHITE, weight=BOLD)
                sym_list.append(t)
                sym_group = t
            elif n == 2:
                sym_list = [
                    Text(s, font_size=26, color=WHITE, weight=BOLD) for s in symbols
                ]
                sym_group = VGroup(*sym_list).arrange(RIGHT, buff=0.10)
            elif n == 3:
                s0 = Text(symbols[0], font_size=22, color=WHITE, weight=BOLD)
                s1 = Text(symbols[1], font_size=22, color=WHITE, weight=BOLD)
                s2 = Text(symbols[2], font_size=22, color=WHITE, weight=BOLD)
                sym_list = [s0, s1, s2]
                top_row = VGroup(s0, s1).arrange(RIGHT, buff=0.08)
                sym_group = VGroup(top_row, s2).arrange(DOWN, buff=0.04)
            else:
                rows = []
                for i in range(0, n, 2):
                    row_syms = [
                        Text(s, font_size=20, color=WHITE, weight=BOLD)
                        for s in symbols[i : i + 2]
                    ]
                    sym_list.extend(row_syms)
                    rows.append(VGroup(*row_syms).arrange(RIGHT, buff=0.08))
                sym_group = VGroup(*rows).arrange(DOWN, buff=0.04)

            max_inner = NODE_RADIUS * 1.25
            if sym_group.width > max_inner:
                sym_group.scale(max_inner / sym_group.width)
            if sym_group.height > max_inner:
                sym_group.scale(max_inner / sym_group.height)

            sym_group.move_to(circle.get_center())
            sym_group.set_z_index(3)

            freq_text = Text(str(freq), font_size=23, color=BLUE_A, weight=BOLD)
            freq_text.set_stroke(color=BLACK, width=4, background=True)
            freq_text.next_to(circle, DOWN, buff=0.08)
            freq_text.set_z_index(3)

            node_group = VGroup(circle, sym_group, freq_text)
            return node_group, circle, sym_group, sym_list, freq_text

        # Tworzy skośną krawędź łączącą dokładnie brzegi dwóch okręgów
        def create_edge(parent_circle, child_circle):
            p1 = parent_circle.get_center()
            p2 = child_circle.get_center()
            vec = p2 - p1
            unit = vec / np.linalg.norm(vec)
            start = p1 + unit * NODE_RADIUS
            end = p2 - unit * NODE_RADIUS
            edge = Line(start, end, color=EDGE_COLOR, stroke_width=2.5)
            edge.set_z_index(0)
            return edge

        # Zbiera wszystkie obiekty (węzły i krawędzie) należące do poddrzewa
        def collect_subtree_mobjects(tree):
            mobs = [tree["node"]]
            if tree["left_edge"] is not None:
                mobs.append(tree["left_edge"])
            if tree["right_edge"] is not None:
                mobs.append(tree["right_edge"])
            if tree["left"] is not None:
                mobs.extend(collect_subtree_mobjects(tree["left"]))
            if tree["right"] is not None:
                mobs.extend(collect_subtree_mobjects(tree["right"]))
            return mobs

        # Zwraca listę animacji przesuwających całe poddrzewo tak,
        # aby środek jego korzenia znalazł się w target_center
        def move_subtree_anims(tree, target_center, path_arc=0.0):
            delta = target_center - tree["circle"].get_center()
            if np.linalg.norm(delta) < 1e-4:
                return []
            mobs = collect_subtree_mobjects(tree)
            return [m.animate(path_arc=path_arc).shift(delta) for m in mobs]

        # ==========================================
        # ETAP 1 – Początkowa sekwencja znaków
        # ==========================================
        arrows = ["↑", "↑", "←", "↓", "↓", "←", "↑", "→", "↓", "↑", "→", "↑"]

        seq_mobs = VGroup()
        for i, sym in enumerate(arrows):
            t = Text(sym, font_size=44, color=WHITE, weight=BOLD)
            t.move_to(LEFT * 5.5 + RIGHT * i * 1.0 + UP * 0.6)
            seq_mobs.add(t)

        self.play(
            LaggedStart(
                *[FadeIn(m, scale=0.82, rate_func=smooth) for m in seq_mobs],
                lag_ratio=0.22,
            ),
            run_time=3.2,
        )
        self.wait(0.8)

        # ==========================================
        # ETAP 2 – Gładkie przejście do posortowanej sekwencji
        # ==========================================
        symbol_order = ["↑", "←", "↓", "→"]
        grouped_indices = {s: [] for s in symbol_order}
        for idx, sym in enumerate(arrows):
            grouped_indices[sym].append(idx)

        sorted_order_indices = []
        for sym in symbol_order:
            sorted_order_indices.extend(grouped_indices[sym])

        sort_anims = []
        for target_slot, orig_idx in enumerate(sorted_order_indices):
            target_pos = LEFT * 5.5 + RIGHT * target_slot * 1.0 + UP * 1.6
            arc = 0.25 if target_slot % 2 == 0 else -0.25
            sort_anims.append(seq_mobs[orig_idx].animate(path_arc=arc).move_to(target_pos))

        self.play(*sort_anims, run_time=1.8)
        self.wait(0.7)

        # ==========================================
        # ETAP 3 – Zebranie tych samych znaków do węzłów
        # ==========================================
        node_x_positions = [-4.2, -1.4, 1.4, 4.2]
        TOP_Y = 2.4

        forest = []
        merge_anims = []

        for i, sym in enumerate(symbol_order):
            indices = grouped_indices[sym]
            freq = len(indices)
            pos = np.array([node_x_positions[i], TOP_Y, 0.0])

            node_group, circle, sym_group, _, freq_text = create_node(
                [sym], freq, pos=pos
            )
            cluster = VGroup(*[seq_mobs[idx] for idx in indices])

            merge_anims.append(GrowFromCenter(circle))
            merge_anims.append(ReplacementTransform(cluster, sym_group))
            merge_anims.append(FadeIn(freq_text, shift=UP * 0.15))

            forest.append(
                {
                    "symbols": [sym],
                    "freq": freq,
                    "node": node_group,
                    "circle": circle,
                    "left": None,
                    "right": None,
                    "left_edge": None,
                    "right_edge": None,
                }
            )

        self.play(*merge_anims, run_time=1.6)
        self.wait(0.9)

        # ==========================================
        # ETAPY 4 i 5 – Naprzemienne sortowanie i łączenie
        # dwóch najmniejszych węzłów aż do pełnego drzewa
        # ==========================================

        merge_layouts = [
            # Iteracja 1: połączenie ← (2) oraz → (2) -> ←→ (4)
            {
                "left_target": np.array([-3.9, 0.85, 0.0]),
                "right_target": np.array([-1.7, 0.85, 0.0]),
                "parent_pos": np.array([-2.8, 2.4, 0.0]),
                "rest_targets": [
                    np.array([0.9, 2.4, 0.0]),
                    np.array([3.7, 2.4, 0.0]),
                ],
            },
            # Iteracja 2: połączenie ↓ (3) oraz ←→ (4) -> ↓←→ (7)
            {
                "left_target": np.array([-3.5, 0.85, 0.0]),
                "right_target": np.array([-0.5, 0.85, 0.0]),
                "parent_pos": np.array([-2.0, 2.4, 0.0]),
                "rest_targets": [
                    np.array([3.2, 2.4, 0.0]),
                ],
            },
            # Iteracja 3: połączenie ↑ (5) oraz ↓←→ (7) -> ↑↓←→ (12)
            {
                "left_target": np.array([-4.4, 1.15, 0.0]),
                "right_target": np.array([-0.4, 1.15, 0.0]),
                "parent_pos": np.array([-2.4, 2.65, 0.0]),
                "rest_targets": [],
            },
        ]

        sort_x_layouts = [
            [-4.2, -1.4, 1.4, 4.2],   # 4 poddrzewa
            [-4.2, -1.1, 2.8],         # 3 poddrzewa
            [-4.1, -0.1],              # 2 poddrzewa
        ]

        for step_idx in range(3):
            # --- KROK 4: Sortowanie węzłów rosnąco po liczbie wystąpień ---
            forest.sort(key=lambda item: item["freq"])
            xs = sort_x_layouts[step_idx]

            step4_anims = []
            for idx, tree in enumerate(forest):
                target = np.array([xs[idx], TOP_Y, 0.0])
                arc = 0.25 if idx % 2 == 0 else -0.25
                step4_anims.extend(move_subtree_anims(tree, target, path_arc=arc))

            if step4_anims:
                self.play(*step4_anims, run_time=1.4)
                self.wait(0.6)

            # --- KROK 5: Opuszczenie 2 pierwszych węzłów i utworzenie rodzica ---
            layout = merge_layouts[step_idx]
            left_tree = forest[0]
            right_tree = forest[1]
            remaining_trees = forest[2:]

            drop_anims = []
            drop_anims.extend(move_subtree_anims(left_tree, layout["left_target"]))
            drop_anims.extend(move_subtree_anims(right_tree, layout["right_target"]))
            for r_tree, r_target in zip(remaining_trees, layout["rest_targets"]):
                drop_anims.extend(move_subtree_anims(r_tree, r_target))

            self.play(*drop_anims, run_time=1.3)

            parent_symbols = left_tree["symbols"] + right_tree["symbols"]
            parent_freq = left_tree["freq"] + right_tree["freq"]
            parent_pos = layout["parent_pos"]

            parent_node, parent_circle, _, parent_sym_list, parent_freq_txt = create_node(
                parent_symbols, parent_freq, pos=parent_pos
            )
            left_edge = create_edge(parent_circle, left_tree["circle"])
            right_edge = create_edge(parent_circle, right_tree["circle"])

            # Najpierw koło i krawędzie, potem powolne pojawienie się strzałek w środku
            self.play(
                GrowFromCenter(parent_circle),
                FadeIn(parent_freq_txt, shift=UP * 0.12),
                Create(left_edge),
                Create(right_edge),
                run_time=1.0,
            )
            self.play(
                LaggedStart(
                    *[FadeIn(s, scale=0.8, rate_func=smooth) for s in parent_sym_list],
                    lag_ratio=0.35,
                ),
                run_time=1.4,
            )
            self.wait(0.7)

            merged_tree = {
                "symbols": parent_symbols,
                "freq": parent_freq,
                "node": parent_node,
                "circle": parent_circle,
                "left": left_tree,
                "right": right_tree,
                "left_edge": left_edge,
                "right_edge": right_edge,
            }
            forest = [merged_tree] + remaining_trees

        root_tree = forest[0]

        # ==========================================
        # ETAP 6 – Etykiety 0/1 na krawędziach i wyznaczanie kodów
        # ==========================================
        edge_labels = VGroup()

        def attach_bit_labels(tree):
            if tree["left"] is not None:
                edge = tree["left_edge"]
                vec = edge.get_end() - edge.get_start()
                dx, dy = vec[0], vec[1]
                perp = np.array([dy, -dx, 0.0]) / np.linalg.norm(vec)
                lbl = Text("0", font_size=22, color=TEAL_A, weight=BOLD)
                lbl.set_stroke(color=BLACK, width=4, background=True)
                lbl.move_to(edge.get_center() + perp * 0.26)
                lbl.set_z_index(4)
                tree["left_bit_label"] = lbl
                edge_labels.add(lbl)
                attach_bit_labels(tree["left"])

            if tree["right"] is not None:
                edge = tree["right_edge"]
                vec = edge.get_end() - edge.get_start()
                dx, dy = vec[0], vec[1]
                perp = np.array([-dy, dx, 0.0]) / np.linalg.norm(vec)
                lbl = Text("1", font_size=22, color=YELLOW_B, weight=BOLD)
                lbl.set_stroke(color=BLACK, width=4, background=True)
                lbl.move_to(edge.get_center() + perp * 0.26)
                lbl.set_z_index(4)
                tree["right_bit_label"] = lbl
                edge_labels.add(lbl)
                attach_bit_labels(tree["right"])

        attach_bit_labels(root_tree)

        self.play(
            LaggedStart(*[FadeIn(lbl, scale=1.2) for lbl in edge_labels], lag_ratio=0.08),
            run_time=1.3,
        )
        self.wait(0.6)

        # Panel z kodami binarnymi po prawej stronie
        panel_x = 4.9
        title = Text("Kody Huffmana", font_size=30, color=BLUE_B, weight=BOLD)
        title.move_to(np.array([panel_x, 2.65, 0.0]))
        underline = Line(
            np.array([panel_x - 1.5, 2.35, 0.0]),
            np.array([panel_x + 1.5, 2.35, 0.0]),
            color=BLUE_B,
            stroke_width=2,
        )

        self.play(Write(title), Create(underline), run_time=1.0)

        def find_path(tree, target_sym):
            if tree["left"] is None and tree["right"] is None:
                return [] if tree["symbols"] == [target_sym] else None
            if tree["left"] is not None:
                sub = find_path(tree["left"], target_sym)
                if sub is not None:
                    return [("0", tree["left_edge"], tree["left_bit_label"], tree["left"])] + sub
            if tree["right"] is not None:
                sub = find_path(tree["right"], target_sym)
                if sub is not None:
                    return [("1", tree["right_edge"], tree["right_bit_label"], tree["right"])] + sub
            return None

        row_ys = [1.65, 0.80, -0.05, -0.90]
        symbols_to_trace = ["↑", "↓", "←", "→"]

        for row_idx, sym in enumerate(symbols_to_trace):
            y = row_ys[row_idx]
            sym_lbl = Text(sym, font_size=32, color=GOLD, weight=BOLD)
            sym_lbl.move_to(np.array([panel_x - 1.05, y, 0.0]))
            colon_lbl = Text(":", font_size=30, color=WHITE, weight=BOLD)
            colon_lbl.move_to(np.array([panel_x - 0.55, y, 0.0]))

            self.play(
                FadeIn(sym_lbl, scale=0.8, rate_func=smooth),
                FadeIn(colon_lbl, rate_func=smooth),
                root_tree["circle"].animate.set_stroke(GOLD, width=4.5),
                run_time=1.2,
            )

            path = find_path(root_tree, sym)
            highlighted_edges = []
            highlighted_circles = [root_tree["circle"]]
            bit_mobs = []

            for step_i, (bit_char, edge, bit_lbl, child_tree) in enumerate(path):
                bit_color = TEAL_A if bit_char == "0" else YELLOW_B
                code_bit = Text(bit_char, font_size=32, color=bit_color, weight=BOLD)
                code_bit.move_to(np.array([panel_x - 0.1 + step_i * 0.34, y, 0.0]))
                bit_mobs.append(code_bit)

                highlighted_edges.append(edge)
                highlighted_circles.append(child_tree["circle"])

                self.play(
                    edge.animate.set_color(GOLD).set_stroke(width=5.5),
                    Indicate(bit_lbl, color=GOLD, scale_factor=1.35),
                    child_tree["circle"].animate.set_stroke(GOLD, width=4.5),
                    FadeIn(code_bit, shift=LEFT * 0.15),
                    run_time=0.75,
                )

            leaf_circle = highlighted_circles[-1]
            self.play(Indicate(leaf_circle, color=GOLD, scale_factor=1.12), run_time=0.5)

            self.play(
                sym_lbl.animate.set_color(WHITE),
                *[e.animate.set_color(EDGE_COLOR).set_stroke(width=2.5) for e in highlighted_edges],
                *[c.animate.set_stroke(BORDER_BLUE, width=3.0) for c in highlighted_circles],
                run_time=0.45,
            )

        self.wait(3)