class ScrappingPNGError(Exception):
    def __init__(self, **errors):
        self.message = "Something went wrong while taking screenshot"
        if errors:
            self.message += f": {errors}"
        super().__init__(self.message)


class ScrappingHTMLError(Exception):
    def __init__(self, **errors):
        self.message = "Something went wrong while taking HTML snapshot"
        if errors:
            self.message += f": {errors}"
        super().__init__(self.message)
