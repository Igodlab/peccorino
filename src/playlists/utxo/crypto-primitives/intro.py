from manim import *
import numpy as np
from helper_coordinates import PEOPLE, centerLabel, Character, HashLabel
from utils import CoordinateHelper

# random Generator variable
rng = np.random.default_rng(seed=48)

# >>> 00 - Title >>>
class Title(Scene):
    def construct(self):
        # >>> Ingredient 1: Hashes & Signatures
        sticker_one = SVGMobject("../../../../assets/svg/excalidraw/sticker_one.svg").shift(UP * 0.5 + LEFT * 3)
        sticker_hash = SVGMobject("../../../../assets/svg/excalidraw/sticker-hash.svg").shift(UP * 0.5)
        sticker_signature = SVGMobject("../../../../assets/svg/excalidraw/sticker_signature.svg").shift(RIGHT * 3 + UP * 0.5)

        txt = Text("Hashes and Signatures", color=XTXT, font="Excalifont", font_size=48).shift(DOWN * 2)

        self.play(LaggedStart(
            FadeIn(sticker_one),
            FadeIn(sticker_hash),
            FadeIn(sticker_signature),
            Write(txt),
            lag_ratio=0.5,
            run_time=4,
        ))
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
        self.play(world.animate.set_opacity(0.25))
        self.play(FadeIn(world_network))
        self.wait()

        for i, _ in enumerate(PEOPLE):
            self.play(FadeIn(person[i]), run_time=0.2)
        self.wait()
        # <<< 1st Section <<<

        # >>> 2nd Section >>>
        self.next_section("Show world and ledger")
        # Group world & people 
        world_group = Group(world, world_network, *person)
        ledger_box = Rectangle(width=7.0, height=6.0, color=XTXT).to_edge(RIGHT)
        ledger_title = Text("Ledger", font="Excalifont", font_size=46, color=XTXT).next_to(ledger_box, UP)
        ledger = VGroup(ledger_box, ledger_title).shift(DOWN * 0.3)

        ax_x_range = 6
        ax_y_range = 5
        nm = (ax_x_range - 1) * (ax_y_range - 1) # coordinate index skips points at coordinate axes
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
        msg_file_hashed = SVGMobject("../../../../assets/svg/excalidraw/msg-for-signature-encrypted.svg").move_to(folder_front.get_center() + UP * 0.6 + LEFT * 0.1).rotate(10 * PI / 180)
        size_msg_file_ = (msg_file.width, msg_file.height)
        msg_file_hashed.scale_to_fit_width(size_msg_file_[0])
        # grouped msg: ([0],        [1],        [2]) 
        msg = Group(folder_back, msg_file, folder_front).scale(0.2)


        folder_back.set_z_index(1)
        msg_file.set_z_index(2)
        folder_front.set_z_index(50)
        self.remove(folder_back, folder_front, msg)

        # Participants for Gossiping
        ith_person_msg = []
        ith_msg_ledger = []
        arr = []

        # weights for randomized folder placement in ledger array
        def expWeigths_(size=10):
            exp_sample = rng.exponential(1.0, size=1000)
            counts, _ = np.histogram(exp_sample, bins=size*2, density=False)
            counts_truncate = counts[:size]
            counts_truncate_norm = counts_truncate / np.sum(counts_truncate)
            return counts_truncate_norm        

        exp_ = expWeigths_(size=nm)
        coordinates_rand_ix = rng.choice(range(nm), size=nm, replace=False, p=exp_)
        coordinates_ordered = [(i, j) for j in range(ax_y_range - 1, 0, -1) for i in range(1, ax_x_range)] # x_range goes from left to right, y_range from top to bottom
        coordinates_rand = [coordinates_ordered[i] for i in coordinates_rand_ix]
        k = 0
        for i in range(len([person[pi] for pi in rng.choice(range(10), replace=False, size=5)])):
            n_targets = rng.choice([1,2,3,4])
            ith_person_msg += [msg.copy().scale(0.75) for _ in range(n_targets)]
            ith_msg_ledger += [msg.copy() for _ in range(n_targets)]
            targets_ix = rng.choice([l for l in range(len(person)) if l != i], size=n_targets)
            targets = [person[l] for l in targets_ix]

            for j in range(len(targets)):
                ith_person_msg[k].move_to(person[i].get_center())
                ith_msg_ledger[k].move_to(axes.c2p(*coordinates_rand[k]))
                arr.append(CurvedArrow(
                    start_point = person[i].get_center(),
                    end_point = targets[j].get_center() + DOWN * 0.3,
                    angle=-PI/3,
                    color=PURE_GREEN,
                    tip_length=0.2
                ))
                self.play(
                    FadeIn(arr[k]),
                    FadeIn(ith_person_msg[k]),
                    MoveAlongPath(ith_person_msg[k], arr[k]),
                    run_time=1.25,
                )
                self.add(ith_msg_ledger[k])
                k += 1


        # Add hashes and labels in the array and reorder
        hash_sticker = SVGMobject("../../../../assets/svg/excalidraw/sticker-hash.svg").scale(0.6)

        ith_hash_sticker = [] # blue hash sticker
        ith_msg_file_hashed = [] # encrypted hashed file
        ith_msg_ledger_lbl = [] # label w/ hash
        ith_obj_ledger = [] # full final hashed object
        transform_file_to_hashed = []
        time_lbl = []

        for i in range(len(ith_msg_ledger)):
            ith_msg_file_hashed.append(msg_file_hashed.copy())
            ith_msg_file_hashed[i].scale_to_fit_width(size_msg_file_[0])
            ith_msg_file_hashed[i].scale(0.2) # after setting to width we scaled down by 0.2
            ith_msg_file_hashed[i].move_to(ith_msg_ledger[i][1].get_center())
            ith_msg_file_hashed[i].set_z_index(10 + i)

            ith_msg_ledger_lbl.append(HashLabel(f"obj\\;{i+1}", hash_text=False))
            ith_msg_ledger_lbl[i].move_to(ith_msg_ledger[i].get_center() + RIGHT * 0.1 + DOWN * 0.1)
            ith_msg_ledger_lbl[i].set_z_index(100 + i)

            ith_hash_sticker.append(hash_sticker.copy()) # .set_opacity(0.25))  
            ith_hash_sticker[i].move_to(ith_msg_ledger[i].get_center())
            ith_hash_sticker[i].set_z_index(150 + i)

            transform_file_to_hashed.append(Transform(ith_msg_ledger[i][1], ith_msg_file_hashed[i], replace_mobject_with_target_in_scene=True))

            ith_obj_ledger.append(Group(ith_msg_ledger[i], ith_msg_file_hashed[i], ith_msg_ledger_lbl[i]))

            time_lbl_ = f"time\\;{i+1}"
            time_lbl.append(MathTex(time_lbl_, font_size=18, color=XTXT))


        self.remove(
            *ith_msg_file_hashed,
            *ith_msg_ledger_lbl,
            *ith_hash_sticker,
        )
        
        # print(f"ith_msg_file_hashed={ith_msg_file_hashed}")
        # print(f"ith_hash_sticker={ith_hash_sticker}")
        # print(f"ith_msg_ledger_lbl={ith_msg_ledger_lbl}")
        # print(f"ith_msg_ledger (obj [1])={[mob[1] for mob in ith_msg_ledger]}")

        # Zoom in and show a hash for first msg file
        self.camera.frame.save_state()
        self.play(self.camera.frame.animate.move_to(ith_msg_ledger[0]).set(width=ith_msg_ledger[0].width*5))
        self.wait()
        self.play(LaggedStart(
            ith_hash_sticker[0].animate.set_opacity(0.25),
            ith_msg_ledger[0][1].animate.shift(UP * 0.3),
            lag_ratio=2,
            run_time=4
        ))
        self.remove(world_group, *ith_person_msg, *arr)
        self.wait()
        self.play(
            transform_file_to_hashed[0],
            FadeIn(ith_msg_ledger_lbl[0]),
            run_time=3
        )
        self.wait()
        self.play(
            ith_hash_sticker[0].animate.set_opacity(0.0),
            self.camera.frame.animate.move_to(ledger).set(height=ledger.height*1.1)
        )
        self.wait()

        # Animate the rest of folders - Hash and label-hash them!
        self.play(
            *[mob.animate.set_opacity(0.25) for mob in ith_hash_sticker[1:]],
            run_time=2,
        )
        self.wait()
        self.play(
            *transform_file_to_hashed[1:],
            FadeIn(*ith_msg_ledger_lbl[1:]),
            *[mob.animate.set_opacity(0.0) for mob in ith_hash_sticker[1:]],
            run_time=4
        )
        self.wait()

        ith_obj_ledger_Animate = [mob.animate.move_to(axes.c2p(*coordinates_ordered[i])) for i, mob in enumerate(ith_obj_ledger)]
        self.play(
            *ith_obj_ledger_Animate,
            run_time=3
        )

        time_lbl_FadeIn = [FadeIn(time_lbl[i].next_to(ith_obj_ledger[i], UP)) for i in range(len(time_lbl))] 
        self.play(LaggedStart(
            *time_lbl_FadeIn,
            lag_ratio=0.2,
        ))
        self.wait(3)
        # <<< 2nd Section <<<
# <<< 01 - Need for hashes <<<

# >>> aux folder >>>
class Folder(Scene):
    def construct(self):
        code_txt = '''use sha2::{Sha256, Digest};
fn main() {
    let mut hasher = Sha256::new();
    let string = "object1";
    hasher.update(string);
    let hash = hasher.finalize();
    println!("Binary hash: H({:?}) = {:?}", string, hash);

    let hex_hash = hex::encode(hash);
}
'''
        folder_back = SVGMobject("../../../../assets/svg/notoEmoji/File-Folder-back-only.svg")
        folder_front = SVGMobject("../../../../assets/svg/notoEmoji/File-Folder-cover-only.svg")
        msg = SVGMobject("../../../../assets/svg/excalidraw/msg-for-signature.svg").shift(UP * 2 + LEFT * 2)
        msg_hashed = SVGMobject("../../../../assets/svg/excalidraw/msg-for-signature-encrypted.svg").shift(DOWN + LEFT * 2)
        # code = SVGMobject("../../../../assets/svg/excalidraw/Code-Editor.svg").shift(UP * 2)
        # code_hashed = SVGMobject("../../../../assets/svg/excalidraw/Code-Editor-encrypted.svg").shift(DOWN)
        code=Code(
            code_string=code_txt,
            language="rust",
            background="window",
            background_config={"stroke_color": "maroon"},
            tab_width=2,
        ).shift(UP * 2).scale(0.4)
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
        code.set_z_index(8)
        # code_hashed.set_z_index(5)
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
            # code_hashed,
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
            Transform(msg, msg_hashed, replace_mobject_with_target_in_scene=True)
        )
        self.wait()
# <<< aux folder <<<


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
        alice = Character(name="Alice", show_name=True).move_to(UL * 2 + LEFT * 2)
        bob = Character(name="Bob", show_name=True).move_to(UR * 2 + RIGHT * 2)
        mallory = Character(name="Mallory", show_name=True, expr="Smiling-Face-With-Horns").move_to(DOWN * 2) 
        msg = SVGMobject("../../../../assets/svg/excalidraw/msg-for-signature").next_to(alice, RIGHT).scale(0.75)
        msg_hashed = SVGMobject("../../../../assets/svg/excalidraw/msg-for-signature-encrypted.svg")

        broadcast = Arc(radius=20, start_angle=3 * PI / 2, angle=PI / 2, color=PURE_GREEN).move_to(alice.get_center() + UL * 2)

        self.add(alice, bob)
        self.wait()
        self.play(LaggedStart(
            FadeIn(msg),
            Broadcast(broadcast, focal_point=alice.get_center(), n_mobs=10),
            lag_ratio=1,
            run_time=3
        ))
        self.play(
            msg.animate.next_to(bob, LEFT),
            run_time=2,
        )
        self.wait()
        self.add(mallory)
        self.wait()
# <<< 02 - Need for signatures <<<


# >>> 03 - Regular Functions >>>
class RegularFunctions(Scene):
    def addPointsToSet(
        self,
        mob,
        noise=0.1, 
        n_elements=10,
        labels=None,
        **kwargs
    ):
        amplitude = (mob.height / 2) * 0.75 
        dots_w_labels = []
        if labels is not None:
            n_elements = len(labels)
            mat = np.round(rng.normal(size=(n_elements, 2)) *  noise, 2)
            mat[:,0] += amplitude * np.linspace(-1, 1, n_elements)
            dots = [Dot(color=kwargs["color"], stroke_width=kwargs["stroke_width"]).move_to(mob.get_center() + DOWN * i[0] + RIGHT * i[1]) for i in mat]
            for i, dot in enumerate(dots):
                if labels[i] == "...":
                    dots[i].set_opacity(0.0)
                    dots_w_labels.append(MathTex("\\vdots", color=XTXT, font_size=42).move_to(dot))
                else:
                    dots_w_labels.append(VGroup(dot, MathTex(labels[i], color=XTXT, font_size=32).next_to(dot, kwargs["label_position"])))
            return dots_w_labels

        mat = np.round(rng.normal(size=(n_elements, 2)) *  noise, 2)
        mat[:,0] += amplitude * np.linspace(-1, 1, n_elements)
        dots = [Dot(color=kwargs["color"], stroke_width=kwargs["stroke_width"]).move_to(mob.get_center() + DOWN * i[0] + RIGHT * i[1]) for i in mat]
        return dots

    def construct(self):
        scene_title = VGroup(
            Text("Regular functions:\n", font="Excalifont", font_size=36, color=XTXT),
            MathTex("\\\\ F:X\\mapsto Y", font_size=40, color=XTXT)
        ).to_edge(UP)

        x_set_circle = Circle(radius=2, color=XTXT).move_to(LEFT * 3.5 + DOWN)
        x_set_title = MathTex("X", color=XTXT, font_size=40).next_to(x_set_circle, UP)
        x_set = VGroup(x_set_circle, x_set_title)
        x_labs_ = ["x_1"] #, "x_2", "...", "x_n", "x_{n+1}", "...", "x_m"]
        x_elements = self.addPointsToSet(
            x_set_circle,
            labels=x_labs_,
            **{"color": XPURPLE, "stroke_width": 0.5, "label_position": LEFT * 0.75}
        )

        y_set_circle = Circle(radius=2, color=XTXT).move_to(RIGHT * 3.5 + DOWN)
        y_set_title = MathTex("Y", color=XTXT, font_size=40).next_to(y_set_circle, UP)
        y_set = VGroup(y_set_circle, y_set_title)
        y_labs_ = ["y_1"] #, "y_2", "...", "y_n"]
        y_elements = self.addPointsToSet(
            y_set_circle,
            labels=y_labs_,
            **{"color": XRED, "stroke_width": 0.5, "label_position": RIGHT * 0.75}
        )


        self.add(scene_title, x_set, y_set)

        arr_fwd = []
        arr_bck = []
        for i, j in zip(x_elements[:len(y_elements)], y_elements):
            arr_fwd.append(
                CurvedArrow(
                    start_point=i[0].get_center(),
                    end_point=j[0].get_center(),
                    angle=-60 * PI / 180,
                    color=XTXT,
                    tip_length=0.2
                ),
            )
            arr_bck.append(
                CurvedArrow(
                    start_point=j[0].get_center(),
                    end_point=i[0].get_center(),
                    angle=-60 * PI / 180,
                    color=XTXT,
                    tip_length=0.2
                ),
            )
        arr_fwd_w_label = [VGroup(mob, MathTex(f"F(x_{i+1}) = y_{i+1}", color=XTXT, font_size=32).next_to(mob, UP)) for i, mob in enumerate(arr_fwd) if type(mob) != MathTex]
        arr_bck_w_label = [VGroup(mob, MathTex(r"F^{-1}"+f"(y_{i+1})=x_{i+1}", color=XTXT, font_size=32).next_to(mob, DOWN)) for i, mob in enumerate(arr_bck) if type(mob) != MathTex]

        self.add(x_set, y_set)
        self.play(
            *[FadeIn(i) for i in x_elements], 
            *[FadeIn(i) for i in y_elements],
        )
        self.wait()
        self.play(
            *[FadeIn(i) for i in arr_fwd_w_label],
        )
        self.wait()
        self.play(
            *[FadeIn(i) for i in arr_bck_w_label],
        )
        self.wait()
# <<< 03 - Regular Functions <<<

# >>> 05 - Collisions Functions >>>
class Collisions(Scene):
    def addPointsToSet(
        self,
        mob,
        noise=0.1, 
        n_elements=10,
        labels=None,
        **kwargs
    ):
        amplitude = (mob.height / 2) * 0.75 
        dots_w_labels = []
        if labels is not None:
            n_elements = len(labels)
            mat = np.round(rng.normal(size=(n_elements, 2)) *  noise, 2)
            mat[:,0] += amplitude * np.linspace(-1, 1, n_elements)
            dots = [Dot(color=kwargs["color"], stroke_width=kwargs["stroke_width"]).move_to(mob.get_center() + DOWN * i[0] + RIGHT * i[1]) for i in mat]
            for i, dot in enumerate(dots):
                if labels[i] == "...":
                    dots[i].set_opacity(0.0)
                    dots_w_labels.append(MathTex("\\vdots", color=XTXT, font_size=40).move_to(dot))
                else:
                    dots_w_labels.append(VGroup(dot, MathTex(labels[i], color=XTXT, font_size=28).next_to(dot, kwargs["label_position"])))
            return dots_w_labels

        mat = np.round(rng.normal(size=(n_elements, 2)) *  noise, 2)
        mat[:,0] += amplitude * np.linspace(-1, 1, n_elements)
        dots = [Dot(color=kwargs["color"], stroke_width=kwargs["stroke_width"]).move_to(mob.get_center() + DOWN * i[0] + RIGHT * i[1]) for i in mat]
        return dots

    def construct(self):
        x_set_circle = Circle(radius=2, color=XTXT).move_to(LEFT * 3.5)
        x_set_title = MathTex("X", color=XTXT, font_size=40).next_to(x_set_circle, UP)
        x_set = VGroup(x_set_circle, x_set_title)
        x_labs_ = ["x_1", "x_2", "...", "x_n", "x_{n+1}", "...", "x_m"]
        x_elements = self.addPointsToSet(
            x_set_circle,
            labels=x_labs_,
            **{"color": TEAL_E, "stroke_width": 0.5, "label_position": LEFT * 0.75}
        )

        y_set_circle = Circle(radius=2, color=XTXT).move_to(RIGHT * 3.5)
        y_set_title = MathTex("Y", color=XTXT, font_size=40).next_to(y_set_circle, UP)
        y_set = VGroup(y_set_circle, y_set_title)
        y_labs_ = ["y_1", "y_2", "...", "y_n"]
        y_elements = self.addPointsToSet(
            y_set_circle,
            labels=y_labs_,
            **{"color": RED_E, "stroke_width": 0.5, "label_position": RIGHT * 0.75}
        )


        self.add(x_set, y_set)

        arr_fwd = []
        for i, j in zip(x_elements[:len(y_elements)], y_elements):
            arr_fwd.append(
                CurvedArrow(
                    start_point=i[0].get_center(),
                    end_point=j[0].get_center(),
                    angle=-PI/3,
                    color=XTXT,
                    tip_length=0.2
                ),
            )
        arr_fwd_w_label = [VGroup(mob, MathTex(f"F(x_{i+1}) = y_{i+1}").next_to(mob, UP)) for i, mob in enumerate(arr_fwd) if mob != MathTex]

        self.add(x_set, y_set)
        self.play(
            *[FadeIn(i) for i in x_elements], 
            *[FadeIn(i) for i in y_elements],
        )
        self.wait()
        self.play(LaggedStart(
            *[FadeIn(i) for i in arr_fwd_w_label],
            lag_ratio=0.25
        ))
# <<< 05 - Collisions <<<


# >>> Array of folders in Ledger >>>
class TempExperimental(Scene):
    def construct(self):
        folder_back = SVGMobject("../../../../assets/svg/notoEmoji/File-Folder-back-only.svg")
        folder_front = SVGMobject("../../../../assets/svg/notoEmoji/File-Folder-cover-only.svg")
        msg_file = SVGMobject("../../../../assets/svg/excalidraw/msg-for-signature.svg").move_to(folder_front.get_center() + UP * 0.6 + LEFT * 0.1).rotate(10 * PI / 180).scale(0.85)
        lbl = SVGMobject("../../../../assets/svg/excalidraw/label.svg")
        msg = Group(folder_back, folder_front, msg_file, lbl).scale(0.2)

        folder_back.set_z_index(1)
        msg_file.set_z_index(2)
        folder_front.set_z_index(3)
        msg.set_z_index(4)
        self.remove(folder_back, folder_front, msg_file, msg)

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
        ith_obj = []
        ith_obj_group = []
        coordinates_ordered = [(i, j) for j in range(ax_y_range - 1, 0, -1) for i in range(1, ax_x_range)]
        coordinates_random = coordinates_ordered.copy()
        random.seed(42)
        random.shuffle(coordinates_random)
        k = 0
        print(coordinates_ordered)
        print(coordinates_random)
        for i in range(1, ax_x_range):
            for j in range(1, ax_y_range):
                print(f"(i,j,k)=({i}, {j}, {k})")
                ith_obj.append(msg.copy())
                folder_i = ith_obj[k].move_to(axes.c2p(*coordinates_random[k]))
                txt_ = Text(f"({i},{j})", color=BLACK, font_size=14).move_to(ith_obj[k].get_center()) 
                txt_.set_z_index(k + 10)
                self.remove(txt_)
                ith_obj_group.append(Group(ith_obj[k], txt_))
                self.add(
                    # folder_i,
                    # txt_,
                    ith_obj_group[k]
                )
                k += 1

        ith_obj_animate = [mob.animate.move_to(axes.c2p(*coordinates_ordered[k])) for k, mob in enumerate(ith_obj_group)]
        self.play(*ith_obj_animate, run_time=5)
# <<< Array of folders in Ledger <<<
