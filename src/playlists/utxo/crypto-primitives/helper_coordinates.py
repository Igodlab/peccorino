from manim import *


PEOPLE = {
    "Alice": {"color": "#56B6F7", "faceColor": "SkyBlue"}, # (Bright Sky Blue) - Primary legitimate user/sender
    "Bob": {"color": "#00E676", "faceColor": "VibrantGreen"}, # (Vibrant Green) - Primary legitimate receiver
    "Charlie": {"color": "#FFDD00", "faceColor": "SunnyYellow"}, # (Sunny Yellow) - Third legitimate participant
    "Eve": {"color": "#FF5252", "faceColor": "BrightRed"}, # (Bright Red) - Eavesdropper (passive attacker)
    "Mallory": {"color": "#FF55FF", "faceColor": "HotPink"}, # (Hot Pink) - Malicious attacker (active)
    "Trent": {"color": "#56CBCB", "faceColor": "Teal"}, # (Teal) - Trusted third party
    "Peggy": {"color": "#C792EA", "faceColor": "SoftPurple"}, # (Soft Purple) - Prover in zero-knowledge proofs
    "Victor": {"color": "#FF9E64", "faceColor": "WarmOrange"}, # (Warm Orange) - Verifier in zero-knowledge proofs
    "Grace": {"color": "#AEEA00", "faceColor": "MintGreen"}, # (Mint Green) - Group coordinator
    "Sybil": {"color": "#FF7AB2", "faceColor": "BrightPink"}, # (Bright Pink) - Multiple fake identities
}

# >>> Flatten List >>>
def FlattenList(nested_list):
    def flatten(lst):
        for item in lst:
            if isinstance(item, list):
                flatten(item)
            else:
                flat_lst.append(item)

    flat_lst = []
    flatten(nested_list)
    return flat_lst
# <<< Flatten List <<<


# >>> get center for label emoji >>>
def centerLabel(obj: ImageMobject):
    # select font size to 18 for a label of size 0.5
    return obj.get_center() + DOWN * 0.2 + RIGHT * 0.2
# <<< get center for label emoji <<<

# >>> Hash label Mobject >>>
class HashLabel(Group):
    def __init__(
        self,
        text: str | None = None,
        hash_text: bool = True,
        **kwargs
    ): 
        Group.__init__(self, **kwargs)

        svg_path = "../../../../assets/svg/excalidraw/label.svg"
        self.label_svg_ = SVGMobject(svg_path)
        if hash_text == True:
            hash_txt_ = f"{text}" # Rust sha256(text)
            lbl_name = "" + hash_txt_[:2] + ".\\hfil .\\hfil ." + hash_txt_[-2:]
        else:
            lbl_name = f"{text}"

        self.label_txt_ = MathTex(lbl_name, color=BLACK, font_size=38).move_to(centerLabel(self.label_svg_)).rotate(angle=-PI/4)
        self.hash_label = Group(self.label_svg_, self.label_txt_).scale(0.25)
        self.add(self.hash_label)

# <<< Hash label Mobject <<<

# class PersonExpression:
#     def __init__(self)


# >>> Emoji Person >>>
class Character(Group):
    def __init__(
            self, 
            # obj: SVGMobject, 
            name: str | None = None, 
            expr: str = "Slightly-Smiling-Face",
            show_name: bool = False, 
            **kwargs
    ):
        Group.__init__(self, **kwargs)

        svg_path = "../../../../assets/svg/excalidraw/person-w.svg"
        self.person = SVGMobject(svg_path)
        self.add(self.person)

        # get shape
        self.w = self.person.width
        self.h = self.person.height
        self.c = self.person.get_center()

        if name is not None:
            color = PEOPLE[name]["color"]
            faceColor = PEOPLE[name]["faceColor"]

            # Option to show emotion
            face_path = f"../../../../assets/svg/openMoji/{expr}-{faceColor}.svg"
            face = SVGMobject(face_path).shift(self.c + UP * 0.52 + RIGHT * 0.068).scale(0.53)
            self.add(face)

            # Option to show name
            if show_name:
                self.name_text = Text(
                    name,
                    font="Excalifont",
                    color=color,
                    font_size=24,
                ).next_to(self.person, DOWN, buff=0.2)

                self.name_text_boundary = AnimatedBoundary(
                    self.name_text, 
                    colors=[BLACK],
                    max_stroke_width=4,

                )

                # self.signature = Text(
                #     name,
                #     font="Whispering Signature-Personal use",
                #     color=color,
                #     font_size=24,
                # ).next_to(self.person, DOWN * 3, buff=0.2)
                #
                # self.signature_boundary = AnimatedBoundary(
                #     self.signature, 
                #     colors=[BLACK],
                # )

                self.add(
                    self.name_text_boundary,
                    self.name_text,
                    # self.signature_boundary,
                    # self.signature,
                )
# <<< Emoji Person <<<


# >>> Hash label Mobject >>>
# class HashLabel(Group):
#     def __init__(
#         self,
#         txt: str | None = None,
#         **kwargs
#     ):
#         lbl_svg_ = SVGMobject("../../../../assets/svg/excalidraw/label.svg")
#
#         if txt == None:
#             self.add(lbl_txt_)
#
#         lbl_txt_ = 

# <<< Hash label Mobject <<<


class AnimateCharacter(Scene):
    def construct(self):
        # >>> Character >>>
        positions = [
            UP * 3 + LEFT * 6,
            UP * 3 + LEFT * 3,
            UP * 3,
            UP * 3 + RIGHT * 3,
            UP * 3 + RIGHT * 6,
            DOWN + LEFT * 6,
            DOWN + LEFT * 3,
            DOWN,
            DOWN + RIGHT * 3,
            DOWN + RIGHT * 6,
        ]
        person = []
        for i, nm in enumerate(PEOPLE):
            person.append(Character(
                name = nm,
                show_name=True
            ).shift(positions[i]))
            self.play(FadeIn(person[i]))
            self.wait(2)
            # if i > 4: 
            #     break
        # <<< Character <<<

# >>> Colored SVGs >>>
class Face(Scene):
    def construct(self):
        silhouette = SVGMobject("../../../../assets/svg/excalidraw/person.svg")
        face = SVGMobject("../../../../assets/svg/openMoji/Face-With-Open-Mouth-SkyBlue.svg").shift(UP * 0.52 + RIGHT * 0.065).scale(0.53)
        face2 = SVGMobject("../../../../assets/svg/openMoji/Grinning-Face-SkyBlue.svg").shift(UP * 0.52 + RIGHT * 0.065).scale(0.53)
        self.add(silhouette)
        # self.add(face)
        # self.add(face2)
        self.play(Transform(face, face2), run_time=0.5, rate_func=smooth)
        self.wait(2)
# <<< Colored SVGs <<<
