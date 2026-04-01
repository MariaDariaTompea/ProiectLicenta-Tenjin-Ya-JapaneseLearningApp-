import json

def render_exercise_runner(exercise, tests, chapter_id, category="grammar"):
    tests_json = json.dumps([{
        'id': t.id,
        'test_type': t.test_type,
        'question': t.question,
        'correct_answer': t.correct_answer,
        'options': t.options,
    } for t in tests])

    theory_html = exercise.theory_content if exercise.theory_content else ""
    theory_display = "flex" if theory_html else "none"

    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{exercise.title} — Tenjin-Ya</title>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/wanakana"></script>
    <style>
        /* CSS reset and foundations */
        *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: 'Inter', sans-serif;
            background: #0d0608;
            color: #FCBCD7;
            min-height: 100vh;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 20px 20px 100px 20px;
            gap: 10px;
        }}

        /* Background layout */
        .bg-layer {{
            position: fixed; inset: 0;
            background: radial-gradient(circle at center, #1a0a12 0%, #0d0608 100%);
            z-index: -1;
        }}

        /* Top Bar */
        .top-bar {{
            width: 80%; max-width: 800px;
            display: flex; flex-direction: column; gap: 10px;
            margin-top: 20px;
            flex-shrink: 0;
            position: relative;
            z-index: 10;
        }}
        .stars-container {{
            display: flex; justify-content: center; gap: 40px; margin-bottom: 10px;
        }}
        .star-box {{
            position: relative;
            width: 120px;
            height: 120px;
            transition: transform 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
        }}
        .star-box.earned {{
            transform: scale(1.15);
        }}
        .fox-icon {{
            position: absolute;
            inset: 0;
            width: 100%;
            height: 100%;
            background-size: contain;
            background-repeat: no-repeat;
            background-position: center;
        }}
        .fox-off {{
            background-image: url('/icons/foxheadlightoff.png');
            opacity: 1;
            transition: opacity 0.6s ease;
        }}
        .fox-on {{
            background-image: url('/icons/foxheadlighton.png');
            opacity: 0;
            transition: opacity 0.6s ease;
            filter: drop-shadow(0 0 8px rgba(252, 188, 215, 0.4));
        }}
        .star-box.earned .fox-off {{
            opacity: 0;
        }}
        .star-box.earned .fox-on {{
            opacity: 1;
        }}

        .progress-container {{ display: flex; align-items: center; gap: 20px; }}
        .progress-bar {{
            flex: 1; height: 12px; background: rgba(252,188,215,0.1);
            border-radius: 6px; overflow: hidden; position: relative;
        }}
        .progress-fill {{
            position: absolute; height: 100%; top: 0; left: 0;
            background: linear-gradient(90deg, #E56AB3, #FCBCD7);
            width: 0%; transition: width 0.5s cubic-bezier(0.34,1.56,0.64,1);
        }}
        .progress-counter {{
            font-family: 'Playfair Display', serif; font-size: 14px;
            color: rgba(252,188,215,0.6); min-width: 40px;
        }}

        /* Theory Modal Overlay */
        .theory-overlay {{
            position: fixed; inset: 0; background: rgba(0,0,0,0.85);
            display: {theory_display}; justify-content: center; align-items: center; z-index: 100;
        }}
        .theory-content {{
            background: #1a0a12; border: 1px solid rgba(252,188,215,0.2);
            border-radius: 16px; width: 90%; max-width: 600px; max-height: 80vh;
            padding: 40px; overflow-y: auto; text-align: left;
            box-shadow: 0 10px 40px rgba(229,106,179,0.3);
        }}
        .theory-content h3 {{ font-family: 'Playfair Display', serif; font-size: 32px; margin-bottom: 20px; color: #E56AB3; }}
        .theory-content p {{ margin-bottom: 15px; line-height: 1.6; font-size: 16px; color: #FCBCD7; }}
        .theory-content ul {{ margin-left: 20px; margin-bottom: 20px; }}
        .theory-content li {{ margin-bottom: 10px; line-height: 1.5; color: rgba(252,188,215,0.8); }}
        .close-theory-btn {{
            background: linear-gradient(135deg, #E56AB3, #9d3f74);
            color: white; border: none; border-radius: 30px;
            padding: 12px 40px; font-size: 16px; font-weight: 600; cursor: pointer;
            display: block; margin: 30px auto 0; text-transform: uppercase; letter-spacing: 2px;
        }}

        /* Exercise Card container */
        .exercise-card {{
            background: rgba(252,188,215,0.03);
            border: 1px solid rgba(252,188,215,0.1);
            border-radius: 20px;
            padding: 40px; width: 90%; max-width: 700px; min-height: 350px;
            display: flex; flex-direction: column; align-items: center;
            box-shadow: 0 10px 40px rgba(0,0,0,0.4);
            transition: all 0.5s ease;
            transform: translateY(20px); opacity: 0;
            visibility: hidden;
            margin-top: 30px;
            flex-shrink: 0;
            position: relative;
            z-index: 5;
        }}
        .exercise-card.visible {{ transform: none; opacity: 1; visibility: visible; }}

        .question-text {{
            font-family: 'Playfair Display', serif; font-size: 28px;
            text-align: center; margin-bottom: 40px; line-height: 1.4;
        }}

        /* Renderer-specific CSS */
        .options-grid, .choices-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; width: 100%; }}
        .option-btn, .choice-btn, .tf-btn {{
            background: rgba(252,188,215,0.06); border: 1px solid rgba(252,188,215,0.15);
            color: #FCBCD7; border-radius: 12px; padding: 18px; cursor: pointer;
            font-size: 16px; transition: all 0.2s ease; font-family: 'Inter', sans-serif;
        }}
        .option-btn:hover, .choice-btn:hover, .match-item:hover, .tf-btn:hover {{
            background: rgba(252,188,215,0.12); border-color: rgba(252,188,215,0.35); transform: translateY(-2px);
        }}
        .option-btn.selected, .choice-btn.selected, .match-item.selected, .tf-btn.selected {{
            background: #E56AB3 !important; color: #fff !important; border-color: #E56AB3 !important;
        }}
        .match-item.matched-correct {{
            opacity: 0.4 !important;
            filter: grayscale(80%);
            box-shadow: inset 0 0 20px rgba(0,0,0,0.5);
            pointer-events: none !important;
            border-color: rgba(76, 175, 80, 0.4) !important;
            background: rgba(76, 175, 80, 0.1) !important;
            transform: scale(0.95);
        }}

        .word-blocks {{ display: flex; flex-wrap: wrap; gap: 10px; margin-top: 30px; justify-content: center; }}
        .word-block {{
            padding: 10px 20px; background: rgba(252,188,215,0.1); border-radius: 8px;
            border: 1px solid rgba(252,188,215,0.2); cursor: pointer; transition: all 0.2s;
        }}
        .drop-zone {{
            width: 100%; min-height: 50px; background: rgba(0,0,0,0.2); border-bottom: 2px solid rgba(252,188,215,0.2);
            margin: 20px 0; padding: 10px; display: flex; flex-wrap: wrap; gap: 10px; justify-content: center;
        }}

        .matching-container {{ display: flex; gap: 40px; width: 100%; justify-content: space-between; }}
        .matching-column {{ display: flex; flex-direction: column; gap: 10px; flex: 1; }}
        .match-item {{
            padding: 14px; background: rgba(252,188,215,0.05); border: 1px solid rgba(252,188,215,0.1);
            border-radius: 8px; text-align: center; cursor: pointer; transition: all 0.2s;
        }}

        .input-wrapper {{ width: 100%; display: flex; gap: 12px; margin-top: 20px; }}
        #answerField {{
            flex: 1; background: transparent; border: none; border-bottom: 2px solid rgba(252,188,215,0.2);
            font-size: 24px; color: #FCBCD7; text-align: center; padding: 10px; outline: none;
        }}
        .hint-btn {{
            width: 40px; height: 40px; border-radius: 50%; background: rgba(252,188,215,0.1); border: none;
            color: #FCBCD7; cursor: pointer; transition: background 0.2s;
        }}

        /* Bottom Controls */
        .controls {{
            position: fixed; bottom: 40px; width: 100%; display: flex; justify-content: center;
            opacity: 0; transition: opacity 0.5s ease; visibility: hidden;
        }}
        .controls.visible {{ opacity: 1; visibility: visible; }}
        .check-btn {{
            background: linear-gradient(135deg, #E56AB3, #9d3f74);
            color: white; border: none; border-radius: 30px;
            padding: 16px 60px; font-size: 18px; font-weight: 600;
            cursor: pointer; box-shadow: 0 4px 15px rgba(229,106,179,0.3);
            text-transform: uppercase; letter-spacing: 2px; transition: all 0.3s;
        }}
        .check-btn:hover {{ transform: scale(1.05); filter: brightness(1.1); }}

        /* Results Screen Vigenere Style */
        .results-screen {{
            display: none; flex-direction: column; align-items: center; text-align: center;
            background: rgba(26,10,18,0.9); padding: 50px; border-radius: 20px; border: 1px solid rgba(229,106,179,0.3);
            box-shadow: 0 0 50px rgba(229,106,179,0.2); z-index: 10;
        }}
        .results-title {{ font-family: 'Playfair Display', serif; font-size: 48px; color: #E56AB3; margin-bottom: 10px; }}
        
        .results-stars {{ 
            display: flex; gap: 40px; margin-bottom: 40px; justify-content: center;
        }}
        .results-stars .star-box {{ width: 180px; height: 180px; }}

        .results-score {{ font-size: 24px; font-weight: 500; font-family: 'Inter', sans-serif; color: rgba(252,188,215,0.8); margin-bottom: 40px; }}
        
        .results-buttons {{ display: flex; gap: 20px; }}
        .btn-retry {{
            background: rgba(252,188,215,0.06); border: 1px solid rgba(252,188,215,0.3);
            color: #FCBCD7; border-radius: 30px; padding: 16px 40px; font-size: 16px; font-weight: 600;
            cursor: pointer; text-transform: uppercase; letter-spacing: 2px; transition: all 0.3s;
        }}
        .btn-retry:hover {{ background: rgba(252,188,215,0.15); }}

    </style>
</head>
<body>
    <div class="bg-layer"></div>

    <div class="theory-overlay" id="theoryOverlay">
        <div class="theory-content">
            {theory_html}
            <button class="close-theory-btn" onclick="closeTheory()">Start Test</button>
        </div>
    </div>

    <div class="top-bar">
        <div class="stars-container" id="starsContainer">
            <div class="star-box" id="star1">
                <div class="fox-icon fox-off"></div>
                <div class="fox-icon fox-on"></div>
            </div>
            <div class="star-box" id="star2">
                <div class="fox-icon fox-off"></div>
                <div class="fox-icon fox-on"></div>
            </div>
            <div class="star-box" id="star3">
                <div class="fox-icon fox-off"></div>
                <div class="fox-icon fox-on"></div>
            </div>
        </div>
        <div class="progress-container">
            <div class="progress-counter" id="progressCount">1 / 15</div>
            <div class="progress-bar"><div class="progress-fill" id="progressFill"></div></div>
        </div>
    </div>

    <div class="exercise-card" id="questionCard">
        <!-- Content injected here -->
    </div>

    <div class="results-screen" id="resultsScreen">
        <h2 class="results-title">Exercise Complete</h2>
        <div class="results-stars" id="finalStars">
            <!-- Injected -->
        </div>
        <div class="results-score" id="finalScoreText">12 / 15 (80%)</div>
        <div class="results-buttons">
            <button class="btn-retry" onclick="location.reload()">Retry</button>
            <button class="check-btn" onclick="window.location.href='/course/{category}'">Continue</button>
        </div>
    </div>

    <div class="controls" id="controls">
        <button class="check-btn" id="checkBtn">Check Answer</button>
    </div>

    <script>
        const tests = {tests_json};
        
        let currentIndex = 0;
        let score = 0; // Absolute
        let firstAttemptSuccesses = 0; // Number of questions correctly answered ON FIRST TRY
        let isFirstAttemptForCurrentQuestion = true;
        let hasScoredThisQuestion = false;
        let selectedValue = null;
        let matchingTimeout = null;

        const card = document.getElementById('questionCard');
        const fill = document.getElementById('progressFill');
        const counter = document.getElementById('progressCount');
        const controls = document.getElementById('controls');
        const checkBtn = document.getElementById('checkBtn');
        const theoryOverlay = document.getElementById('theoryOverlay');

        function closeTheory() {{
            theoryOverlay.style.display = 'none';
            if(tests.length > 0) loadQuestion(0);
            else showResults();
        }}

        function updateStars() {{
            // 5 success -> 1 star, 10 -> 2, 15 -> 3
            if(firstAttemptSuccesses >= 5) document.getElementById('star1').classList.add('earned');
            if(firstAttemptSuccesses >= 10) document.getElementById('star2').classList.add('earned');
            if(firstAttemptSuccesses >= 15) document.getElementById('star3').classList.add('earned');
        }}

        function loadQuestion(index) {{
            if (index >= tests.length) {{
                showResults();
                return;
            }}

            const test = tests[index];
            counter.innerText = `${{index + 1}} / ${{tests.length}}`;
            fill.style.width = `${{((index + 1) / tests.length) * 100}}%`;
            isFirstAttemptForCurrentQuestion = true;
            hasScoredThisQuestion = false;
            selectedValue = null;
            if(matchingTimeout) clearTimeout(matchingTimeout);
            
            card.classList.remove('visible');
            setTimeout(() => {{
                fetch(`/api/exercise/render-test/${{test.id}}`)
                    .then(res => res.json())
                    .then(data => {{
                        card.innerHTML = data.html;
                        card.classList.add('visible');
                        controls.classList.add('visible');
                        attachListeners();
                    }});
            }}, 500);
        }}

        function attachListeners() {{
            const test = tests[currentIndex];
            checkBtn.innerText = "Check Answer";
            checkBtn.style.background = "";
            checkBtn.onclick = checkAnswer;

            // Bind Wanakana to text input if it exists
            let inputEl = document.getElementById('answerField');
            if (inputEl && typeof wanakana !== 'undefined') {{
                wanakana.bind(inputEl);
            }}

            document.querySelectorAll('.option-btn, .choice-btn, .tf-btn').forEach(btn => {{
                btn.onclick = function() {{
                    document.querySelectorAll('.option-btn, .choice-btn, .tf-btn').forEach(b => b.classList.remove('selected'));
                    this.classList.add('selected');
                    selectedValue = this.getAttribute('data-value');
                }};
            }});

            document.querySelectorAll('.word-block').forEach(blk => {{
                blk.onclick = function() {{
                    const dz = document.getElementById('sentenceDropZone');
                    if (this.parentNode.id === 'sentenceDropZone') {{
                        document.querySelector('.word-blocks').appendChild(this);
                    }} else {{
                        dz.appendChild(this);
                    }}
                }};
            }});

            let matchLeft = null, matchRight = null;
            let matchedPairs = 0;
            let totalPairs = test.test_type === 'matching' ? (JSON.parse(test.options).pairs || []).length : 0;
            
            if (test.test_type === 'matching') {{
                checkBtn.innerText = "Match all pairs first";
                checkBtn.disabled = true;
                checkBtn.style.opacity = '0.5';
                checkBtn.style.pointerEvents = 'none';
            }} else {{
                checkBtn.disabled = false;
                checkBtn.style.opacity = '1';
                checkBtn.style.pointerEvents = 'auto';
            }}

            document.querySelectorAll('.match-item').forEach(item => {{
                item.onclick = function() {{
                    if (this.classList.contains('matched')) return;

                    if (this.parentNode.classList.contains('left')) {{
                        document.querySelectorAll('.matching-column.left .match-item:not(.matched)').forEach(i => i.classList.remove('selected'));
                        matchLeft = this;
                    }} else {{
                        document.querySelectorAll('.matching-column.right .match-item:not(.matched)').forEach(i => i.classList.remove('selected'));
                        matchRight = this;
                    }}
                    this.classList.add('selected');

                    if (matchLeft && matchRight) {{
                        const opts = JSON.parse(test.options);
                        const pairs = opts.pairs || [];
                        const vL = matchLeft.getAttribute('data-value');
                        const vR = matchRight.getAttribute('data-value');
                        const isMatch = pairs.find(p => p[0] === vL && p[1] === vR);

                        if (isMatch) {{
                            matchLeft.classList.add('matched');
                            matchRight.classList.add('matched');
                            
                            matchLeft.style.backgroundColor = '#4CAF50';
                            matchRight.style.backgroundColor = '#4CAF50';
                            matchLeft.style.color = '#fff';
                            matchRight.style.color = '#fff';
                            
                            const mL = matchLeft;
                            const mR = matchRight;
                            
                            setTimeout(() => {{
                                mL.classList.remove('selected');
                                mR.classList.remove('selected');
                                mL.style.backgroundColor = '';
                                mR.style.backgroundColor = '';
                                mL.style.color = '';
                                mR.style.color = '';
                                mL.classList.add('matched-correct');
                                mR.classList.add('matched-correct');
                            }}, 400);
                            
                            matchLeft = null;
                            matchRight = null;
                            matchedPairs++;
                            
                            if (matchedPairs >= totalPairs) {{
                                selectedValue = "pair match";
                                checkBtn.disabled = false;
                                checkBtn.style.opacity = '1';
                                checkBtn.style.pointerEvents = 'auto';
                                checkBtn.innerText = "Check Answer";
                                // Auto check answer after a short delay
                                if(matchingTimeout) clearTimeout(matchingTimeout);
                                matchingTimeout = setTimeout(() => {{
                                    checkAnswer();
                                }}, 800);
                            }}
                        }} else {{
                            isFirstAttemptForCurrentQuestion = false;
                            const mL = matchLeft;
                            const mR = matchRight;
                            mL.style.backgroundColor = '#f44336';
                            mR.style.backgroundColor = '#f44336';
                            
                            setTimeout(() => {{
                                mL.classList.remove('selected');
                                mR.classList.remove('selected');
                                mL.style.backgroundColor = '';
                                mR.style.backgroundColor = '';
                            }}, 500);
                            matchLeft = null;
                            matchRight = null;
                        }}
                    }}
                }};
            }});
        }}

        function checkAnswer() {{
            if (hasScoredThisQuestion) return;
            if (matchingTimeout) {{
                clearTimeout(matchingTimeout);
                matchingTimeout = null;
            }}

            const test = tests[currentIndex];
            let UserAnswer = selectedValue;

            if (test.test_type === 'sentence_builder') {{
                const dz = document.getElementById('sentenceDropZone');
                UserAnswer = Array.from(dz.children).map(c => c.getAttribute('data-value')).join(' ');
            }} else if (test.test_type === 'text_input') {{
                let inputEl = document.getElementById('answerField');
                if(inputEl) UserAnswer = inputEl.value.trim();
            }}

            // Normalise strings by removing all spaces to check for equality without space sensitivity
            const normalize = (str) => (str || "").replace(/\\s+/g, "");

            if (normalize(UserAnswer) === normalize(test.correct_answer)) {{
                if(isFirstAttemptForCurrentQuestion) {{
                    firstAttemptSuccesses++;
                    updateStars();
                }}
                score++;
                hasScoredThisQuestion = true;
                checkBtn.innerText = "Correct! ✅ Next";
                checkBtn.style.background = "#4CAF50";
                checkBtn.onclick = nextQuestion;
            }} else {{
                isFirstAttemptForCurrentQuestion = false;
                checkBtn.innerText = "Incorrect ❌ Try Again";
                checkBtn.style.background = "#f44336";
                checkBtn.onclick = () => {{ attachListeners(); checkBtn.innerText="Check Answer"; checkBtn.style.background=""; }};
            }}
        }}

        function nextQuestion() {{
            checkBtn.style.background = "";
            currentIndex++;
            loadQuestion(currentIndex);
        }}

        function showResults() {{
            card.style.display = 'none';
            controls.style.display = 'none';
            document.getElementById('resultsScreen').style.display = 'flex';
            
            // Render final stars
            let starsHtml = "";
            let starCount = 0;
            if(firstAttemptSuccesses >= 5) starCount++;
            if(firstAttemptSuccesses >= 10) starCount++;
            if(firstAttemptSuccesses >= 15) starCount++;
            
            for(let i=1; i<=3; i++) {{
                const earnedClass = i <= starCount ? 'earned' : '';
                starsHtml += `
                    <div class="star-box ${{earnedClass}}">
                        <div class="fox-icon fox-off"></div>
                        <div class="fox-icon fox-on"></div>
                    </div>
                `;
            }}
            document.getElementById('finalStars').innerHTML = starsHtml;
            
            let pct = Math.round((tests.length > 0 ? (score / tests.length) : 0) * 100);
            document.getElementById('finalScoreText').innerText = `${{score}} / ${{tests.length}} (${{pct}}%)`;

            // POST results to backend
            fetch('/api/exercise/complete', {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify({{
                    exercise_id: {exercise.id},
                    stars: starCount
                }})
            }}).then(r => r.json()).then(data => console.log("Progress saved:", data));
        }}

        function showHint(text) {{
            alert("Hint: " + text);
        }}

        // If there's no theory, start immediately
        window.onload = () => {{
            if('{theory_display}' === 'none') {{
                loadQuestion(0);
            }}
        }};
    </script>
</body>
</html>
"""
