import sys
import os
import json
import pytest

# Ensure python-utils is in path for testing
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "python-utils"))
from ocr_fixer import OCRFixer

@pytest.fixture
def mock_config(tmp_path):
    config = {
        "global_replacements": {
            "chars": {"ll": "ll", "rn": "m"},
            "punctuation_spacing": True,
            "page_header_patterns": ["^CHAPTER.*", "^PAGE.*"]
        },
        "dictionary": {
            "verified": {"oldword": "newword"},
            "ambiguous": {"test": ["option1", "option2"]},
            "contextual": [
                {"pattern": "fix me", "replacement": "fixed", "reason": "context test"}
            ]
        }
    }
    config_path = tmp_path / "test_config.json"
    config_path.write_text(json.dumps(config), encoding='utf-8')
    return str(config_path)

def test_ocr_fixer_initialization(mock_config):
    fixer = OCRFixer(mock_config)
    assert fixer.data["dictionary"]["verified"]["oldword"] == "newword"

def test_global_replacements(mock_config):
    fixer = OCRFixer(mock_config)
    # Test char replacement (rn -> m)
    assert "com" in fixer.apply_global_replacements("corn")
    # Test punctuation spacing
    assert fixer.apply_global_replacements("word .") == "word."
    assert fixer.apply_global_replacements("word.next") == "word. next"

def test_dehyphenate(mock_config):
    fixer = OCRFixer(mock_config)
    text = "split-\nword"
    # Note: process_text calls dehyphenate
    processed, _ = fixer.process_text(text)
    assert "splitword" in processed

def test_irish_prefix_hyphen_protection(mock_config):
    fixer = OCRFixer(mock_config)
    # n-, t-, h- should NOT be dehyphenated if at start of word
    text = "an n-\noileán"
    processed, _ = fixer.process_text(text)
    assert "n-oileán" in processed

def test_stray_caps_fix(mock_config):
    fixer = OCRFixer(mock_config)
    assert fixer.apply_stray_caps_fix("sentence with A capital") == "sentence with a capital"
    # Irish prefix protection: tUisce should stay tUisce (but the rule might lower the rest)
    # Actually the rule lowers the group(3). tUIsce -> tUisce
    assert fixer.apply_stray_caps_fix("an tUIsce") == "an tUisce"

def test_ambiguous_pattern_detection(mock_config):
    fixer = OCRFixer(mock_config)
    text = "This is a test case."
    _, patterns = fixer.process_text(text)
    # 'test' is in ambiguous dict
    assert any(p['word'] == 'test' for p in patterns)

def test_visual_noise_fixer(mock_config):
    fixer = OCRFixer(mock_config)
    # Ponc detaching cases
    assert fixer.visual_noise_fixer("b.uaileadh") == "ḃuaileadh"
    assert fixer.visual_noise_fixer("C'iandracán") == "Ċiandracán"
    
def test_tironian_et(mock_config):
    fixer = OCRFixer(mock_config)
    assert fixer.normalize_tironian_et("bhaile 7 abhaile") == "bhaile agus abhaile"

def test_vowel_harmony_checker(mock_config):
    fixer = OCRFixer(mock_config)
    # Correct harmony across consonants
    assert fixer.vowel_harmony_checker("cailín") == True # ai -> broad, í -> slender
    assert fixer.vowel_harmony_checker("ciandracán") == True 
    assert fixer.vowel_harmony_checker("fílan") == False # Slender (í) -> Consonant(l) -> Broad (a) = violation!
