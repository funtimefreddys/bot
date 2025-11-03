# bad_words.py - Bad Words / Profanity Filter
# รองรับทั้งภาษาไทยและอังกฤษ

# Bad words list - Thai
BAD_WORDS_TH = [
    # คำหยาบคายภาษาไทย
    'โง่', 'บ้า', 'ควาย', 'มึง', 'กู', 'เย็ด', 'กระหรี่', 'เยอ',
    'เหี้ย', 'สัส', 'เฮี่ย', 'สาส', 'มึง', 'กู', 'มรึง',
    'มรึง', 'ควาย', 'โง่', 'โง่เง่า', 'บัดซบ', 'กระหรี่',
    # เพิ่มคำหยาบคายอื่นๆ ตามต้องการ
]

# Bad words list - English
BAD_WORDS_EN = [
    # English profanity
    'fuck', 'shit', 'damn', 'bitch', 'ass', 'bastard', 'idiot',
    'stupid', 'dumb', 'hell', 'crap', 'piss', 'cock', 'dick',
    'damn', 'bastard', 'motherfucker', 'fucker', 'asshole',
    'whore', 'slut', 'cunt', 'pussy', 'nigga', 'nigger',
    # Add more as needed
]

# Combined list for checking
BAD_WORDS_ALL = list(set(BAD_WORDS_TH + BAD_WORDS_EN))

def get_bad_words(language: str = 'en') -> list:
    """Get bad words list for specific language"""
    if language == 'th':
        return BAD_WORDS_TH
    elif language == 'en':
        return BAD_WORDS_EN
    return BAD_WORDS_ALL

def check_bad_words(text: str, language: str = 'en') -> tuple[bool, list[str]]:
    """
    Check if text contains bad words
    
    Returns:
        (contains_bad_words: bool, found_words: list[str])
    """
    text_lower = text.lower()
    bad_words = get_bad_words(language)
    found_words = []
    
    for word in bad_words:
        if word.lower() in text_lower:
            found_words.append(word)
    
    return len(found_words) > 0, found_words

def add_bad_word(word: str, language: str = 'en'):
    """Add a bad word to the list"""
    global BAD_WORDS_TH, BAD_WORDS_EN, BAD_WORDS_ALL
    
    word = word.strip().lower()
    if not word:
        return False
    
    if language == 'th':
        if word not in BAD_WORDS_TH:
            BAD_WORDS_TH.append(word)
            BAD_WORDS_ALL = list(set(BAD_WORDS_TH + BAD_WORDS_EN))
            return True
    elif language == 'en':
        if word not in BAD_WORDS_EN:
            BAD_WORDS_EN.append(word)
            BAD_WORDS_ALL = list(set(BAD_WORDS_TH + BAD_WORDS_EN))
            return True
    
    return False

def remove_bad_word(word: str, language: str = 'en'):
    """Remove a bad word from the list"""
    global BAD_WORDS_TH, BAD_WORDS_EN, BAD_WORDS_ALL
    
    word = word.strip().lower()
    if not word:
        return False
    
    if language == 'th':
        if word in BAD_WORDS_TH:
            BAD_WORDS_TH.remove(word)
            BAD_WORDS_ALL = list(set(BAD_WORDS_TH + BAD_WORDS_EN))
            return True
    elif language == 'en':
        if word in BAD_WORDS_EN:
            BAD_WORDS_EN.remove(word)
            BAD_WORDS_ALL = list(set(BAD_WORDS_TH + BAD_WORDS_EN))
            return True
    
    return False

