#Rack class for managing available letters, which includes blank tiles (represented by a '.').
class Rack:
    def __init__(self):
        self.letters = {}
          
    def fill_rack(self, letters) -> None:
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
        self.letters = rack
    
    def fill_rack_from_input(self) -> None:
        """Fills rack from user input."""
        while True:
            print("Please enter the tiles on your rack. Represent blanks with a period: ")
            letters = input().strip().lower()
            if len(letters) > 7:
                print("Rack cannot exceed 7 tiles. Please try again.")
                continue
            for char in letters:
                if char != '.' and not char.isalpha():
                    print("At least one tile entered incorrectly. Letters and periods only please.")
                    break
            else:
                break
        self.fill_rack(letters)
    

    def use_letter(self, char) -> set:
        """Attempts to use a rack letter. If empty, checks for blanks.
        Returns a set:
        (True, False) if regular tile,
        (True, True) if blank tile.
        (False, False) if neither available."""
        if not char.isalpha():
            raise ValueError(f"Using invalid character '{char}'. Only letters are allowed.")
        char = char.lower()
        if char in self.letters['letters'] and self.letters['letters'][char] > 0:
            self.letters['letters'][char] -= 1
            return (True, False)
        elif self.letters['blanks'] > 0:
            self.letters['blanks'] -= 1
            return (True, True)
        return (False, False)
    
    def restore_letter(self, char, is_blank) -> None:
        """Restores a letter to the rack after backtracking.
        If is_blank is True, restores a blank tile. Otherwise restores the specific character."""
        if is_blank:
            self.letters['blanks'] += 1
        else:
            char = char.lower()
            if char in self.letters['letters']:
                self.letters['letters'][char] += 1
            else:
                self.letters['letters'][char] = 1
