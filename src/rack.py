#Rack class for managing available letters, which includes blank tiles (represented by a '.').
class Rack:
    def __init__(self, letters):
        self.letters = self.build_rack(letters)
          
    def build_rack(self, letters) -> dict:
        """Validates letters and accounts for blanks."""
        rack = {"letters": {}, "blanks": 0}
        for char in letters:
            char = char.lower()
            if char != '.' and not char.isalpha():
                raise ValueError(f"Invalid character '{char}' in rack. Only letters and '.' are allowed.")
            if char == '.':
                rack['blanks'] += 1
            else:
                rack['letters'][char] = rack['letters'].get(char, 0) + 1
        return rack
    
    def use_letter(self, char) -> set:
        """Attempts to use a rack letter. If empty, checks for blanks.
        Returns a set:
        (True, 'char') if regular tile,
        (True, 'blank') if blank tile.
        (False, None) if neither available."""
        if not char.isalpha():
            raise ValueError(f"Using invalid character '{char}'. Only letters are allowed.")
        char = char.lower()
        if char in self.letters['letters'] and self.letters['letters'][char] > 0:
            self.letters['letters'][char] -= 1
            return (True, 'char')
        elif self.letters['blanks'] > 0:
            self.letters['blanks'] -= 1
            return (True, 'blank')
        return (False, None)
