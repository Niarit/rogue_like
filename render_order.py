from enum import auto, Enum


class RenderOrder(Enum):
    CORPSE = auto()
    ITEM = auto()
    ACTOR = auto()

# auto assigns incrementing integer values automatically,
# so we don’t need to retype them if we add more values later on.
# This means Corpse will have a smaller value than ITEM and ITEM will have a smaller value than ACTOR
