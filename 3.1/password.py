def isValidPassword(s: str) -> bool:
    # 长度 6-12
    if not (6 <= len(s) <= 12):
        return False
    
    has_digit = any(c.isdigit() for c in s)
    has_alpha = any(c.isalpha() for c in s)

    return has_digit and has_alpha
