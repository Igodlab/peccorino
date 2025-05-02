from manim import * 

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
