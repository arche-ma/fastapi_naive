from dataclasses import asdict


class GenericInput:
    def to_dict(self):
        return {
            key: value
            for key, value in asdict(self).items()
            if value is not None
        }

    def __post_init__(self):
        self.validate()

    @classmethod
    def _valid_methods(cls):
        validate_methods = [
            getattr(cls, method)
            for method in dir(cls)
            if "validate_" in method
        ]
        return validate_methods

    def validate(self):
        methods = self._valid_methods()
        print(methods)
        for method in methods:
            method(self)
