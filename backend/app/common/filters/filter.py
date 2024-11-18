class BaseFilter:
    def __init__(
        self,
        field_name: str | None = None,
        lookup_expr: str | None = None,
        method: str | None = None,
        **kwargs,
    ):
        if lookup_expr is None:
            lookup_expr = "__eq__"
        self.field_name = field_name
        self.lookup_expr = lookup_expr
        self.method = method
        self.extra = kwargs
        self.extra.setdefault("required", False)

class BaseInFilter:
    def __init__(
        self,
        field_name: str | None = None,
        lookup_expr: str | None = None,
        method: str | None = None,
        **kwargs,
    ):
        if lookup_expr is None:
            lookup_expr = "in_"
        self.field_name = field_name
        self.lookup_expr = lookup_expr
        self.method = method
        self.extra = kwargs
        self.extra.setdefault("required", False)


class BaseRangeFilter:
    """TODO: _max и _min надо сделать."""

    def __init__(
        self,
        field_name: str | None = None,
        lookup_expr: str | None = None,
        method: str | None = None,
        **kwargs,
    ):
        if lookup_expr is None:
            lookup_expr = "range_"
        self.field_name = field_name
        self.lookup_expr = lookup_expr
        self.method = method
        self.extra = kwargs
        self.extra.setdefault("required", False)



class IntegerFilter(BaseFilter): ...


class IntegerInFilter(BaseFilter): ...


class RangeFilter(BaseRangeFilter): ...


class CharFilter(BaseFilter): ...


class CharInFilter(BaseInFilter): ...


class BooleanFilter(BaseFilter): ...


class BaseRelationshipFilter:
    def __init__(
        self,
        field_name: str | None = None,
        lookup_expr: str | None = None,
        method: str | None = None,
        **kwargs,
    ):
        if field_name is None:
            raise AttributeError
        if lookup_expr is None:
            lookup_expr = "__eq__"
        self.field_name = field_name
        self.lookup_expr = lookup_expr
        self.method = method
        self.extra = kwargs
        self.extra.setdefault("required", False)


class RelationshipFilter(BaseRelationshipFilter): ...
