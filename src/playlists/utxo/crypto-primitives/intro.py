from manim import *
import numpy as np
from helper_coordinates import PEOPLE, centerLabel, Character, CoordinateHelper

# random Generator as a global variable
rng = np.random.default_rng(seed=48)

# >>> 00 - Title >>>
class Title(Scene):
    def construct(self):
        # >>> Ingredient 1: Hashes & Signatures
        sticker_one = ImageMobject("png/excalidraw/sticker_one.png").shift(UP * 0.25 + LEFT * 3)
        sticker_hash = ImageMobject("png/excalidraw/sticker-hash.png").shift(UP * 0.5)
        sticker_signature = ImageMobject("png/excalidraw/sticker_signature.png").shift(RIGHT * 3 + UP * 0.5)

        txt = Text("Hashes and Signatures", color=XTXT, font="Excalifont", font_size=48).shift(DOWN * 2)

        self.play(FadeIn(sticker_one))
        # self.wait()
        self.play(FadeIn(sticker_hash))
        # self.wait()
        self.play(FadeIn(sticker_signature))
        # self.wait()
        self.play(Write(txt))
        self.wait(3)
# <<< 00 - Title <<<

# >>> 01 - Need for hashes >>>
# class NeedForHashes(Scene):
class NeedForHashes(MovingCameraScene):
    def construct(self):
        world = SVGMobject("../../../../assets/svg/excalidraw/world.svg").scale(2.5)
        world_network = SVGMobject("../../../../assets/svg/excalidraw/world-network.svg").scale(2.5)
        person = []
        
        vec_world_xy = [
            ORIGIN + LEFT * 0.3, # Alice 
            UL * 1.3, # Bob
            UR * 1.25, # Charlie
            DOWN * 2.25 + LEFT * 0.1, # Sybil
            RIGHT * 1.3, # Eve
            DR * 1.15 + RIGHT * 0.1, # Mallory
            DL * 1.05 + LEFT * 0.2, # Trent
            RIGHT * 2.5 + UP * 0.15, # Peggy
            UP * 2.55, # Victor
            LEFT * 2.45 + UP * 0.15, # Grace
        ]

        # >>> 1st Section >>>
        for i, ppl in enumerate(PEOPLE):
            person.append(Character(ppl, show_name=False).shift(vec_world_xy[i]).scale(0.35))

        self.play(FadeIn(world))
        self.wait()
        # self.play(world.animate.scale(2.5))
        self.play(world.animate.set_opacity(0.25))
        self.play(FadeIn(world_network))
        self.wait()

        for i, _ in enumerate(PEOPLE):
            self.play(FadeIn(person[i]), run_time=0.2)
        self.wait(3)
        # <<< 1st Section <<<

        # >>> 2nd Section >>>
        self.next_section("Show world and ledger")
        # Group world & people 
        world_group = Group(world, world_network, *person)
        ledger_box = Rectangle(width=7.0, height=6.0, color=XTXT).to_edge(RIGHT)
        ledger_title = Text("Ledger", font="Excalifont", font_size=46).next_to(ledger_box, UP)
        ledger = VGroup(ledger_box, ledger_title).shift(DOWN * 0.3)

        ax_x_range = 6
        ax_y_range = 6
        nm = (ax_x_range - 1) * (ax_y_range - 1)
        axes = Axes(
                    x_range=[0, ax_x_range, 1],
                    y_range=[0, ax_y_range, 1],
                    x_length=ledger_box.width,
                    y_length=ledger_box.height,
        ).move_to(ledger_box.get_center())
        # self.add(axes)
        
        # Animate grouped world
        self.play(
            world_group.animate.scale(1).to_edge(LEFT, buff=0.5),
            FadeIn(ledger),
            run_time = 2,
        )
        self.wait()
        
        # Gossiping
        folder_back = SVGMobject("../../../../assets/svg/notoEmoji/File-Folder-back-only.svg")
        folder_front = SVGMobject("../../../../assets/svg/notoEmoji/File-Folder-cover-only.svg")
        msg_file = SVGMobject("../../../../assets/svg/excalidraw/msg-for-signature.svg").move_to(folder_front.get_center() + UP * 0.6 + LEFT * 0.1).rotate(10 * PI / 180).scale(0.85)
        msg = Group(folder_back, msg_file, folder_front).scale(0.2)

        folder_back.set_z_index(1)
        msg_file.set_z_index(2)
        folder_front.set_z_index(50)
        self.remove(folder_back, folder_front, msg)

        # Participants for Gossiping
        ith_person_msg = []
        ith_person_msg_in_ledger = []

        # weights for randomized folder placement in ledger array
        def expWeights(size=10):
            exp_sample = rng.exponential(1.0, size=1000)
            counts, _ = np.histogram(exp_sample, bins=size*2, density=False)
            counts_truncate = counts[:size]
            counts_truncate_norm = counts_truncate / np.sum(counts_truncate)
            return counts_truncate_norm        

        exp_ = expWeights(size=nm)
        coordinates_rand_ix = rng.choice(range(nm), size=nm, replace=False, p=exp_)
        coordinates_ordered = [(i, j) for j in range(ax_y_range - 1, 0, -1) for i in range(1, ax_x_range)] # x_range goes from left to right, y_range from top to bottom
        coordinates_rand = [coordinates_ordered[i] for i in coordinates_rand_ix]
        k = 0
        for i, pi in enumerate(person[pi] for pi in rng.choice(range(10), replace=False, size=5)):
            n_targets = rng.choice([1,2,3,4])
            ith_person_msg.append([msg.copy().scale(0.75) for _ in range(n_targets)])
            ith_person_msg_in_ledger.append([msg.copy() for _ in range(n_targets)])
            targets_ix = rng.choice([k for k in range(len(person)) if k != i], size=n_targets)
            targets = [person[k] for k in targets_ix]
            # ax_ixs = 110G
            for j in range(len(targets)):
                arr = CurvedArrow(
                    start_point = person[i].get_center(),
                    end_point = targets[j].get_center() + DOWN * 0.3,
                    angle=-PI/3,
                    color=PURE_GREEN,
                    tip_length=0.2
                )
                self.play(
                    FadeIn(arr),
                    FadeIn(ith_person_msg[i][j].shift(person[i].get_center())),
                    MoveAlongPath(ith_person_msg[i][j], arr),
                    run_time=2,
                )
                self.add(ith_person_msg_in_ledger[i][j].move_to(axes.c2p(coordinates_rand[k][0], coordinates_rand[k][1])))
                k += 1


        # Zoom in and show a hash
        msg_file_hashed = SVGMobject("../../../../assets/svg/excalidraw/msg-for-signature-encrypted.svg").move_to(folder_front.get_center() + UP * 0.6 + LEFT * 0.1).rotate(10 * PI / 180)
        size_msg_file_ = (ith_person_msg_in_ledger[0][0][1].width, ith_person_msg_in_ledger[0][0][1].height)
        msg_file_hashed.scale_to_fit_width(size_msg_file_[0])

        msg_file_hashed_svg_ = SVGMobject("../../../../assets/svg/excalidraw/label.svg")
        msg_file_hashed_txt_ = MathTex(r"44.\hfil .\hfill . a7", color=BLACK, font_size=38).move_to(centerLabel(msg_file_hashed_svg_)).rotate(angle=-PI/4)
        msg_file_hashed_lbl = Group(msg_file_hashed_svg_, msg_file_hashed_txt_).scale(0.25)
        # msg_file_hashed_lbl = Group(msg_file_hashed, msg_file_hashed_lbl_)

        hash_sticker = SVGMobject("../../../../assets/svg/excalidraw/sticker-hash.svg").scale(0.6)
    
        msg_file_hashed.set_z_index(4)
        msg_file_hashed_lbl.set_z_index(100)
        hash_sticker.set_z_index(150)
        self.remove(hash_sticker, msg_file_hashed, msg_file_hashed_lbl)

        self.camera.frame.save_state()
        self.play(
            self.camera.frame.animate.move_to(ith_person_msg_in_ledger[0][0]).set(width=ith_person_msg_in_ledger[0][0].width*5),
        )
        self.wait(3)
        self.play(
            ith_person_msg_in_ledger[0][0][1].animate.shift(UP * 0.3),
            FadeIn(hash_sticker.set_opacity(0.25).move_to(ith_person_msg_in_ledger[0][0].get_center())),
            run_time=2
        )
        self.wait()
        self.play(
            Transform(
                ith_person_msg_in_ledger[0][0][1], 
                msg_file_hashed.move_to(ith_person_msg_in_ledger[0][0][1].get_center()),
            ),
            FadeIn(msg_file_hashed_lbl.move_to(ith_person_msg_in_ledger[0][0].get_center() + RIGHT * 0.1 + DOWN * 0.1)),
            msg_file_hashed.animate.shift(DOWN * 0.3),
            ith_person_msg_in_ledger[0][0][1].animate.shift(DOWN * 0.3),
            run_time=3
        )
        self.wait(2)
        self.play(
            FadeOut(hash_sticker),
            Restore(self.camera.frame)
        )
        self.wait(5)
        
        # Add hashes and labels in the array and reorder
        ith_person_msg_in_ledger_lbl = [[msg_file_hashed_lbl]] 
        for i in range(len(ith_person_msg_in_ledger)):
            # skip first obj because its done in zoomed in scene
            if i > 0:
                ith_person_msg_in_ledger_lbl.append([])
            for j in range(len(ith_person_msg_in_ledger[i])):
                # skip first obj because its done in zoomed in scene
                if i == 0 and j == 0:
                    pass

                ith_person_msg_in_ledger_lbl[i].append(msg_file_hashed_lbl.copy())
                self.play(
                    FadeIn(ith_person_msg_in_ledger_lbl[i][j].move_to(ith_person_msg_in_ledger[i][j].get_center() + RIGHT * 0.1 + DOWN * 0.1)),
                )
                # hash, transform and reorder

        

        # Place dots at grid coordinates (i, j)
        # for i in range(1, ax_x_range):
        #     for j in range(1, ax_y_range):
        #         folder_i = msg.copy().move_to(axes.c2p(i, j))
        #         self.add(folder_i)

        # <<< 2nd Section <<<


# <<< 01 - Need for hashes <<<

class Folder(Scene):
    def construct(self):
        DEBUG_MODE = False

        folder_back = SVGMobject("../../../../assets/svg/notoEmoji/File-Folder-back-only.svg")
        folder_front = SVGMobject("../../../../assets/svg/notoEmoji/File-Folder-cover-only.svg")
        msg = SVGMobject("../../../../assets/svg/excalidraw/msg-for-signature.svg").shift(UP * 2 + LEFT * 2)
        msg_hashed = SVGMobject("../../../../assets/svg/excalidraw/msg-for-signature-encrypted.svg").shift(DOWN + LEFT * 2)
        code = SVGMobject("../../../../assets/svg/excalidraw/Code-Editor.svg").shift(UP * 2)
        code_hashed = SVGMobject("../../../../assets/svg/excalidraw/Code-Editor-encrypted.svg").shift(DOWN)
        nft = SVGMobject("../../../../assets/svg/excalidraw/bored-ape.svg").shift(UP * 2 + RIGHT * 2)
        nft_hashed = SVGMobject("../../../../assets/svg/excalidraw/bored-ape-encrypted.svg").shift(DOWN + RIGHT * 2)
        # crypto_coin = SVGMobject("../../../../assets/svg/excalidraw/bitcoin-coins.svg").shift(UP * 2 + LEFT * 4)
        nft_lbl_svg = SVGMobject("../../../../assets/svg/excalidraw/label.svg") 
        nft_lbl_txt = MathTex(r"15.\hfil .\hfill . e9", color=BLACK, font_size=38).move_to(centerLabel(nft_lbl_svg)).rotate(angle=-PI/4)
        nft_lbl = Group(nft_lbl_svg, nft_lbl_txt).scale(0.5).align_to(nft, nft.get_corner(UR))
        nft_w_lbl = Group(nft, nft_lbl)

        hash_lbl = SVGMobject("../../../../assets/svg/excalidraw/sticker-hash.svg").set_opacity(0.5)

        folder_back.set_z_index(1)
        nft.set_z_index(2)
        nft_hashed.set_z_index(3)
        code.set_z_index(4)
        code_hashed.set_z_index(5)
        msg.set_z_index(6)
        msg_hashed.set_z_index(7)
        # crypto_coin.set_z_index(8)
        nft_lbl.set_z_index(9)
        folder_front.set_z_index(10)
        hash_lbl.set_z_index(11)

        self.remove(
            folder_back,
            folder_front,
            msg,
            msg_hashed,
            code,
            code_hashed,
            nft,
            nft_hashed,
            # crypto_coin,
            nft_lbl
        )

        # Animate stuff
        self.add(folder_back, folder_front)
        self.play(
            FadeIn(msg),
            FadeIn(code),
            FadeIn(nft),
            # FadeIn(crypto_coin),
            FadeIn(nft_lbl),
            # FadeIn(msg_hashed),
            # FadeIn(code_hashed),
            # FadeIn(nft_hashed),
            run_time=3
        )
        self.wait()
        self.play(
            code.animate.move_to(folder_front.get_center() + UP * 0.3 + LEFT * 0.1).rotate(10 * PI / 180).scale(0.75),
            nft_w_lbl.animate.move_to(folder_front.get_center() + UP * 0.3 + RIGHT * 0.1).rotate(10 * PI / 180).scale(0.75),
            msg.animate.move_to(folder_front.get_center() + UP * 0.3 + LEFT * 0.3).rotate(10 * PI / 180).scale(0.75)
        )
        self.wait()
        self.play(
            FadeIn(hash_lbl),
            # FadeOut(hash_lbl),
            Transform(msg, msg_hashed)
        )
        self.wait()

        # >>> Debug Mode >>>
        dbg_objects = [
            # folder_back,
            # folder_front,
            # msg, 
            # msg_hashed, 
            # code, 
            # code_hashed, 
            nft, 
            # nft_hashed,
            nft_lbl,
            # hash_lbl
        ]
        cycle_colors = [XNEON_RED, XNEON_BLUE, XNEON_GREEN, XNEON_PURPLE]

        for di, dObj in enumerate(dbg_objects):
            # Debug coordinates if in debug mode
            if DEBUG_MODE:
                helper = CoordinateHelper.show_coordinates(
                    dObj, 
                    self, 
                    show_points=False,
                    label_scale=0.2,
                    color=cycle_colors[di]
                    
                )
                # Wait to observe the coordinates
                self.wait(0.5)
                # Remove helper after viewing (optional)
                # self.remove(helper)
        # <<< Debug Mode <<<

class GossipMessage(Scene):
    def construct(self):
        folder_back = SVGMobject("../../../../assets/svg/notoEmoji/File-Folder-back-only.svg")
        folder_front = SVGMobject("../../../../assets/svg/notoEmoji/File-Folder-cover-only.svg")
        msg = SVGMobject("../../../../assets/svg/excalidraw/msg-for-signature.svg").shift(UP * 2)

        folder_back.set_z_index(1)
        msg.set_z_index(2)
        folder_front.set_z_index(3)

        self.remove(folder_back, folder_front, msg)

        self.play(
            FadeIn(folder_back, folder_front),
            FadeIn(msg)
        )
        self.wait(2)
        self.play(
            msg.animate.rotate(10 * PI / 180).scale(0.75).move_to(folder_front.get_center(), UP * 0.2)
        )


# >>> 02 - Need for signatures >>>
class NeedForSignatures(Scene):
    def construct(self):
        alice = Character(name="Alice", show_name=True).shift(UL * 2 + LEFT * 2)
        bob = Character(name="Bob", show_name=True).shift(UR * 2 + RIGHT * 2)
        mallory = Character(name="Mallory", show_name=True, expr="Smiling-Face-With-Horns").shift(DOWN * 2) # .shift(UP * 0.8)
        msg = SVGMobject("../../../../assets/svg/excalidraw/msg-for-signature").next_to(alice, RIGHT).scale(0.75)

        self.add(alice, bob)
        self.wait(2)
        self.play(
            FadeIn(msg),
            msg.animate.next_to(bob, LEFT),
        )
        self.wait()
        self.add(mallory)
        self.wait()

# <<< 02 - Need for signatures <<<


# >>> Array of folders in Ledger >>>
class ArrayFolders(Scene):
    def construct(self):
        folder_back = SVGMobject("../../../../assets/svg/notoEmoji/File-Folder-back-only.svg")
        folder_front = SVGMobject("../../../../assets/svg/notoEmoji/File-Folder-cover-only.svg")
        msg_file = SVGMobject("../../../../assets/svg/excalidraw/msg-for-signature.svg").move_to(folder_front.get_center() + UP * 0.6 + LEFT * 0.1).rotate(10 * PI / 180).scale(0.85)
        msg = Group(folder_back, folder_front, msg_file).scale(0.2)

        folder_back.set_z_index(1)
        msg_file.set_z_index(2)
        folder_front.set_z_index(3)
        self.remove(folder_back, folder_front, msg)

        box = Rectangle(height=7.0, width=10.0, color=LOGO_BLUE).move_to(RIGHT * 2)
        ax_x_range = 11
        ax_y_range = 4
        axes = Axes(
                    x_range=[0, ax_x_range, 1],
                    y_range=[0, ax_y_range, 1],
                    x_length=box.width,
                    y_length=box.height,
                    # x_length=4,
                    # y_length=3,
        ).move_to(box.get_center())
        self.add(box)
        # self.add(axes)

        # Place dots at grid coordinates (i, j)
        for i in range(1, ax_x_range):
            for j in range(1, ax_y_range):
                folder_i = msg.copy().move_to(axes.c2p(i, j))
                self.add(folder_i)
# <<< Array of folders in Ledger <<<
