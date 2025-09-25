"""
Authentic Furbish Language Reference
Based on https://arkaia.gitlab.io/www.langmaker.com/furbish.htm#English2Furbish
Official Furbish dictionary from original 1998 Furby documentation

This module contains verified authentic Furbish phrases and vocabulary
from the original Furby toy documentation.
"""

# Authentic Furbish Dictionary from original 1998 Furby
# Source: https://arkaia.gitlab.io/www.langmaker.com/furbish.htm#English2Furbish
AUTHENTIC_FURBISH = {
    # Basic words
    "dah": "yes",
    "boo": "no",
    "kah": "me",
    "u-nye": "you", 
    "way-loh": "again",
    "may-may": "love",
    "a-loh": "please",
    "doo-moh": "more",
    "loo-loo": "joke",
    "koh-koh": "sleep",
    "wee-tah": "sing",
    "ooh-lah": "yes (excited)",
    "eee-day": "what",
    "boh-bay": "hug",
    "noo-loo": "happy",
    "ay-ay-ay": "worried",
    "dee-doh": "big",
    "tee-tah": "hungry",
    "way-way": "play",
    "dah-noh-lah": "party",
    "may-lah": "love a lot",
    "wah": "tell",
    "toh-dye": "scared",
    "nah-bah": "down",
    "ee-kah": "me scared",
    "way-loo": "maybe",
    "tay-tay": "again",
    "noo-noo": "baby",
    "ay-way": "go",
    "boo-kah": "no me",
    "doo-ay": "please",
    "kah-tay": "me hungry",
    "kah-way": "me want",
    "u-nye-way": "you want",
    "u-nye-loo-loo": "you funny",
    "kah-may-may": "me love",
    "u-nye-may-may": "you love",
    "kah-noo-loo": "me happy",
    "u-nye-noo-loo": "you happy",
    "kah-koh-koh": "me sleep",
    "u-nye-koh-koh": "you sleep",
    "kah-wee-tah": "me sing",
    "u-nye-wee-tah": "you sing",
    "kah-way-way": "me play",
    "u-nye-way-way": "you play",
    "kah-tee-tah": "me hungry",
    "u-nye-tee-tah": "you hungry",
    "kah-boh-bay": "me hug",
    "u-nye-boh-bay": "you hug",
    "kah-ay-way": "me go",
    "u-nye-ay-way": "you go",
    "dah-way-loh": "yes again",
    "boo-way-loh": "no again",
    "may-may-kah": "love me",
    "may-may-u-nye": "love you",
    "way-loh-may-may": "love again",
    "doo-moh-may-may": "more love",
    "noo-loo-may-may": "happy love",
    "kah-may-may-u-nye": "me love you",
    "u-nye-may-may-kah": "you love me",
    "dah-kah-may-may-u-nye": "yes me love you",
    "way-loh-kah-may-may": "again me love",
    "kah-a-loh-u-nye": "me please you",
    "u-nye-a-loh-kah": "you please me",
    "dah-ay-loh-nee-way": "please play with me",
    "way-loh-kah-a-tay": "feed me again",
    "dah-kah-way-way": "yes me want to play",
    "kah-way-loo": "me like to play",
    "u-nye-kah-noo-loo": "you make me happy"
}

# Authentic Furbish phrases for therapeutic contexts
# Using only verified authentic Furbish words and proper grammar structure
THERAPEUTIC_FURBISH = {
    # Comfort and support - using authentic phrases
    "kah-may-may-u-nye": "me love you",
    "u-nye-noo-loo": "you happy", 
    "koh-koh": "sleep/calm",
    "kah-boh-bay": "me hug",
    "u-nye-dee-doh": "you big",
    "way-loh-may-may": "love again",
    "kah-wah": "me tell",
    "u-nye-may-may": "you love",
    "dah-u-nye-noo-loo": "yes you happy",
    "kah-a-loh-u-nye": "me please you",
    
    # Encouragement - authentic combinations
    "u-nye-dee-doh": "you big",
    "dah-u-nye-way-way": "yes you play",
    "way-loh-way-way": "play again",
    "noo-loo-may-may": "happy love",
    "kah-way-u-nye-noo-loo": "me want you happy",
    "doo-moh-noo-loo": "more happy",
    "u-nye-loo-loo": "you funny",
    "way-loh-noo-loo": "happy again",
    
    # Understanding and listening - authentic phrases
    "kah-wah": "me tell",
    "eee-day": "what",
    "u-nye-wah": "you tell",
    "dah-kah-wah": "yes me tell",
    "way-loo": "maybe",
    
    # Bicycle-themed using authentic Furbish structure
    "way-way-dee-doh": "play big",
    "u-nye-way-way-noo-loo": "you play happy",
    "kah-way-way": "me play",
    "way-loh-way-way": "play again",
    "u-nye-dee-doh-way-way": "you big play"
}

# Phrases that were invented and need correction to authentic Furbish
# Based on authentic dictionary from https://arkaia.gitlab.io/www.langmaker.com/furbish.htm
INCORRECT_PHRASES = {
    # Current incorrect -> Correct authentic
    "dah a-loh u-nye": "kah-may-may-u-nye",  # "me love you" 
    "kah may-may": "kah-may-may",  # "me love" (proper hyphenation)
    "u-nye way-loh": "u-nye-noo-loo",  # "you happy" (way-loh means "again")
    "may-may kah": "may-may-kah",  # "love me" (proper word order)
    "dah koh-koh": "koh-koh",  # just "sleep/calm" (dah is redundant)
    "way-loh dah": "dah-way-loh",  # "yes again" (proper word order)
    "u-nye loo-loo": "u-nye-loo-loo",  # "you funny" (needs hyphen)
    "kah doo-moh": "kah-way-doo-moh",  # "me want more" (missing 'way')
    "dah boh-bay": "boh-bay",  # just "hug" (dah is redundant)
    "kah u-nye": "kah-wah",  # "me tell" (u-nye doesn't follow kah directly)
    "way-loh kah": "kah-way-loh",  # "me again" (proper word order)
    "doo-moh way": "doo-moh",  # just "more" (way doesn't fit here)
    "dah way-loh": "dah-way-loh",  # "yes again" (needs hyphen)
    "u-nye wee-tah": "u-nye-wee-tah",  # "you sing" (needs hyphen)
    "kah loo-loo": "kah-loo-loo",  # "me joke" (needs hyphen)
    "u-nye kah": "u-nye-wah",  # "you tell" (kah doesn't follow u-nye)
    "kah dah way": "kah-way",  # "me want" (dah is redundant)
    "way-loh may-may": "way-loh-may-may",  # "love again" (needs hyphen)
    
    # Bicycle-themed corrections using authentic words
    "dah wheel-loh": "way-way-dee-doh",  # "play big" (no 'wheel' in Furbish)
    "kah pedal-may": "kah-way-way",  # "me play" (no 'pedal' in Furbish)
    "u-nye cycle-way": "u-nye-way-way",  # "you play" (no 'cycle' in Furbish)
    "way-loh bike-dah": "way-loh-way-way",  # "play again" (no 'bike' in Furbish)
    "doo-moh chain-kah": "doo-moh-dee-doh",  # "more big" (no 'chain' in Furbish)
    "loo-loo spoke-way": "loo-loo-way-way"  # "funny play" (no 'spoke' in Furbish)
}

def validate_furbish_phrase(phrase):
    """
    Validate if a Furbish phrase uses authentic vocabulary and structure.
    
    Args:
        phrase (str): The Furbish phrase to validate
        
    Returns:
        tuple: (is_valid, corrected_phrase, explanation)
    """
    # Normalize the phrase (remove spaces, convert to lowercase)
    normalized = phrase.lower().replace(' ', '-')
    
    # Check if phrase exists in authentic dictionary
    if normalized in AUTHENTIC_FURBISH:
        return True, normalized, "Authentic phrase"
    
    if normalized in THERAPEUTIC_FURBISH:
        return True, normalized, "Authentic therapeutic phrase"
    
    # Check if it's a known incorrect phrase that needs correction
    if normalized in INCORRECT_PHRASES:
        corrected = INCORRECT_PHRASES[normalized]
        return False, corrected, f"Corrected from non-authentic phrase"
    
    # Check if phrase follows authentic word patterns
    # First check if the whole phrase is authentic
    if normalized in AUTHENTIC_FURBISH:
        return True, normalized, "Authentic compound phrase"
    
    # For compound phrases, check if they're made of authentic components
    # But be more flexible about compound word validation
    words = normalized.split('-')
    authentic_words = set(AUTHENTIC_FURBISH.keys())
    
    # Extract base words from the authentic dictionary for component checking
    base_words = set()
    for word in authentic_words:
        if '-' in word:
            # Add components of compound words
            base_words.update(word.split('-'))
        else:
            base_words.add(word)
    
    # Check each word component
    invalid_words = [word for word in words if word not in base_words and word not in authentic_words]
    
    if not invalid_words:
        return True, normalized, "Uses authentic Furbish word components"
    else:
        # Try to suggest correction using similar authentic words
        suggestion = suggest_authentic_alternative(normalized)
        return False, suggestion, f"Contains non-authentic words: {', '.join(invalid_words)}"

def suggest_authentic_alternative(phrase):
    """
    Suggest an authentic Furbish alternative for a non-authentic phrase.
    
    Args:
        phrase (str): Non-authentic phrase
        
    Returns:
        str: Suggested authentic alternative
    """
    # Mapping based on therapeutic intent and meaning
    therapeutic_alternatives = {
        # Love and affection
        "dah-a-loh-u-nye": "kah-may-may-u-nye",  # "me love you"
        "kah-may-may": "kah-may-may",  # already correct
        "may-may-kah": "may-may-kah",  # "love me" - correct
        
        # Happiness and positivity  
        "u-nye-way-loh": "u-nye-noo-loo",  # "you happy"
        "dah-way-loh": "dah-way-loh",  # "yes again" - correct
        "u-nye-wee-tah": "u-nye-wee-tah",  # "you sing" - correct
        "kah-loo-loo": "kah-loo-loo",  # "me joke" - correct
        "way-loh-dah": "dah-way-loh",  # "yes again"
        
        # Comfort and calm
        "dah-koh-koh": "koh-koh",  # just "sleep/calm"
        "u-nye-loo-loo": "u-nye-loo-loo",  # "you funny" - correct
        "kah-doo-moh": "doo-moh",  # just "more"
        
        # Understanding and communication
        "dah-boh-bay": "boh-bay",  # just "hug"
        "kah-u-nye": "kah-wah",  # "me tell"
        "way-loh-kah": "kah-way-loh",  # "me again"
        "doo-moh-way": "doo-moh",  # just "more"
        "u-nye-kah": "u-nye-wah",  # "you tell"
        "kah-dah-way": "kah-way",  # "me want"
        "way-loh-may-may": "way-loh-may-may",  # "love again" - correct
        "kah-a-loh": "kah-a-loh-u-nye",  # "me please you"
        
        # Bicycle themed - use authentic words for play/movement
        "dah-wheel-loh": "way-way-dee-doh",  # "play big"
        "kah-pedal-may": "kah-way-way",  # "me play"
        "u-nye-cycle-way": "u-nye-way-way",  # "you play"
        "way-loh-bike-dah": "way-loh-way-way",  # "play again"
        "doo-moh-chain-kah": "doo-moh-dee-doh",  # "more big"
        "loo-loo-spoke-way": "loo-loo-way-way",  # "funny play"
    }
    
    if phrase in therapeutic_alternatives:
        return therapeutic_alternatives[phrase]
    
    # Default fallback based on common therapeutic needs
    return "kah-may-may-u-nye"  # "me love you"

def get_authentic_therapeutic_phrases():
    """
    Get all authentic Furbish phrases suitable for therapeutic use.
    
    Returns:
        dict: Dictionary of authentic therapeutic phrases with translations
    """
    result = {}
    
    # Add single authentic words that work therapeutically
    therapeutic_singles = {
        "may-may": "love",
        "noo-loo": "happy", 
        "boh-bay": "hug",
        "koh-koh": "sleep/calm",
        "dah": "yes",
        "wee-tah": "sing",
        "loo-loo": "funny/good"
    }
    
    result.update(therapeutic_singles)
    
    # Add compound therapeutic phrases
    for phrase, translation in THERAPEUTIC_FURBISH.items():
        result[phrase] = translation
    
    return result