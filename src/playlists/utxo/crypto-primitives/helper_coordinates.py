from manim import *
from utils import PEOPLE

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

        if expr == "Smiling-Face-With-Horns":
            position_offset = UP * 0.58 + RIGHT * 0.068
            scale_offset = 0.55
        else:
            position_offset = UP * 0.52 + RIGHT * 0.068
            scale_offset = 0.53


        if name is not None:
            color = PEOPLE[name]["color"]
            faceColor = PEOPLE[name]["faceColor"]

            # Option to show emotion
            face_path = f"../../../../assets/svg/openMoji/{expr}-{faceColor}.svg"
            face = SVGMobject(face_path).shift(self.c + position_offset).scale(scale_offset)
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

# >>> Mix Latex and normal text >>>
# class TextLatex(VGroup):
#     def __init__(
#         self,
#         txt: str,
#         custom_font: str ="Excalifont",
#         **kwargs,
#     ):
# <<< Mix Latex and normal text <<<
    
# >>> Add elements to sets >>>
def addPointsToSet(
    mob,
    noise=0.1, 
    n_elements=10,
    height_span=None,
    labels=None,
    **kwargs
):
    # random Generator variable
    rng = np.random.default_rng(seed=43)

    if height_span is None:
        height_span = (mob.height / 2) * 0.75

    if "stroke_width" not in kwargs:
        strk_w = 1.5
    else:
        strk_w = kwargs["stroke_width"]

    dots_w_labels = []
    if labels is not None:
        n_elements = len(labels)
        mat = np.round(rng.normal(size=(n_elements, 2)) *  noise, 2)
        mat[:,0] += height_span * np.linspace(-1, 1, n_elements)
        dots = [Dot(color=kwargs["color"], stroke_color=XTXT, stroke_width=strk_w).move_to(mob.get_center() + DOWN * i[0] + RIGHT * i[1]) for i in mat]
        for i, dot in enumerate(dots):
            if labels[i] == "...":
                dots[i].set_opacity(0.0)
                dots_w_labels.append(VGroup(
                    MathTex("\\vdots", color=XTXT, font_size=42).move_to(dot),
                    MathTex("")
                ))
            else:
                dots_w_labels.append(VGroup(
                    dot, 
                    MathTex(labels[i], color=XTXT, font_size=32).next_to(dot, kwargs["label_position"])
                ))
        return dots_w_labels

    mat = np.round(rng.normal(size=(n_elements, 2)) *  noise, 2)
    mat[:,0] += height_span * np.linspace(-1, 1, n_elements)
    dots = [Dot(color=kwargs["color"], stroke_width=kwargs["stroke_width"]).move_to(mob.get_center() + DOWN * i[0] + RIGHT * i[1]) for i in mat]
    return dots
# <<< Add elements to sets <<<
