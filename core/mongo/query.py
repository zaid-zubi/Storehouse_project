from collections import OrderedDict


class BaseMongoQuery:
    """
    A class to convert query params to a mongo `match` dict
    """

    def dict(self):
        """
        get provided query params as dict
        """
        exclude = ['page', 'page_size']
        exclude += self.Config.exclude

        return {k: v for k, v in self.__dict__.items() if v is not None and (k not in exclude)}

    @staticmethod
    def is_special(k):
        """
        whether this query_param should be handled using a special__{} method
        """
        return '__' in k

    def special__in(self, k, v):
        """
        handler for the __in special query
        """
        normal_key, _ = k.split('__')

        return tuple((normal_key, {'$in': v}))

    def special__all(self, k, v):
        """
        handler for the __all special query
        """
        normal_key, _ = k.split('__')

        return tuple((normal_key, {'$all': v}))

    def prepare_match(self) -> list:
        """
        prepare array for the match OrderedDict
        """
        data = self.dict()
        match = []
        for k, v in [(k, v) for (k, v) in data.items() if not self.is_special(k)]:
            # normal query_params
            match.append((k, v))

        for k, v in [(k, v) for (k, v) in data.items() if self.is_special(k)]:
            # special query params
            type_ = k.split('__')[1]
            match.append(getattr(self, f'special__{type_}')(k, v))

        return match

    def make_match(self) -> OrderedDict:
        return OrderedDict(self.prepare_match())

    class Config:
        exclude = []
