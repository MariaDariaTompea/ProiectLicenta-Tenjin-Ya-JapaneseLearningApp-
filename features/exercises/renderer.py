"""
Renderer functions for different test types.
Returns HTML and data for each question card.
"""
import json

def get_test_data(test):
    """Parse JSON options and return a clean data object (list or dict)."""
    if not test.options:
        return {}
    try:
        data = json.loads(test.options)
        return data
    except:
        return {}

def render_multiple_choice(test):
    options = get_test_data(test)
    if not isinstance(options, list):
        options = []
    return f"""
    <div class="test-content multiple-choice">
        <p class="question-text">{test.question}</p>
        <div class="options-grid">
            {" ".join([f'<button class="option-btn" data-value="{opt}">{opt}</button>' for opt in options])}
        </div>
    </div>
    """

def render_fill_blank(test):
    data = get_test_data(test)
    if not isinstance(data, dict):
        data = {}
    sentence = data.get("sentence", test.question) or ""
    choices = data.get("choices", [])
    
    # Replace ___ with an empty span for the blank
    sentence_html = sentence.replace("___", '<span class="blank"></span>')
    
    return f"""
    <div class="test-content fill-blank">
        <p class="question-text">{sentence_html}</p>
        <div class="choices-grid">
            {" ".join([f'<button class="choice-btn" data-value="{opt}">{opt}</button>' for opt in choices])}
        </div>
    </div>
    """

def render_sentence_builder(test):
    data = get_test_data(test)
    if not isinstance(data, dict):
        data = {}
    words = data.get("words", [])
    distractors = data.get("distractors", [])
    all_blocks = words + distractors
    import random
    random.shuffle(all_blocks)
    
    return f"""
    <div class="test-content sentence-builder">
        <p class="instruction">Arrange the words into the correct sentence:</p>
        <div class="drop-zone" id="sentenceDropZone"></div>
        <div class="word-blocks">
            {" ".join([f'<div class="word-block" data-value="{word}">{word}</div>' for word in all_blocks])}
        </div>
    </div>
    """

def render_matching(test):
    data = get_test_data(test)
    if not isinstance(data, dict):
        data = {}
    pairs = data.get("pairs", [])
    
    left_items = [p[0] for p in pairs]
    right_items = [p[1] for p in pairs]
    
    import random
    random.shuffle(left_items)
    random.shuffle(right_items)
    
    return f"""
    <div class="test-content matching">
        <p class="instruction">Match the pairs:</p>
        <div class="matching-container">
            <div class="matching-column left">
                {" ".join([f'<div class="match-item" data-value="{item}">{item}</div>' for item in left_items])}
            </div>
            <div class="matching-column right">
                {" ".join([f'<div class="match-item" data-value="{item}">{item}</div>' for item in right_items])}
            </div>
        </div>
    </div>
    """

def render_true_false(test):
    return f"""
    <div class="test-content true-false">
        <p class="question-text">{test.question}</p>
        <div class="tf-options">
            <button class="tf-btn true" data-value="True">True</button>
            <button class="tf-btn false" data-value="False">False</button>
        </div>
    </div>
    """

def render_text_input(test):
    data = get_test_data(test)
    if not isinstance(data, dict):
        data = {}
    hint = data.get("hint", "")
    return f"""
    <div class="test-content text-input">
        <p class="question-text">{test.question}</p>
        <div class="input-wrapper">
            <input type="text" id="answerField" placeholder="Type here..." autocomplete="off">
            <button class="hint-btn" onclick="showHint('{hint}')">💡</button>
        </div>
    </div>
    """

RENDERERS = {
    "multiple_choice": render_multiple_choice,
    "fill_blank": render_fill_blank,
    "sentence_builder": render_sentence_builder,
    "matching": render_matching,
    "true_false": render_true_false,
    "text_input": render_text_input
}
