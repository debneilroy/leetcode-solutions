class MaxConsecutiveChars:
    def find_max_consecutive(self, text):
        if not text:
            return []

        max_length = 0
        result = []
        i = 0
        while i < len(text):
            char = text[i]
            if char.isspace():
                i += 1
                continue

            length = 1
            while i + 1 < len(text) and text[i + 1] == char:
                length += 1
                i += 1

            if length > max_length:
                max_length = length
                result = [char]
            elif length == max_length:
                result.append(char)

            i += 1

        return result
