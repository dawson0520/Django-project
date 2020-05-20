import json

from bson import json_util
from mongoengine import (  # NOQA
    BooleanField,
    DateTimeField,
    DecimalField,
    DictField,
    Document,
    EmbeddedDocument,
    EmbeddedDocumentField,
    IntField,
    ListField,
    QuerySet,
    StringField,
    connect,
    get_db,
)
from src.enums.db import (
    CaseStatusEnum,
    CaseTypeEnum,
    CashierType,
    DoorStatus,
    ShopperStatusEnum,
    ShopperType,
)
from src.settings import MONGO_URI

connect(host=MONGO_URI)
db = get_db()


def queryset_to_json(items):
    return json_util.dumps([o.to_dict() for o in items])


def queryset_to_dict(items):
    return [o.to_dict() for o in items]


def to_dict(o):
    data = o.to_mongo()
    data = {k: v for k, v in data.items()}
    data["id"] = str(data.pop("_id", None))
    return data


def to_json(o):
    return json.dumps(o.to_dict())


QuerySet.to_json = queryset_to_json
QuerySet.to_dict = queryset_to_dict
Document.to_dict = to_dict
Document.to_json = to_json


class CashierModel(Document):
    meta = {"collection": "cashiers"}
    username = StringField(required=True, max_length=100)
    password = StringField(required=True, max_length=100)
    type = IntField(choices=CashierType.choices(), default=CashierType.OUT.value)


class CaseModel(Document):
    meta = {"collection": "cases"}
    store_id = StringField()
    target_id = StringField(required=True, max_length=100, default="")
    event_id = StringField(default="")
    type = StringField(choices=CaseTypeEnum.choices(), required=True)
    status = StringField(
        choices=CaseStatusEnum.choices(),
        required=True,
        default=CaseStatusEnum.pending.value,
    )

    metadata = DictField()
    frames = DictField()
    products = ListField(DictField(), default=list)
    shoppers = ListField(default=list)  # save shopper id
    tickets = ListField(DictField(), default=list)

    cashier = StringField()  # save cashier name
    result = DictField()
    pending_ts = IntField(default=0)
    processing_ts = IntField(default=0)
    finished_ts = IntField(default=0)
    is_void = BooleanField(default=False)

    start_ts = IntField(default=0)
    end_ts = IntField(default=0)
    extend_ts = IntField(default=0)

    cart_list = ListField()
    cache_mock = DictField()


class ShopperCaseModel(Document):
    meta = {"collection": "shopper_case", "indexes": ["target_id", "case_id"]}
    target_id = StringField(default="")
    case_id = StringField(default="")


class GroupCasesModel(Document):
    meta = {"collection": "group_case", "indexes": ["qr_code", "case_id"]}
    qr_code = StringField()
    case_id = StringField()
    is_valid = BooleanField(default=True)


class GroupModel(Document):
    meta = {"collection": "group", "ordering": ["-create_ts"]}
    store_id = StringField(default="")
    door_id = StringField(default="")

    open_id = StringField(required=True, max_length=100)
    qr_code = StringField(required=True, max_length=100)
    origin_qr_code = StringField(default="")

    shoppers = ListField(default=list)
    create_ts = IntField(required=True, default=0)
    uncertain_shoppers = ListField(default=list)
    # all shoppers of the group are in the store
    is_in_store = BooleanField(required=True, default=True)
    is_checkout = BooleanField(required=True, default=False)
    door_status = IntField(choices=DoorStatus.choices(), default=DoorStatus.OPEN.value)
    open_ts = IntField(default=0)
    close_ts = IntField(default=0)


class ShopperModel(Document):
    meta = {"collection": "shoppers"}

    store_id = StringField(required=True, max_length=100)
    image_url = StringField(required=True, max_length=100, default="")
    entry_timestamp = IntField(required=True, default=0)
    exit_timestamp = IntField(required=True, default=0)
    target_id = StringField(required=True, max_length=100)
    origin_target_id = StringField(required=True, max_length=100)
    qr_code = StringField(max_length=100, default="")
    status = IntField(
        choices=ShopperStatusEnum.choices(),
        required=True,
        default=ShopperStatusEnum.IN.value,
    )
    bbox = DictField(default=dict)
    key_points_2d = DictField(default=dict)
    type = IntField(choices=ShopperType.choices(), default=ShopperType.OUT.value)


class OpenDoorModel(Document):
    meta = {"collection": "open_door", "ordering": ["-open_timestamp"]}
    store_id = StringField(required=True, max_length=100)
    door_id = StringField(required=True, max_length=100)
    open_id = StringField(required=True, max_length=100)
    qr_code = StringField(required=True, max_length=100)
    open_timestamp = IntField(required=True)


class DoorModel(Document):
    meta = {"collection": "doors"}
    store_id = StringField(required=True, max_length=100)
    door_id = StringField(required=True, max_length=100)
    door_name = StringField(required=True, max_length=100)


class StoreModel(Document):
    meta = {"collection": "store"}
    store_id = StringField(required=True, max_length=100)
    store_code = StringField(required=True, max_length=100)
    store_name = StringField(required=True, max_length=100)


class ShopperCartModel(Document):
    meta = {"collection": "shopper_cart"}
    target_id = StringField(required=True, max_length=100)
    qr_code = StringField(max_length=100)
    items = ListField(DictField(), default=list)


class Items(EmbeddedDocument):
    item_id = StringField(required=True, max_length=100)
    name = StringField(required=True, max_length=100)
    num = IntField(required=True)
    img = StringField(required=True, max_length=256)
    price = DecimalField(required=True)


class OrderModel(Document):

    meta = {"collection": "orders"}
    store_code = StringField(required=True, max_length=100)
    sno = StringField(required=True, max_length=100)
    open_id = StringField(required=True, max_length=100)
    items_list = ListField(EmbeddedDocumentField(Items), default=list)
    amount = DecimalField()
    # note = StringField(max_length=100)
    # cashier_id = StringField(required=True, max_length=100)
    create_time = DateTimeField()
    update_time = DateTimeField()
    is_correct = BooleanField(default=True)

    def clean(self):
        if not self.items_list and not self.amount:
            self.amount = 0


class CameraModel(Document):
    meta = {"collection": "cameras"}
    cam_id = StringField(required=True, primary_key=True)
    # camera ip address
    address = StringField(required=True)
    # camera type: identify the model of the camera
    cam_type = StringField(required=True)


class GondolaModel(Document):
    meta = {"collection": "gondolas"}
    """
        group key formatter
        {
            "store_id": "",
            "name": ""
        }
    """
    group_key = DictField(required=True, primary_key=True)
    name = StringField(required=True)
    store_id = StringField(required=True)
    layer_num = IntField()
    positions = StringField()
    # [top, left, right]
    cameras = StringField()
    mis_place_items = ListField(default=list)  # save item_id into the field

    def to_dict(self):
        data = super().to_mongo()
        data = {k: v for k, v in data.items()}
        data["id"] = str(data.pop("_id", None)["name"])
        return data

    def to_json(self, *args, **kwargs):
        return json.dumps(self.to_dict())


class ProductModel(Document):
    meta = {"collection": "products"}
    """
        id formatter
        {
            "store_id": "",
            "product_id": ""
        }
    """
    group_key = DictField(required=True, primary_key=True)
    product_id = StringField(required=True)
    store_id = StringField(required=True)
    name = StringField(required=True)
    # thumbnail image
    url = StringField(required=True, default="")
    original_url = StringField(required=True, default="")
    # sale price
    sale_price = DecimalField()
    # retail price
    price = DecimalField(required=True)
    on_sale = IntField(required=True, default=1)
    barcode = StringField()

    def to_dict(self):
        data = super().to_mongo()
        data = {k: v for k, v in data.items()}
        data["id"] = str(data.pop("_id", None)["product_id"])
        return data

    def to_json(self, *args, **kwargs):
        return json.dumps(self.to_dict())


class SystemConfigModel(Document):
    meta = {"collection": "system_config"}
    name = StringField(required=True, primary_key=True)
    content = StringField(default="")


class FrameViewsModel(Document):
    meta = {"collection": "frame_views"}
    case_id = StringField(default="")
    event_id = StringField(default="")
    data = ListField(default=list)


class MockHistoryModel(Document):
    meta = {"collection": "mock_history"}
    case_id = StringField(required=True)
    cashier = StringField(required=True)
    start_ts = IntField(required=True)
    end_ts = IntField(required=True)
    duration = IntField(required=True)
    is_correct = BooleanField(required=True)
    cart_list = ListField()


class OperatorFeedbackModel(Document):
    meta = {"colleciton": "operator_feedback"}
    comment = StringField(default="")
    cashier = StringField(required=True)
    create_ts = IntField(required=True)

