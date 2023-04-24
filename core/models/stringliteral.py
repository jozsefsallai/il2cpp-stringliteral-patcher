class StringLiteral:
    index: int
    value: str

    def __init__(self, index: int, value: str):
        self.index = index
        self.value = value

    def to_dict(self):
        return {
            'index': self.index,
            'value': self.value
        }

    @staticmethod
    def from_dict(d: dict):
        if 'index' not in d or 'value' not in d:
            raise Exception('Invalid StringLiteral object')

        return StringLiteral(d['index'], d['value'])
