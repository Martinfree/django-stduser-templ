from django.core.exceptions import ValidationError

class SymbolPasswordValidator:
    def validate(self, password, user=None):
        massive =("!@#$%<>^~=-&*()_+")
        for symbol in massive:
            for letter in password:
                if letter is symbol:
                    return None
        
        raise ValidationError("Password must contain at least one symbol")

class CharPasswordValidator:
    def validate(self, password, user=None):
        for letter in password:
            if letter.isdigit():
                return None
        
        raise ValidationError("Password must contain at leat one numeric symbol")

class UpPasswordValidator:
    def validate(self, password, user=None):
        for letter in password:
            if letter == letter.capitalize():
                return None
        
        raise ValidationError("Password must contain at least one uppercase letter")

class LowPasswordValidator:
    def validate(self,password,user=None):
        massive =("!@#$%<>^~=-&*()_+")
        
        for letter in password:
            for symbol in massive:
                if letter == letter.lower() and not letter.isdigit() and letter is not symbol:
                    return None

        raise ValidationError("Password must contain at least one lowercase letter")
