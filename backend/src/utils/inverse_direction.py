from backend.src.types.direction import Direction


def inverse_direction(direction: Direction) -> Direction:
    match direction:
        case "up":
            return "down"
        case "down":
            return "up"
        case "left":
            return "right"
        case "right":
            return "left"
