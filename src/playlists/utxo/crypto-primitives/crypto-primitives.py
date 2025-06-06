from manim import *
import numpy as np
from helper_coordinates import centerLabel, Character, HashLabel, addPointsToSet
from utils import PEOPLE, CoordinateHelper

# random Generator variable
rng = np.random.default_rng(seed=48)

# >>> 00 - Title >>>
class Title(Scene):
    def construct(self):
        # >>> Ingredient 1: Hashes & Signatures
        sticker_one = SVGMobject("../../../../assets/svg/excalidraw/sticker_one.svg").shift(DOWN * 0.25 + LEFT * 3)
        sticker_hash = SVGMobject("../../../../assets/svg/excalidraw/sticker-hash.svg").shift(DOWN * 0.25)
        sticker_signature = SVGMobject("../../../../assets/svg/excalidraw/sticker_signature.svg").shift(RIGHT * 3 + DOWN * 0.25)

        txt = Text("Hashes and Signatures", color=XTXT, font="Excalifont", font_size=48).shift(UP * 2)

        self.play(LaggedStart(
            Write(sticker_one),
            Write(sticker_hash),
            Write(Text("and", font="Excalifont", font_size=50, color=XTXT).next_to(sticker_hash, RIGHT * 0.9)),
            Write(sticker_signature),
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
        # self.next_section("Show world and ledger")
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
        msg_file = SVGMobject("../../../../assets/svg/excalidraw/msg-for-signature.svg").move_to(folder_front.get_center() + UP * 0.6 + LEFT * 0.1).rotate(10 * DEGREES).scale(0.85)
        msg_file_hashed = SVGMobject("../../../../assets/svg/excalidraw/msg-for-signature-encrypted.svg").move_to(folder_front.get_center() + UP * 0.6 + LEFT * 0.1).rotate(10 * DEGREES)
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
            code.animate.move_to(folder_front.get_center() + UP * 0.3 + LEFT * 0.1).rotate(10 * DEGREES).scale(0.75),
            nft_w_lbl.animate.move_to(folder_front.get_center() + UP * 0.3 + RIGHT * 0.1).rotate(10 * DEGREES).scale(0.75),
            msg.animate.move_to(folder_front.get_center() + UP * 0.3 + LEFT * 0.3).rotate(10 * DEGREES).scale(0.75)
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
            msg.animate.rotate(10 * DEGREES).scale(0.75).move_to(folder_front.get_center(), UP * 0.2)
        )


# >>> 02 - Need for signatures >>>
class NeedForSignatures(Scene):
# class NeedForSignatures(MovingCameraScene):
    def construct(self):
        # camera = self.camera.frame
        # camera.save_state()
        # self.play(camera.animate.move_to().set(width=ith_msg_ledger[0].width*5))
        #
        # world = SVGMobject("../../../../assets/svg/excalidraw/world.svg").scale(2.5)
        alice = Character(name="Alice", show_name=True).move_to(UL * 2 + LEFT * 2)
        bob = Character(name="Bob", show_name=True).move_to(UR * 2 + RIGHT * 2)
        mallory = Character(name="Mallory", show_name=True, expr="Smiling-Face-With-Horns").move_to(DOWN * 2) 
        
        msg_bob = SVGMobject("../../../../assets/svg/excalidraw/msg-for-signature").next_to(alice, RIGHT).scale(0.75)
        msg_mallory = msg_bob.copy()
        msg_hashed_bob = SVGMobject("../../../../assets/svg/excalidraw/msg-for-signature-encrypted.svg").scale(0.75).move_to(msg_bob.get_center())
        msg_hashed_mallory = msg_hashed_bob.copy().move_to(msg_mallory.get_center())

        hash_sticker = SVGMobject("../../../../assets/svg/excalidraw/sticker-hash.svg").scale(1.25)
        signature_sticker = SVGMobject("../../../../assets/svg/excalidraw/sticker_signature.svg").scale(1.25)
        correct_sticker_ = SVGMobject("../../../../assets/svg/excalidraw/correct.svg").scale(0.35)
        incorrect_sticker_ = SVGMobject("../../../../assets/svg/excalidraw/incorrect.svg").scale(0.35)
        question_sticker_ = SVGMobject("../../../../assets/svg/excalidraw/question-mark.svg").scale(0.35)
        correct_alice, correct_bob, correct_mallory = correct_sticker_.next_to(alice, DL * 0.1), correct_sticker_.copy().next_to(bob, DR * 0.1), correct_sticker_.copy().next_to(mallory, RIGHT * 0.5)
        incorrect_alice, incorrect_bob, incorrect_mallory = incorrect_sticker_.next_to(alice, DL * 0.1), incorrect_sticker_.copy().next_to(bob, DR * 0.1), incorrect_sticker_.copy().next_to(mallory, RIGHT * 0.5)
        question_alice, question_bob, question_mallory = question_sticker_.next_to(alice, DL * 0.1), question_sticker_.copy().next_to(bob, DR * 0.1), question_sticker_.copy().next_to(mallory, RIGHT * 0.5)

        hash_sticker.set_z_index(10)
        signature_sticker.set_z_index(11)
        self.remove(hash_sticker)
        self.remove(signature_sticker)

        broadcast = Arc(radius=20, start_angle=3 * PI / 2, angle=PI / 2, color=PURE_GREEN).move_to(alice.get_center() + UL * 2)

        self.add(alice, bob)
        self.wait()
        txt_00 = Text("Alice wants to send a message to Bob and Bob ONLY!", font="Excalifont", font_size=28, color=XTXT).move_to(ORIGIN)
        self.play(Write(txt_00))
        self.wait()
        self.play(FadeIn(msg_bob))
        self.wait(0.5)
        self.play(
            Broadcast(broadcast, focal_point=alice.get_center(), n_mobs=10, lag_ratio=0.5, run_time=3),
            msg_bob.animate.next_to(bob, LEFT)
        )
        self.wait()
        self.play(
            Create(correct_alice),
            Create(correct_bob),
            FadeOut(txt_00),
        )
        self.wait(2)
        self.play(FadeOut(correct_alice), FadeOut(correct_bob), FadeOut(msg_bob))
        self.play(FadeIn(mallory), run_time=3)
        self.play(
            Broadcast(broadcast, focal_point=alice.get_center(), n_mobs=10, lag_ratio=0.5, run_time=3),
            FadeIn(msg_bob.next_to(alice, RIGHT)),
            FadeIn(msg_mallory),
            msg_bob.animate.next_to(bob, LEFT),
            msg_mallory.animate.next_to(mallory, LEFT),
        )
        self.wait()
        self.play(
            Create(incorrect_alice),
            Create(incorrect_bob),
            Create(correct_mallory),
        )
        self.wait()
        txt_01 = Text("Is there a way we could\nuse hashes in this scenario?", font="Excalifont", font_size=28, color=XTXT).move_to(ORIGIN)
        self.play(Write(txt_01))
        self.wait()
        self.play(FadeOut(incorrect_alice), FadeOut(incorrect_bob), FadeOut(correct_mallory), FadeOut(msg_bob), FadeOut(msg_mallory))
        self.remove(txt_01)
        self.wait()
        self.play(
            Broadcast(broadcast, focal_point=alice.get_center(), n_mobs=10, lag_ratio=0.5, run_time=3),
            FadeIn(msg_bob.next_to(alice, RIGHT)),
        )
        self.play(FadeIn(hash_sticker.move_to(msg_bob.get_center())), run_time=1)
        self.play(LaggedStart(
            # FadeIn(hash_sticker.move_to(msg_bob.get_center())),
            hash_sticker.animate.set_opacity(0.25),
            Transform(msg_bob, msg_hashed_bob.move_to(msg_bob.get_center()), replace_mobject_with_target_in_scene=True),
            lag_ratio=1.5,
            run_time=3,
        ))
        self.add(msg_hashed_mallory.move_to(msg_hashed_bob.get_center()))
        self.wait(0.5)
        self.play(
            hash_sticker.animate.set_opacity(0.0),
            msg_hashed_bob.animate.next_to(bob, LEFT),
            msg_hashed_mallory.animate.next_to(mallory, LEFT),
        )
        self.wait()
        self.play(
            Create(question_alice),
            Create(question_bob),
            Create(question_mallory),
        )
        self.wait()
        txt_02 = Text("Alice's message is undecipherable\nto anyone else! Is there a way\nto make the message decipherable\nONLY to Bob?", font="Excalifont", font_size=24, color=XTXT).move_to(ORIGIN)
        self.play(Write(txt_02))
        self.wait(3)
        self.play(FadeOut(question_alice), FadeOut(question_bob), FadeOut(question_mallory), FadeOut(msg_hashed_bob), FadeOut(msg_hashed_mallory), FadeOut(txt_02))
        self.wait()

        # Animate Signature
        self.play(
            Broadcast(broadcast, focal_point=alice.get_center(), n_mobs=10, lag_ratio=0.5, run_time=3),
            FadeIn(msg_bob.next_to(alice, RIGHT)),
        )
        self.play(FadeIn(signature_sticker.move_to(msg_bob.get_center())), run_time=1)
        self.play(LaggedStart(
            # FadeIn(hash_sticker.move_to(msg_bob.get_center())),
            signature_sticker.animate.set_opacity(0.25),
            Transform(msg_bob, msg_hashed_bob.move_to(msg_bob.get_center()), replace_mobject_with_target_in_scene=True),
            lag_ratio=1.5,
            run_time=3,
        ))
        self.add(msg_hashed_mallory.move_to(msg_hashed_bob.get_center()))
        self.wait(0.5)
        self.play(
            signature_sticker.animate.set_opacity(0.0),
            msg_hashed_bob.animate.next_to(bob, LEFT),
            msg_hashed_mallory.animate.next_to(mallory, LEFT),
        )
        self.wait()
        # self.play(
        #
        # )
# <<< 02 - Need for signatures <<<


# >>> 03 - Regular Functions >>>
class RegularFunctions(Scene):
    def construct(self):
        title_0_ = Text("Regular functions", font="Excalifont", font_size=36, color=XTXT) 
        title_1_ = MathTex("F:X\\mapsto Y", font_size=44, color=XTXT).next_to(title_0_, RIGHT) 
        scene_title = VGroup(title_0_, title_1_).move_to(ORIGIN).to_edge(UP)

        x_set_circle = Circle(radius=1.75, color=XTXT).move_to(LEFT * 3.5 + DOWN * 0.75)
        x_set_title = MathTex("X", color=XTXT, font_size=40).next_to(x_set_circle, UP)
        x_set = VGroup(x_set_circle, x_set_title)
        x_labs = ["x_1"]
        x_elements = addPointsToSet(
            mob=x_set_circle,
            labels=x_labs,
            height_span=(x_set_circle.height / 2) * 0.85,
            **{"color": XPURPLE, "label_position": LEFT * 0.25}
        )

        y_set_circle = Circle(radius=1.75, color=XTXT).move_to(RIGHT * 3.7 + DOWN * 0.75)
        y_set_title = MathTex("Y", color=XTXT, font_size=40).next_to(y_set_circle, UP)
        y_set = VGroup(y_set_circle, y_set_title)
        y_labs = ["y_1"]
        y_elements = addPointsToSet(
            mob=y_set_circle,
            labels=y_labs,
            height_span=(y_set_circle.height / 2) * 0.6,
            **{"color": XRED, "label_position": RIGHT * 0.25}
        )

        self.play(LaggedStart(
            Write(scene_title),
            Create(x_set),
            Create(y_set),
            lag_ratio=0.5,
            run_time=3
        ))

        self.play(
            *[Write(i) for i in x_elements], 
            *[Write(i) for i in y_elements],
        )

        # Add arrows, labels and animate
        arr_fwd = []
        arr_bck = []
        arr_fwd_w_label = []
        arr_bck_w_label = []
        map_ix = [0]
        for k, i in enumerate(map_ix):
            if i < 5:
                j = i
                arrow_arc = -60 * DEGREES
            elif i == 5:
                j = 2
                arrow_arc = -30 * DEGREES
            # elif i > 5:

            arr_fwd += [CurvedArrow(
                start_point=x_elements[i][0].get_center(),
                end_point=y_elements[j][0].get_center(),
                angle=arrow_arc,
                color=XTXT,
                tip_length=0.2
            )]
            arr_fwd_w_label += [VGroup(
                arr_fwd[-1], 
                MathTex(
                    "F("+x_labs[i]+") ="+y_labs[j], 
                    color=XTXT, 
                    font_size=32,
                    substrings_to_isolate=[
                        x_labs[i],
                        y_labs[j],
                    ]
                ).next_to(arr_fwd[-1], UP * 0.5)
            )]
        
            arr_bck += [CurvedArrow(
                start_point=y_elements[j][0].get_center(),
                end_point=x_elements[i][0].get_center(),
                angle=arrow_arc,
                color=XTXT,
                tip_length=0.2
            )]
            arr_bck_w_label += [VGroup(
                arr_bck[-1], 
                MathTex(
                    r"F^{-1}("+y_labs[j]+") = "+x_labs[i],
                    color=XTXT,
                    font_size=32,
                    substrings_to_isolate=[
                        x_labs[i],
                        y_labs[j],
                    ]
                ).next_to(arr_bck[-1], DOWN * 0.5)
            )]

            # F maps X -> Y
            self.play(Write(arr_fwd_w_label[k]), run_time=1.5)
            self.wait()
            # emphasize x points in XPURPLE
            self.play(
                x_elements[i][1].animate.set_color(XPURPLE).scale(1.5),
                arr_fwd_w_label[k][1].get_part_by_tex(x_labs[i]).animate.set_color(XPURPLE).scale(1.5), 
                run_time=0.75
            )
            self.wait(0.5)
            self.play(
                x_elements[i][1].animate.set_color(XTXT).scale(1/1.5),
                arr_fwd_w_label[k][1].get_part_by_tex(x_labs[i]).animate.set_color(XTXT).scale(1/1.5),
                run_time=0.75
            )
            # emphasize y points in XRED
            self.wait(0.5)
            self.play(
                y_elements[j][1].animate.set_color(XRED).scale(1.5),
                arr_fwd_w_label[k][1].get_part_by_tex(y_labs[j]).animate.set_color(XRED).scale(1.5), 
                run_time=0.75
            )
            self.wait(0.5)
            self.play(
                y_elements[j][1].animate.set_color(XTXT).scale(1/1.5),
                arr_fwd_w_label[k][1].get_part_by_tex(y_labs[j]).animate.set_color(XTXT).scale(1/1.5),
                run_time=0.75
            )

            # F inverse maps Y -> Y
            self.play(Create(arr_bck_w_label[k]))
            self.wait()
            # emphasize y points in XRED
            self.wait(0.5)
            self.play(
                y_elements[j][1].animate.set_color(XRED).scale(1.5),
                arr_bck_w_label[k][1].get_part_by_tex(y_labs[j]).animate.set_color(XRED).scale(1.5), 
                run_time=0.75
            )
            self.wait(0.5)
            self.play(
                y_elements[j][1].animate.set_color(XTXT).scale(1/1.5),
                arr_bck_w_label[k][1].get_part_by_tex(y_labs[j]).animate.set_color(XTXT).scale(1/1.5),
                run_time=0.75
            )
            # emphasize x points in XPURPLE
            self.play(
                x_elements[i][1].animate.set_color(XPURPLE).scale(1.5),
                arr_bck_w_label[k][1].get_part_by_tex(x_labs[i]).animate.set_color(XPURPLE).scale(1.5), 
                run_time=0.75
            )
            self.wait(0.5)
            self.play(
                x_elements[i][1].animate.set_color(XTXT).scale(1/1.5),
                arr_bck_w_label[k][1].get_part_by_tex(x_labs[i]).animate.set_color(XTXT).scale(1/1.5),
                run_time=0.75
            )
        self.wait(0.5)

        txt_0_ = MathTex("F", font_size=38, color=XTXT).shift(DOWN * 0.2)
        txt_01_ = Text("is an invertible function!", font="Excalifont", font_size=28, color=XTXT).next_to(txt_0_, RIGHT)
        txt_0 = VGroup(txt_0_, txt_01_).move_to(ORIGIN).to_edge(DOWN) 
        self.play(Write(txt_0))
        self.wait(2)
        self.play(
            [FadeOut(i) for i in arr_fwd_w_label],
            [FadeOut(i) for i in arr_bck_w_label],
            FadeOut(txt_0),
            run_time=2,
        )
        self.wait()
# <<< 03 - Regular Functions <<<


# >>> 04 - Hash Functions >>>
class HashFunctions(Scene):
    def construct(self):
        # recreate last scene:  <<< 03 - Regular Functions <<<
        prev_title_0_ = Text("Regular functions", font="Excalifont", font_size=36, color=XTXT) 
        prev_title_1_ = MathTex("F:X\\mapsto Y", font_size=44, color=XTXT).next_to(prev_title_0_, RIGHT) 
        prev_scene_title = VGroup(prev_title_0_, prev_title_1_).move_to(ORIGIN).to_edge(UP)

        # Continue with current scene
        title_0_ = Text("Hash functions", font="Excalifont", font_size=36, color=XTXT) 
        title_1_ = MathTex("H:X\\mapsto Y", font_size=46, color=XTXT).next_to(title_0_, RIGHT) 
        scene_title = VGroup(title_0_, title_1_).move_to(ORIGIN).to_edge(UP)

        incorrect_1 = SVGMobject("../../../../assets/svg/excalidraw/incorrect.svg").scale(0.5).set_opacity(0.75)
        incorrect_2 = incorrect_1.copy()

        x_set_circle = Circle(radius=1.75, color=XTXT).move_to(LEFT * 3.5 + DOWN * 0.75)
        x_set_title = MathTex("X", color=XTXT, font_size=40).next_to(x_set_circle, UP)
        x_set = VGroup(x_set_circle, x_set_title)
        x_labs = ["x_1"]
        x_elements = addPointsToSet(
            mob=x_set_circle,
            labels=x_labs,
            height_span=(x_set_circle.height / 2) * 0.85,
            **{"color": XPURPLE, "label_position": LEFT * 0.25}
        )

        y_set_circle = Circle(radius=1.75, color=XTXT).move_to(RIGHT * 3.7 + DOWN * 0.75)
        y_set_title = MathTex("Y", color=XTXT, font_size=40).next_to(y_set_circle, UP)
        y_set = VGroup(y_set_circle, y_set_title)
        y_labs = ["y_1"]
        y_elements = addPointsToSet(
            mob=y_set_circle,
            labels=y_labs,
            height_span=(y_set_circle.height / 2) * 0.6,
            **{"color": XRED, "label_position": RIGHT * 0.25}
        )

        # recreate previous scene and transform to initial state
        self.add(
            prev_scene_title,
            x_set,
            y_set,
            *x_elements,
            *y_elements,
        )
        self.wait(2)
        self.play(Transform(prev_scene_title, scene_title), replace_mobject_with_target_in_scene=True)
        self.wait(2)

        # Add arrows, labels and animate
        arr_fwd = []
        arr_bck = []
        arr_fwd_w_label = []
        arr_bck_w_label = []
        map_ix = [0]
        for k, i in enumerate(map_ix):
            if i < 5:
                j = i
                arrow_arc = -60 * DEGREES
            elif i == 5:
                j = 2
                arrow_arc = -30 * DEGREES

            arr_fwd += [CurvedArrow(
                start_point=x_elements[i][0].get_center(),
                end_point=y_elements[j][0].get_center(),
                angle=arrow_arc,
                color=XTXT,
                tip_length=0.2
            )]
            arr_fwd_w_label += [VGroup(
                arr_fwd[-1], 
                MathTex(
                    "H("+x_labs[i]+") ="+y_labs[j], 
                    color=XTXT, 
                    font_size=32,
                    substrings_to_isolate=[
                        x_labs[i],
                        y_labs[j],
                    ]
                ).next_to(arr_fwd[-1], UP * 0.5)
            )]
        
            arr_bck += [CurvedArrow(
                start_point=y_elements[j][0].get_center(),
                end_point=x_elements[i][0].get_center(),
                angle=arrow_arc,
                color=XTXT,
                tip_length=0.2
            )]
            arr_bck_w_label += [VGroup(
                arr_bck[-1], 
                MathTex(
                    r"H^{-1}("+y_labs[j]+") = "+x_labs[i],
                    color=XTXT,
                    font_size=32,
                    substrings_to_isolate=[
                        x_labs[i],
                        y_labs[j],
                    ]
                ).next_to(arr_bck[-1], DOWN * 0.5)
            )]

            # F maps X -> Y
            self.play(Write(arr_fwd_w_label[k]), run_time=1.5)
            self.wait()
            # emphasize x points in XPURPLE
            self.play(
                x_elements[i][1].animate.set_color(XPURPLE).scale(1.5),
                arr_fwd_w_label[k][1].get_part_by_tex(x_labs[i]).animate.set_color(XPURPLE).scale(1.5), 
                run_time=0.75
            )
            self.wait(0.5)
            self.play(
                x_elements[i][1].animate.set_color(XTXT).scale(1/1.5),
                arr_fwd_w_label[k][1].get_part_by_tex(x_labs[i]).animate.set_color(XTXT).scale(1/1.5),
                run_time=0.75
            )
            # emphasize y points in XRED
            self.wait(0.5)
            self.play(
                y_elements[j][1].animate.set_color(XRED).scale(1.5),
                arr_fwd_w_label[k][1].get_part_by_tex(y_labs[j]).animate.set_color(XRED).scale(1.5), 
                run_time=0.75
            )
            self.wait(0.5)
            self.play(
                y_elements[j][1].animate.set_color(XTXT).scale(1/1.5),
                arr_fwd_w_label[k][1].get_part_by_tex(y_labs[j]).animate.set_color(XTXT).scale(1/1.5),
                run_time=0.75
            )

        self.wait(2)
        self.play(Succession(
            Create(arr_bck_w_label[0]),
            FadeIn(incorrect_1.move_to(arr_bck_w_label[0].get_center() + DOWN * 0.5)),
            lag_ratio=1,
            run_time=3,
        ))
        self.wait()
        # Fade opaque
        self.play(
            *[i.animate.set_opacity(0.15) for i in x_elements],
            *[i.animate.set_opacity(0.15) for i in y_elements],
            *[i.animate.set_opacity(0.0) for i in arr_fwd_w_label],
            *[i.animate.set_opacity(0.0) for i in arr_bck_w_label],
            incorrect_1.animate.set_opacity(0.0),
            run_time=1.5,
        )
        self.wait()

        # Oranges to orange juice analogy
        orange_ = SVGMobject("../../../../assets/svg/kawaii/orange.svg").scale(0.75)
        oranges = Group(
            orange_.shift(UR * 0.6),
            orange_.copy().shift(LEFT * 0.4),
            orange_.copy().shift(DOWN * 0.4)
        ).scale(0.5).move_to(x_set_circle.get_center() + DOWN * 0.5)
        orange_juice = SVGMobject("../../../../assets/svg/openMoji/orange-juice-jar.svg").scale(0.35).move_to(y_set_circle.get_center() + DOWN * 0.5)
        blender = SVGMobject("../../../../assets/svg/excalidraw/blender.svg").scale(0.85).move_to(ORIGIN)
        blender_bottom_point = blender.get_bottom()

        arr_to_blender = CurvedArrow(
            start_point=oranges.get_center(),
            end_point=blender.get_center(),
            angle=-30 * DEGREES,
            color=XTXT,
            tip_length=0.0,
        )
        arr_to_juice = CurvedArrow(
            start_point=blender.get_center(),
            end_point=orange_juice.get_center(),
            angle=-30 * DEGREES,
            color=XTXT,
            tip_length=0.2,
        )
        arr_to_oranges = CurvedArrow(
            start_point=orange_juice.get_center(),
            end_point=oranges.get_center(),
            angle=-60 * DEGREES,
            color=XTXT,
            tip_length=0.2,
        )
        blender.set_z_index(6)
        arr_to_blender.set_z_index(4)
        arr_to_juice.set_z_index(5)

        self.remove(blender, arr_to_blender, arr_to_juice)
        self.play(Succession(
            FadeIn(oranges),
            Create(arr_to_blender),
        ))

        # shaking blender
        def shake_function(mob, alpha):
            # More complex oscillation pattern
            # Decreasing amplitude for a more realistic shake that settles down
            frequency = 100
            damping = 1 - alpha  # Decreases over time
            angle = 10 * damping * np.sin(alpha * np.pi * frequency) * DEGREES
            
            # Reset and rotate
            mob.rotate(angle, about_point=blender_bottom_point)

        shake_animation = UpdateFromAlphaFunc(
            blender,
            shake_function,
            rate_func = lambda t: there_and_back(t) if t < 0.5 else there_and_back(2*t-1)
        )
        self.play(Succession(
            FadeIn(blender),
            shake_animation,
            run_time=3,
        ))
        self.play(Succession(
            Create(arr_to_juice),
            FadeIn(orange_juice),
            Create(arr_to_oranges),
            FadeIn(incorrect_2.move_to(arr_to_oranges.get_center() + DOWN * 0.5)),
            lag_start=3,
            run_time=5,
        ))
        self.wait()

        txt_0_ = MathTex("H", font_size=38, color=XTXT).shift(DOWN * 0.2)
        txt_01_ = Text("is NOT an invertible function!", font="Excalifont", font_size=28, color=XTXT).next_to(txt_0_, RIGHT)
        txt_0 = VGroup(txt_0_, txt_01_).move_to(ORIGIN).to_edge(DOWN) 
        self.play(Write(txt_0))
        self.wait(2)
        self.play(
            *[FadeOut(i) for i in arr_fwd_w_label],
            *[FadeOut(i) for i in arr_bck_w_label],
            *[FadeOut(i) for i in x_elements],
            *[FadeOut(i) for i in y_elements],
            FadeOut(txt_0),
            FadeOut(oranges),
            FadeOut(arr_to_blender),
            FadeOut(blender),
            FadeOut(arr_to_juice),
            FadeOut(orange_juice),
            FadeOut(arr_to_oranges),
            FadeOut(incorrect_2),
            run_time=3,
        )
        self.wait()
# <<< 04 - Hash Functions <<<


# >>> 05 - Collisions Functions >>>
class Collisions(Scene):
    def construct(self):
        # recreate last scene:  <<< 03 - Regular Functions <<<
        prev_title_0_ = Text("Hash functions", font="Excalifont", font_size=36, color=XTXT) 
        prev_title_1_ = MathTex("H:X\\mapsto Y", font_size=44, color=XTXT).next_to(prev_title_0_, RIGHT) 
        prev_scene_title = VGroup(prev_title_0_, prev_title_1_).move_to(ORIGIN).to_edge(UP)

        # Continue with current scene
        scene_title = Text("Collisions", font="Excalifont", font_size=36, color=XTXT).to_edge(UP) 

        x_set_circle_small = Circle(radius=1.75, color=XTXT).move_to(LEFT * 3.5 + DOWN * 0.75)
        x_set_circle = Circle(radius=3.0, color=XTXT).move_to(LEFT * 3.5 + DOWN * 0.75)
        x_set_title = MathTex("X", color=XTXT, font_size=40).next_to(x_set_circle_small, UP)

        y_set_circle = Circle(radius=1.75, color=XTXT).move_to(RIGHT * 3.7 + DOWN * 0.75)
        y_set_title = MathTex("Y", color=XTXT, font_size=40).next_to(y_set_circle, UP)
        y_set = VGroup(y_set_circle, y_set_title)
        y_labs = ["y_1", "y_2", "y_3","...", "y_n"]
        y_elements = addPointsToSet(
            mob=y_set_circle,
            labels=y_labs,
            height_span=(y_set_circle.height / 2) * 0.6,
            **{"color": XRED, "label_position": RIGHT * 0.25}
        )

        collision = SVGMobject("../../../../assets/svg/excalidraw/collision.svg").scale(0.5)

        # recreate previous scene and transform to initial state
        self.add(
            prev_scene_title,
            x_set_circle_small,
            x_set_title,
            y_set,
        )
        self.wait(2)
        self.play(
            Transform(prev_scene_title, scene_title, replace_mobject_with_target_in_scene=True),
        )
        self.wait()
        self.play(
            ReplacementTransform(x_set_circle_small, x_set_circle),
            x_set_title.animate.next_to(x_set_circle, UP),
        )
        self.wait(2)
        # create x elements after growing circle
        x_set = VGroup(x_set_circle, x_set_title)
        x_labs = ["x_1", "x_2", "x_3", "...", "x_n", "x_{n+1}", "...", "x_m"]
        x_elements = addPointsToSet(
            mob=x_set_circle,
            labels=x_labs,
            height_span=(x_set_circle.height / 2) * 0.85,
            **{"color": XPURPLE, "label_position": LEFT * 0.25}
        )

        self.play(
            *[FadeIn(i) for i in x_elements], 
            *[FadeIn(i) for i in y_elements],
        )
        self.wait()
        m_much_greater_n = MathTex(r"m>n", color=XTXT, font_size=44, substrings_to_isolate=["m","n"]).move_to(UP * 2 + RIGHT * 0.5)
        self.play(Create(m_much_greater_n))
        # emphasize m & x points in XPURPLE
        self.wait(0.75)
        self.play(
            m_much_greater_n.get_part_by_tex("m").animate.set_color(XPURPLE).scale(1.5),
            *[i[1].animate.set_color(XPURPLE).scale(1.5) for i in x_elements],
        )
        self.wait(0.3)
        self.play(
            m_much_greater_n.get_part_by_tex("m").animate.set_color(XTXT).scale(1/1.5),
            *[i[1].animate.set_color(XTXT).scale(1/1.5) for i in x_elements],
        )
        # emphasize n & y points in XRED
        self.wait(0.75)
        self.play(
            m_much_greater_n.get_part_by_tex("n").animate.set_color(XPURPLE).scale(1.5),
            *[i[1].animate.set_color(XRED).scale(1.5) for i in y_elements],
        )
        self.wait(0.3)
        self.play(
            m_much_greater_n.get_part_by_tex("n").animate.set_color(XTXT).scale(1/1.5),
            *[i[1].animate.set_color(XTXT).scale(1/1.5) for i in y_elements],
        )
        self.wait(0.5)
        self.play(FadeOut(m_much_greater_n))
        self.wait(0.5)

        # Add arrows, labels and animate
        arr_fwd = []
        arr_fwd_w_label = []
        # mapix indexes point to:
        #        [x1,x2,x3,xn,xn+1]
        #         |  |  |  |  |
        #         v  v  v  v  v
        #        [y1,y2,y3,yn,y3] # collision in H(x3)=y3=H(n+1)
        map_ix = [0, 1, 2, 4, 5]
        for k, i in enumerate(map_ix):
            if i < 5:
                j = i
                arrow_arc = -60 * DEGREES
                wait_between_arrows = 0.3
            elif i == 5:
                j = 2
                arrow_arc = -30 * DEGREES
                wait_between_arrows = 3

            arr_fwd += [CurvedArrow(
                start_point=x_elements[i][0].get_center(),
                end_point=y_elements[j][0].get_center(),
                angle=arrow_arc,
                color=XTXT,
                tip_length=0.2,
                fill_opacity=0
            )]
            arr_fwd_w_label += [VGroup(
                arr_fwd[-1], 
                MathTex(
                    "H("+x_labs[i]+") ="+y_labs[j], 
                    color=XTXT, 
                    font_size=32,
                    substrings_to_isolate=[
                        x_labs[i],
                        y_labs[j],
                    ]
                ).next_to(arr_fwd[-1], UP * 0.5).shift(RIGHT * 0.5)
            )]
        
            # animate inside the loop
            # start at second point
            self.play(Write(arr_fwd_w_label[k]), run_time=1.5)
            self.wait(0.3)
            # emphasize x points in XPURPLE
            self.play(
                x_elements[i][1].animate.set_color(XPURPLE).scale(1.5),
                arr_fwd_w_label[k][1].get_part_by_tex(x_labs[i]).animate.set_color(XPURPLE).scale(1.5), 
                run_time=0.75
            )
            self.wait(0.3)
            self.play(
                x_elements[i][1].animate.set_color(XTXT).scale(1/1.5),
                arr_fwd_w_label[k][1].get_part_by_tex(x_labs[i]).animate.set_color(XTXT).scale(1/1.5),
                run_time=0.75
            )

            # Collision occurs at index 5
            # NOTE.- when i == 5, j = 2
            if i == 5:
                # bring back y_3, remove opacity emphasize y points in XRED
                self.wait(0.3)
                self.play(
                    y_elements[j].animate.set_opacity(1.0),
                )
                self.play(
                    y_elements[j][1].animate.set_color(XRED).scale(1.5),
                    arr_fwd_w_label[k][1].get_part_by_tex(y_labs[j]).animate.set_color(XRED).scale(1.5), 
                    run_time=0.75
                )
                # bring back x_3 & arrow to y_3 removing opacity
                self.wait()
                self.play(
                    x_elements[j].animate.set_opacity(1.0),
                )
                # emphasize x points in XPURPLE
                self.wait(0.3)
                self.play(Write(arr_fwd_w_label[j], run_time=1.5))
                self.wait(0.3)
                self.play(
                    x_elements[j][1].animate.set_color(XPURPLE).scale(1.5),
                    arr_fwd_w_label[j][1].get_part_by_tex(x_labs[j]).animate.set_color(XPURPLE).scale(1.5), 
                    run_time=0.75
                )
                self.wait(0.3)
                self.play(
                    x_elements[j][1].animate.set_color(XTXT).scale(1/1.5),
                    arr_fwd_w_label[j][1].get_part_by_tex(x_labs[j]).animate.set_color(XTXT).scale(1/1.5),
                    run_time=0.75
                )
                self.wait(0.3)
                self.play(
                    y_elements[j].animate.set_opacity(1.0),
                    y_elements[j][1].animate.set_color(XRED).scale(1.5),
                    arr_fwd_w_label[j][1].get_part_by_tex(y_labs[j]).animate.set_color(XRED).scale(1.5), 
                    run_time=0.75
                )
                self.play(FadeIn(collision.next_to(y_elements[j], LEFT * 0.25)), run_time=2)
            else:
                # emphasize y points in XRED
                self.wait(0.3)
                self.play(
                    y_elements[j][1].animate.set_color(XRED).scale(1.5),
                    arr_fwd_w_label[k][1].get_part_by_tex(y_labs[j]).animate.set_color(XRED).scale(1.5), 
                    run_time=0.75
                )
                self.wait(0.3)
                self.play(
                    y_elements[j][1].animate.set_color(XTXT).scale(1/1.5),
                    arr_fwd_w_label[k][1].get_part_by_tex(y_labs[j]).animate.set_color(XTXT).scale(1/1.5),
                    run_time=0.75
                )
                # set opaque arrow
                self.wait(wait_between_arrows)
                self.play(
                    x_elements[i].animate.set_opacity(0.25),
                    y_elements[j].animate.set_opacity(0.25),
                    FadeOut(arr_fwd_w_label[k]),
                )
                self.wait(0.3)
        self.wait(2)

        # exemplify more arrows more collisions
        # more_map_ix indexes point to:
        #             [ ... ,   xm ]
        #               |        |
        #               v        v
        #            [collision,collision] # more arrows more collisions
        more_map_ix = [6, 7]
        arr_coll = []
        arr_coll_svg = [collision.copy(), collision.copy()]

        for k, i in enumerate(more_map_ix):
            arr_coll += [CurvedArrow(
                start_point=x_elements[i][0].get_center() + RIGHT * (0.1 - k / 10),
                end_point=y_elements[i-3][0].get_center() + LEFT * 2.5 + DOWN * (k + 0.25),
                angle=30 * DEGREES,
                color=XTXT,
                tip_length=0.2,
                fill_opacity=0
            )]
            self.play(LaggedStart(
                Write(arr_coll[k]),
                FadeIn(arr_coll_svg[k].next_to(arr_coll[k][1], RIGHT * 0.25)),
                lag_ratio=0.75,
                run_time=1.5
            ))
            self.wait(0.3)
        self.wait()
# <<< 05 - Collisions <<<


# >>> 06 - TwoKappa >>>
class TwoKappa(MovingCameraScene):
    def construct(self):
        # recreate prev scene >>> 05 - Collisions >>>
        x_set = VGroup(
            
        )
        prev_title
        prev_arr = []
        prev_arr_w_lbl = []
        collision_ = 
        collisions = 
# <<< 06 - TwoKappa <<<


# >>> Array of folders in Ledger >>>
class TempExperimental(Scene):
    def construct(self):
        folder_back = SVGMobject("../../../../assets/svg/notoEmoji/File-Folder-back-only.svg")
        folder_front = SVGMobject("../../../../assets/svg/notoEmoji/File-Folder-cover-only.svg")
        msg_file = SVGMobject("../../../../assets/svg/excalidraw/msg-for-signature.svg").move_to(folder_front.get_center() + UP * 0.6 + LEFT * 0.1).rotate(10 * DEGREES).scale(0.85)
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


# >>> test higlight LaTeX >>>
class EmphasizeTerm(Scene):
    def construct(self):
        # Isolate terms using substrings_to_isolate
        equation = MathTex(
            r"\operatorname{Ver}(pk,m,\operatorname{Sig}(sk,m))=\text{true}",
            substrings_to_isolate=[
                r"\operatorname{Ver}", 
                "pk", 
                "m", 
                r"\operatorname{Sig}(sk,m)"
            ]
        ).scale(1.5)
        
        self.add(equation)
        self.wait(0.5)

        # Term-color pairs for animation
        term_color_sequence = [
            (r"\operatorname{Ver}", RED),
            ("pk", YELLOW),
            ("m", ORANGE),
            (r"\operatorname{Sig}(sk,m)", PURPLE)
        ]

        # Animate each term sequentially
        for term_str, color in term_color_sequence:
            term = equation.get_part_by_tex(term_str)
            original_scale = term.scale
            
            self.play(
                term.animate
                .set_color(color)
                .scale(1.3),      # Enlarge for emphasis
                run_time=0.75
            )
            self.wait(0.5)
            self.play(
                term.animate
                .set_color(WHITE)  # Revert to original color
                .scale(1/1.3),     # Return to original size
                run_time=0.75
            )
            self.wait(0.3)
# <<< test higlight LaTeX <<<


# >>> test grow set >>>
class TestGrowSet(Scene):
    def construct(self):
        x_set_circle = Circle(radius=1.75, color=XTXT).move_to(LEFT * 3.5 + DOWN * 0.75)
        x_set_title = Text("X set", font_size=38, color=XTXT).next_to(x_set_circle, UP)
        y_set_circle = Circle(radius=1.75, color=XTXT).move_to(RIGHT * 3.7 + DOWN * 0.75)

        self.play(
            Create(x_set_circle),
            Create(x_set_title),
            run_time=1,
        )
        self.wait()
        self.play(
            x_set_circle.animate.scale(3.0 / 1.75),
            run_time=0.5,
        )
        self.play(
            x_set_title.animate.next_to(x_set_circle, UP), #, buff=SMALL_BUFF),
            run_time=0.5,
        )
        self.wait()
        x_set = VGroup(x_set_circle, x_set_title)
        self.play(x_set.animate.move_to(ORIGIN))
        self.wait()
# <<< test grow set <<<
