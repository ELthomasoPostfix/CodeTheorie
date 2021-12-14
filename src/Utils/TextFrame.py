class TextFrame:
    def __init__(self, text: str):
        self.text = text

    def __len__(self):
        return len(self.text)