from turtle import fillcolor
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

# >>> get center for label emoji >>>
def centerLabel(obj: ImageMobject):
    # select font size to 18 for a label of size 0.5
    return obj.get_center() + DOWN * 0.2 + RIGHT * 0.2
# <<< get center for label emoji <<<


# >>> Coordinate Helper Utility >>>
class CoordinateHelper:
    @staticmethod
    def show_coordinates(
        mobject,
        scene,
        show_points=True,
        show_bounding_box=True,
        show_center=True,
        point_radius=0.05,
        label_scale=0.2,
        color=XNEON_RED
    ):
        
        """
        Visualize the coordinates of a mobject by displaying:
        - Points of the mobject (if applicable)
        - Bounding box with coordinates
        - Center point
        
        Parameters:
        mobject: The mobject to show coordinates for
        scene: The scene to add visualization to
        show_points: Whether to show the points of the mobject
        show_bounding_box: Whether to show the bounding box
        show_center: Whether to show the center point
        point_radius: Radius of the visualization dots
        label_scale: Scale of the coordinate labels
        """
        visualization_group = VGroup()
        
        # Show center dot and coordinates
        if show_center:
            center = mobject.get_center()
            center_dot = Dot(center, color=color, radius=point_radius)
            center_label_txt = f"({center[0]:.2f}, {center[1]:.2f})"
            center_label = Text(
                center_label_txt,
                color=color
            ).scale(label_scale)
            center_label.next_to(center_dot, DOWN, buff=0.1)
            visualization_group.add(center_dot, center_label)
        
        # Show bounding box with corner coordinates
        if show_bounding_box:
            # Get corners
            ul = mobject.get_corner(UL)
            ur = mobject.get_corner(UR)
            dl = mobject.get_corner(DL)
            dr = mobject.get_corner(DR)
            
            # Create bounding box
            box = Polygon(ul, ur, dr, dl, color=color, stroke_width=1)
            
            # Add corner dots and labels
            corners = [(ul, "UL"), (ur, "UR"), (dl, "DL"), (dr, "DR")]
            for corner, name in corners:
                corner_dot = Dot(corner, color=color, radius=point_radius)
                coord_text = f"({corner[0]:.2f}, {corner[1]:.2f})"
                corner_label = Text(coord_text, color=color).scale(label_scale)
                
                # Position labels to avoid overlapping with the mobject
                if "U" in name:
                    corner_label.next_to(corner_dot, UP, buff=0.1)
                else:
                    corner_label.next_to(corner_dot, DOWN, buff=0.1)
                
                visualization_group.add(corner_dot, corner_label, box)
        
        # Show points if applicable and requested
        if show_points and hasattr(mobject, "get_points") and len(mobject.get_points()) > 0:
            points = mobject.get_points()
            
            # If there are too many points, sample a reasonable number
            max_points = 10
            if len(points) > max_points:
                indices = np.linspace(0, len(points) - 1, max_points, dtype=int)
                points = points[indices]
            
            for i, point in enumerate(points):
                point_dot = Dot(point, color=RED, radius=point_radius)
                point_label_txt = f"p{i}: ({point[0]:.2f}, {point[1]:.2f})"
                point_label = Text(
                    point_label_txt, 
                    color=color
                ).scale(label_scale * 0.8)
                point_label.next_to(point_dot, RIGHT, buff=0.1)
                visualization_group.add(point_dot, point_label)
        
        visualization_group.set_z_index(100)
        scene.add(visualization_group)
        return visualization_group
# <<< Coordinate Helper Utility <<<


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

        svg_path = "svg/excalidraw/person-w.svg"
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
            face_path = f"./svg/openMoji/{expr}-{faceColor}.svg"
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
class HashLabel(Group):
    def __init__(
        self,
        txt: str | None = None,
        **kwargs
    ):
        lbl_svg_ = SVGMobject("./svg/excalidraw/label.svg")

        if txt == None:
            self.add(lbl_txt_)

        lbl_txt_ = 

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
        silhouette = SVGMobject("svg/excalidraw/person.svg")
        face = SVGMobject("./svg/openMoji/Face-With-Open-Mouth-SkyBlue.svg").shift(UP * 0.52 + RIGHT * 0.065).scale(0.53)
        face2 = SVGMobject("./svg/openMoji/Grinning-Face-SkyBlue.svg").shift(UP * 0.52 + RIGHT * 0.065).scale(0.53)
        self.add(silhouette)
        # self.add(face)
        # self.add(face2)
        self.play(Transform(face, face2), run_time=0.5, rate_func=smooth)
        self.wait(2)
# <<< Colored SVGs <<<
