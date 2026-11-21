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
        FILL_BLUE = "#41377D"
        BORDER_BLUE = "#E3E3E3"
        EDGE_COLOR = "#FFFFFF"

        # Tworzy niebieski węzeł o stałym promieniu:
        # - w środku wyłącznie symbole (automatycznie ułożone i przeskalowane)
        # - pod kołem opcjonalna liczba wystąpień
        def create_node(symbols, freq=None, pos=ORIGIN, radius=NODE_RADIUS):
            circle = Circle(
                radius=radius,
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

            max_inner = radius * 1.25
            if sym_group.width > max_inner:
                sym_group.scale(max_inner / sym_group.width)
            if sym_group.height > max_inner:
                sym_group.scale(max_inner / sym_group.height)

            sym_group.move_to(circle.get_center())
            sym_group.set_z_index(3)

            if freq is not None:
                freq_text = Text(str(freq), font_size=23, color=BLUE_A, weight=BOLD)
                freq_text.set_stroke(color=BLACK, width=4, background=True)
                freq_text.next_to(circle, DOWN, buff=0.08)
                freq_text.set_z_index(3)
                node_group = VGroup(circle, sym_group, freq_text)
            else:
                freq_text = None
                node_group = VGroup(circle, sym_group)

            return node_group, circle, sym_group, sym_list, freq_text

        # Tworzy skośną krawędź łączącą dokładnie brzegi dwóch okręgów
        def create_edge(parent_circle, child_circle, radius=NODE_RADIUS):
            p1 = parent_circle.get_center()
            p2 = child_circle.get_center()
            vec = p2 - p1
            unit = vec / np.linalg.norm(vec)
            start = p1 + unit * radius
            end = p2 - unit * radius
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
        # ETAP 0A – Niebieskie koło, impulsy kierunkowe i kody 2-bitowe
        # ==========================================
        center_circle = Circle(
            radius=0.52,
            fill_color=FILL_BLUE,
            fill_opacity=1.0,
            stroke_color=BORDER_BLUE,
            stroke_width=3.0,
        )
        center_circle.move_to(ORIGIN)
        center_circle.set_z_index(2)

        self.play(GrowFromCenter(center_circle), run_time=0.9)
        self.wait(0.4)

        # 1. Impuls w górę -> strzałka ↑ nad kołem
        up_arrow = Text("↑", font_size=42, color=WHITE, weight=BOLD)
        up_arrow.next_to(center_circle, UP, buff=0.45)
        self.play(
            center_circle.animate(rate_func=there_and_back).shift(UP * 0.32),
            run_time=0.65,
        )
        self.play(FadeIn(up_arrow, scale=0.8, rate_func=smooth), run_time=0.9)

        # 2. Impuls w lewo -> strzałka ← po lewej stronie koła
        left_arrow = Text("←", font_size=42, color=WHITE, weight=BOLD)
        left_arrow.next_to(center_circle, LEFT, buff=0.55)
        self.play(
            center_circle.animate(rate_func=there_and_back).shift(LEFT * 0.32),
            run_time=0.65,
        )
        self.play(FadeIn(left_arrow, scale=0.8, rate_func=smooth), run_time=0.9)

        # 3. Impuls w prawo -> strzałka → po prawej stronie koła
        right_arrow = Text("→", font_size=42, color=WHITE, weight=BOLD)
        right_arrow.next_to(center_circle, RIGHT, buff=0.55)
        self.play(
            center_circle.animate(rate_func=there_and_back).shift(RIGHT * 0.32),
            run_time=0.65,
        )
        self.play(FadeIn(right_arrow, scale=0.8, rate_func=smooth), run_time=0.9)

        # 4. Impuls w dół -> strzałka ↓ pod kołem
        down_arrow = Text("↓", font_size=42, color=WHITE, weight=BOLD)
        down_arrow.next_to(center_circle, DOWN, buff=0.45)
        self.play(
            center_circle.animate(rate_func=there_and_back).shift(DOWN * 0.32),
            run_time=0.65,
        )
        self.play(FadeIn(down_arrow, scale=0.8, rate_func=smooth), run_time=0.9)
        self.wait(0.4)

        # Pojawienie się kodów binarnych obok strzałek:
        # 00 dla ↑, 01 dla ↓, 10 dla ←, 11 dla →
        code_up = Text("00", font_size=30, color=TEAL_A, weight=BOLD)
        code_up.next_to(up_arrow, RIGHT, buff=0.25)

        code_down = Text("01", font_size=30, color=TEAL_A, weight=BOLD)
        code_down.next_to(down_arrow, RIGHT, buff=0.25)

        code_left = Text("10", font_size=30, color=YELLOW_B, weight=BOLD)
        code_left.next_to(left_arrow, LEFT, buff=0.25)

        code_right = Text("11", font_size=30, color=YELLOW_B, weight=BOLD)
        code_right.next_to(right_arrow, RIGHT, buff=0.25)

        for code_mob in [code_up, code_down, code_left, code_right]:
            self.play(FadeIn(code_mob, scale=0.85, rate_func=smooth), run_time=0.7)

        self.wait(0.8)

        # ==========================================
        # ETAP 0B – Płynne przejście (bez fade in/out) do wykresu słupkowego
        # Kolejność słupków: → (2), ← (2), ↓ (3), ↑ (5)
        # ==========================================
        BASE_Y = -1.65
        UNIT_H = 0.66
        BAR_W = 1.15
        bar_xs = [-3.15, -1.05, 1.05, 3.15]
        bar_values = [2, 2, 3, 5]

        x_axis = Line(
            np.array([-4.45, BASE_Y, 0.0]),
            np.array([4.45, BASE_Y, 0.0]),
            color=BLUE_B,
            stroke_width=2.5,
        )
        y_axis = Line(
            np.array([-4.45, BASE_Y, 0.0]),
            np.array([-4.45, BASE_Y + 5.45 * UNIT_H, 0.0]),
            color=BLUE_B,
            stroke_width=2.5,
        )

        grid_and_ticks = VGroup()
        for level in range(1, 6):
            y_lvl = BASE_Y + level * UNIT_H
            tick = Line(
                np.array([-4.55, y_lvl, 0.0]),
                np.array([-4.35, y_lvl, 0.0]),
                color=BLUE_B,
                stroke_width=2.0,
            )
            grid = Line(
                np.array([-4.35, y_lvl, 0.0]),
                np.array([4.35, y_lvl, 0.0]),
                color=FILL_BLUE,
                stroke_width=1.2,
            )
            grid.set_z_index(-1)
            lvl_lbl = Text(str(level), font_size=20, color=BLUE_A)
            lvl_lbl.next_to(tick, LEFT, buff=0.14)
            grid_and_ticks.add(tick, grid, lvl_lbl)

        axes_group = VGroup(x_axis, y_axis, grid_and_ticks)

        bars = VGroup()
        val_labels = VGroup()
        bar_arrow_targets = []

        for x_pos, val in zip(bar_xs, bar_values):
            bar_h = val * UNIT_H
            bar = Rectangle(
                width=BAR_W,
                height=bar_h,
                fill_color=FILL_BLUE,
                fill_opacity=1.0,
                stroke_color=BORDER_BLUE,
                stroke_width=3.0,
            )
            bar.move_to(np.array([x_pos, BASE_Y + bar_h / 2.0, 0.0]))
            bar.set_z_index(2)

            val_txt = Text(str(round(val*100/12,1))+"%", font_size=28, color=BLUE_A, weight=BOLD)
            val_txt.next_to(bar, UP, buff=0.18)

            bars.add(bar)
            val_labels.add(val_txt)
            bar_arrow_targets.append(bar.get_bottom() + DOWN * 0.42)

        # Morfujemy koło i kody w osie oraz słupki, a strzałki przesuwamy pod oś X
        self.play(
            ReplacementTransform(center_circle, axes_group),
            ReplacementTransform(code_right, VGroup(bars[0], val_labels[0])),
            ReplacementTransform(code_left, VGroup(bars[1], val_labels[1])),
            ReplacementTransform(code_down, VGroup(bars[2], val_labels[2])),
            ReplacementTransform(code_up, VGroup(bars[3], val_labels[3])),
            right_arrow.animate(path_arc=-0.35).move_to(bar_arrow_targets[0]),
            left_arrow.animate(path_arc=0.35).move_to(bar_arrow_targets[1]),
            down_arrow.animate(path_arc=0.25).move_to(bar_arrow_targets[2]),
            up_arrow.animate(path_arc=-0.35).move_to(bar_arrow_targets[3]),
            run_time=2.0,
        )
        self.wait(1.2)

        # ==========================================
        # ETAP 1 – Bezpośrednie przejście z wykresu do posortowanych węzłów
        # Kolejność posortowana rosnąco: ← (2), → (2), ↓ (3), ↑ (5)
        # ==========================================
        sorted_items = [
            ("←", 2, bars[1], val_labels[1], left_arrow),
            ("→", 2, bars[0], val_labels[0], right_arrow),
            ("↓", 3, bars[2], val_labels[2], down_arrow),
            ("↑", 5, bars[3], val_labels[3], up_arrow),
        ]

        node_x_positions = [-4.2, -1.4, 1.4, 4.2]
        TOP_Y = 2.4

        forest = []
        chart_to_nodes_anims = [FadeOut(axes_group, scale=0.95)]

        for i, (sym, freq, bar_mob, val_mob, arrow_mob) in enumerate(sorted_items):
            pos = np.array([node_x_positions[i], TOP_Y, 0.0])
            node_group, circle, sym_group, _, freq_text = create_node(
                [sym], freq, pos=pos
            )

            chart_to_nodes_anims.append(ReplacementTransform(bar_mob, circle))
            chart_to_nodes_anims.append(ReplacementTransform(arrow_mob, sym_group))
            chart_to_nodes_anims.append(ReplacementTransform(val_mob, freq_text))

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

        self.play(*chart_to_nodes_anims, run_time=1.8)
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

        kody_panel = VGroup(title, underline)
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

            kody_panel.add(sym_lbl, colon_lbl, *bit_mobs)

            leaf_circle = highlighted_circles[-1]
            self.play(Indicate(leaf_circle, color=GOLD, scale_factor=1.12), run_time=0.5)

            self.play(
                sym_lbl.animate.set_color(WHITE),
                *[e.animate.set_color(EDGE_COLOR).set_stroke(width=2.5) for e in highlighted_edges],
                *[c.animate.set_stroke(BORDER_BLUE, width=3.0) for c in highlighted_circles],
                run_time=0.45,
            )

        self.wait(1.2)

        # ==========================================
        # ETAP 7 – Porównanie: Zwykłe drzewo binarne (lewo) vs Drzewo Huffmana (prawo)
        # ==========================================
        LEFT_X = -3.55
        RIGHT_X = 3.55
        TITLE_Y = 3.25
        CMP_SCALE = 0.78
        CMP_RADIUS = NODE_RADIUS * CMP_SCALE

        huffman_full_group = VGroup(*collect_subtree_mobjects(root_tree), *edge_labels)

        huffman_title = Text("Drzewo Huffmana", font_size=30, color=BLUE_B, weight=BOLD)
        huffman_title.move_to(np.array([RIGHT_X, TITLE_Y, 0.0]))

        # Wygaszamy panel "Kody Huffmana", przesuwamy drzewo Huffmana na prawo
        # i wyświetlamy nad nim tytuł "Drzewo Huffmana"
        self.play(
            FadeOut(kody_panel, shift=RIGHT * 0.3),
            huffman_full_group.animate.scale(CMP_SCALE).move_to(
                np.array([RIGHT_X, 0.15, 0.0])
            ),
            Write(huffman_title),
            run_time=1.6,
        )
        self.wait(0.5)

        # Budowa zwykłego drzewa binarnego dla kodów stałej długości:
        # ↑ = 00, ↓ = 01, ← = 10, → = 11
        std_title = Text("Zwykłe drzewo binarne", font_size=30, color=BLUE_B, weight=BOLD)
        std_title.move_to(np.array([LEFT_X, TITLE_Y, 0.0]))

        std_root_node, std_root_c, std_root_syms, _, _ = create_node(
            ["↑", "↓", "←", "→"], freq=None, pos=np.array([LEFT_X, 2.05, 0.0]), radius=CMP_RADIUS
        )
        std_n0_node, std_n0_c, std_n0_syms, _, _ = create_node(
            ["↑", "↓"], freq=None, pos=np.array([LEFT_X - 1.40, 0.45, 0.0]), radius=CMP_RADIUS
        )
        std_n1_node, std_n1_c, std_n1_syms, _, _ = create_node(
            ["←", "→"], freq=None, pos=np.array([LEFT_X + 1.40, 0.45, 0.0]), radius=CMP_RADIUS
        )

        std_leaf_00, std_c_00, std_s_00, _, _ = create_node(
            ["↑"], freq=None, pos=np.array([LEFT_X - 2.10, -1.15, 0.0]), radius=CMP_RADIUS
        )
        std_leaf_01, std_c_01, std_s_01, _, _ = create_node(
            ["↓"], freq=None, pos=np.array([LEFT_X - 0.70, -1.15, 0.0]), radius=CMP_RADIUS
        )
        std_leaf_10, std_c_10, std_s_10, _, _ = create_node(
            ["←"], freq=None, pos=np.array([LEFT_X + 0.70, -1.15, 0.0]), radius=CMP_RADIUS
        )
        std_leaf_11, std_c_11, std_s_11, _, _ = create_node(
            ["→"], freq=None, pos=np.array([LEFT_X + 2.10, -1.15, 0.0]), radius=CMP_RADIUS
        )

        def make_std_edge_with_bit(parent_c, child_c, bit_char, is_left):
            edge = create_edge(parent_c, child_c, radius=CMP_RADIUS)
            vec = edge.get_end() - edge.get_start()
            dx, dy = vec[0], vec[1]
            perp = (
                       np.array([dy, -dx, 0.0]) if is_left else np.array([-dy, dx, 0.0])
                   ) / np.linalg.norm(vec)
            bit_color = TEAL_A if bit_char == "0" else YELLOW_B
            lbl = Text(bit_char, font_size=18, color=bit_color, weight=BOLD)
            lbl.set_stroke(color=BLACK, width=4, background=True)
            lbl.move_to(edge.get_center() + perp * 0.22)
            lbl.set_z_index(4)
            return edge, lbl

        e_0, b_0 = make_std_edge_with_bit(std_root_c, std_n0_c, "0", True)
        e_1, b_1 = make_std_edge_with_bit(std_root_c, std_n1_c, "1", False)
        e_00, b_00 = make_std_edge_with_bit(std_n0_c, std_c_00, "0", True)
        e_01, b_01 = make_std_edge_with_bit(std_n0_c, std_c_01, "1", False)
        e_10, b_10 = make_std_edge_with_bit(std_n1_c, std_c_10, "0", True)
        e_11, b_11 = make_std_edge_with_bit(std_n1_c, std_c_11, "1", False)

        # Wyświetlenie tytułu i korzenia zwykłego drzewa binarnego
        self.play(
            Write(std_title),
            GrowFromCenter(std_root_c),
            FadeIn(std_root_syms, scale=0.85),
            run_time=1.1,
        )

        # Poziom 1 zwykłego drzewa binarnego (0 oraz 1)
        self.play(
            Create(e_0),
            Create(e_1),
            FadeIn(b_0, scale=1.2),
            FadeIn(b_1, scale=1.2),
            GrowFromCenter(std_n0_c),
            GrowFromCenter(std_n1_c),
            FadeIn(std_n0_syms, scale=0.85),
            FadeIn(std_n1_syms, scale=0.85),
            run_time=1.2,
        )

        # Poziom 2 (liście: ↑=00, ↓=01, ←=10, →=11)
        self.play(
            Create(e_00),
            Create(e_01),
            Create(e_10),
            Create(e_11),
            FadeIn(b_00, scale=1.2),
            FadeIn(b_01, scale=1.2),
            FadeIn(b_10, scale=1.2),
            FadeIn(b_11, scale=1.2),
            GrowFromCenter(std_c_00),
            GrowFromCenter(std_c_01),
            GrowFromCenter(std_c_10),
            GrowFromCenter(std_c_11),
            FadeIn(std_s_00, scale=0.85),
            FadeIn(std_s_01, scale=0.85),
            FadeIn(std_s_10, scale=0.85),
            FadeIn(std_s_11, scale=0.85),
            run_time=1.3,
        )
        self.wait(1.0)

        # ==========================================
        # ETAP 8 – Średnia długość wiadomości pod oboma drzewami
        # ==========================================
        AVG_Y = -3.10

        avg_left = Text(
            "Średnia długość wiadomości = 2",
            font_size=24,
            color=WHITE,
            weight=BOLD,
        )
        if avg_left.width > 6.2:
            avg_left.scale(6.2 / avg_left.width)
        avg_left.move_to(np.array([LEFT_X, AVG_Y, 0.0]))

        avg_right = Text(
            "Średnia długość wiadomości ~ 1.916",
            font_size=24,
            color=GOLD,
            weight=BOLD,
        )
        if avg_right.width > 6.2:
            avg_right.scale(6.2 / avg_right.width)
        avg_right.move_to(np.array([RIGHT_X, AVG_Y, 0.0]))

        self.play(
            FadeIn(avg_left, shift=UP * 0.2, rate_func=smooth),
            FadeIn(avg_right, shift=UP * 0.2, rate_func=smooth),
            run_time=1.3,
        )

        self.wait(3.5)