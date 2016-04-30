class APIError(Exception):
    def __init__(self, message, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.message = message

    def __repr__(self, *args, **kwargs):
        return super().__str__(*args, **kwargs)

    def __str__(self, *args, **kwargs):
        return self.message
