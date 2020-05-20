from enum import Enum, IntEnum


class CaseStatusEnum(Enum):
    pending = "pending"
    processing = "processing"
    finished = "finished"
    error = "error"

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class ShopperStatusEnum(IntEnum):
    IN = 1
    OUT = 2
    UNKNOWN = 3

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class CaseTypeEnum(Enum):
    item_recognition = "item_recognition"
    shopper_association = "shopper_association"
    item_binding = "item_binding"
    shopper_binding = "shopper_binding"
    shopper_swapping = "shopper_swapping"
    full_time_tracking = "full_time_tracking"
    exit_mis_shopper = "exit_mis_shopper"
    shopper_cart = "shopper_cart"

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class DoorStatus(IntEnum):
    OPEN = 1
    CLOSE = 2

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class ItemAction(IntEnum):
    """
    items action
    """

    UP = 1
    DOWN = 2

    @classmethod
    def all(cls):
        return [key.value for key in cls]


class CashierType(IntEnum):
    """
    cashier type
    """

    INNER = 1
    OUT = 2

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class ShopperType(IntEnum):
    """shopper type"""

    INNER = 1
    OUT = 2

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

