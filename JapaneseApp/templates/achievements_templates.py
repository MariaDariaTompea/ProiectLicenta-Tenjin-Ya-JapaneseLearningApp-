"""Achievements screen template — full-screen view with sliding parchment and paginated list"""


def get_achievements_page_html(achievements: list = None):
    """Generate HTML achievements page with textured background, sliding parchment,
    paginated achievement list with circular arrow navigation"""
    if achievements is None:
        achievements = []

    # Serialise achievements to a JS array
    ach_js_items = []
    for a in achievements:
        name = a.get("name", "Unknown").replace("\\", "\\\\").replace("'", "\\'").replace('"', '\\"').replace("\n", "\\n")
        desc = a.get("description", "").replace("\\", "\\\\").replace("'", "\\'").replace('"', '\\"').replace("\n", "\\n")
        img  = a.get("image_url", "/customisableprofile/defaultsettings/defaultgem.png")
        date = a.get("date", "")
        ach_js_items.append(f'{{"name":"{name}","description":"{desc}","image_url":"{img}","date":"{date}"}}')
    ach_js_array = "[" + ",".join(ach_js_items) + "]"

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Achievements</title>
        <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&display=swap" rel="stylesheet">
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}

            body {{
                margin: 0;
                height: 100vh;
                overflow: hidden;
                font-family: 'Playfair Display', serif;
                opacity: 0;
                transition: opacity 0.8s ease;
            }}
            body.loaded {{
                opacity: 1;
            }}

            /* ── Full-screen textured background ── */
            .ach-bg {{
                position: fixed;
                top: 0; left: 0;
                width: 100%; height: 100%;
                background: url('/textures/achievementbackground.png') no-repeat center center;
                background-size: cover;
                z-index: 0;
            }}

            /* ── Dark overlay for readability ── */
            .ach-overlay {{
                position: fixed;
                top: 0; left: 0;
                width: 100%; height: 100%;
                background: rgba(0, 0, 0, 0.25);
                z-index: 1;
            }}

            /* ── Back button ── */
            .back-btn {{
                position: fixed;
                top: 24px; left: 28px;
                z-index: 10;
                background: rgba(60, 30, 40, 0.55);
                border: 2px solid rgba(180, 140, 160, 0.5);
                border-radius: 50%;
                width: 48px; height: 48px;
                display: flex;
                align-items: center;
                justify-content: center;
                cursor: pointer;
                transition: background 0.3s ease, transform 0.2s ease;
                text-decoration: none;
            }}
            .back-btn:hover {{
                background: rgba(80, 40, 55, 0.7);
                transform: scale(1.08);
            }}
            .back-btn svg {{
                width: 22px; height: 22px;
                fill: none;
                stroke: #e8d0d8;
                stroke-width: 2.5;
                stroke-linecap: round;
                stroke-linejoin: round;
            }}

            /* ── Parchment container ── */
            .parchment-wrapper {{
                position: fixed;
                top: 0; left: 0;
                width: 100%; height: 100%;
                display: flex;
                align-items: flex-start;
                justify-content: center;
                padding-top: 5vh;
                z-index: 5;
                pointer-events: none;
            }}

            .parchment {{
                position: relative;
                width: min(520px, 85vw);
                height: min(680px, 80vh);
                background: url('/customisableprofile/defaultsettings/pergamentachievements.png') no-repeat center center;
                background-size: 100% 100%;
                pointer-events: auto;

                /* Start off-screen above */
                transform: translateY(-120vh);
                animation: slideDown 1s cubic-bezier(0.22, 1, 0.36, 1) 0.3s forwards;

                display: flex;
                flex-direction: column;
                align-items: center;
                padding: 50px 40px 40px;
            }}

            @keyframes slideDown {{
                0%   {{ transform: translateY(-120vh); }}
                100% {{ transform: translateY(0); }}
            }}

            /* ── Parchment title ── */
            .parchment-title {{
                margin-bottom: -180px;
                margin-top: -88px;
                margin-left: -10px;
                text-align: center;
            }}

            .parchment-title img {{
                max-width: 500px;
                width: 130%;
                height: auto;
                object-fit: contain;
            }}

            /* ── Achievement list inside parchment ── */
            .ach-list {{
                width: 80%;
                height: 54.5%;
                margin-top: 32px;
                overflow-y: auto;
                overflow-x: hidden;
                display: flex;
                flex-direction: column;
                gap: 6px;
                padding: 16px;
                border: none;
                background: transparent;
            }}

            /* Hide scrollbar but keep scrollable */
            .ach-list::-webkit-scrollbar {{
                display: none;
            }}
            .ach-list {{
                -ms-overflow-style: none;
                scrollbar-width: none;
            }}

            .ach-item {{
                display: flex;
                align-items: flex-start;
                justify-content: center;
                padding: 8px 14px;
                text-align: center;
            }}

            .ach-info {{
                display: flex;
                flex-direction: column;
                gap: 3px;
                min-width: 0;
            }}

            .ach-date {{
                font-family: 'Playfair Display', serif;
                font-size: 12px;
                font-style: italic;
                color: #6b4058;
                letter-spacing: 0.8px;
            }}

            .ach-name {{
                font-family: 'Playfair Display', serif;
                font-size: 15px;
                font-weight: 700;
                color: #3d2028;
                line-height: 1.35;
            }}

            .ach-desc {{
                font-family: 'Playfair Display', serif;
                font-size: 13px;
                color: #6b4058;
                line-height: 1.4;
            }}

            /* ── Empty state ── */
            .ach-empty {{
                flex: 1;
                display: flex;
                align-items: center;
                justify-content: center;
                text-align: center;
                font-size: 18px;
                color: #6b4058;
                padding: 20px;
                line-height: 1.6;
            }}

            /* ── Pagination arrows ── */
            .parchment-nav {{
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 30px;
                margin-top: 12px;
            }}

            .parchment-nav .nav-arrow {{
                background: rgba(60, 30, 40, 0.18);
                border: 2px solid rgba(80, 50, 60, 0.35);
                border-radius: 50%;
                width: 40px; height: 40px;
                display: flex;
                align-items: center;
                justify-content: center;
                cursor: pointer;
                transition: background 0.25s ease, transform 0.2s ease;
            }}
            .parchment-nav .nav-arrow:hover {{
                background: rgba(60, 30, 40, 0.30);
                transform: scale(1.12);
            }}
            .parchment-nav .nav-arrow svg {{
                width: 18px; height: 18px;
                fill: none;
                stroke: #3d2028;
                stroke-width: 2.5;
                stroke-linecap: round;
                stroke-linejoin: round;
            }}

            .page-indicator {{
                font-family: 'Playfair Display', serif;
                font-size: 16px;
                color: #3d2028;
                min-width: 50px;
                text-align: center;
            }}

            /* Hide nav when not needed (only 1 page or no achievements) */
            .parchment-nav.hidden {{
                display: none;
            }}
        </style>
    </head>
    <body>
        <!-- Background -->
        <div class="ach-bg"></div>
        <div class="ach-overlay"></div>

        <!-- Back button -->
        <a class="back-btn" href="/profile" title="Back to Profile">
            <svg viewBox="0 0 24 24"><polyline points="15 18 9 12 15 6"/></svg>
        </a>

        <!-- Parchment -->
        <div class="parchment-wrapper">
            <div class="parchment" id="parchment">
                <div class="parchment-title">
                    <img src="/customisableprofile/defaultsettings/Achvlogo.png" alt="Achievements">
                </div>

                <div class="ach-list" id="achList">
                    <!-- Filled by JS -->
                </div>

                <!-- Pagination arrows -->
                <div class="parchment-nav hidden" id="parchmentNav">
                    <div class="nav-arrow" id="arrowLeft" title="Previous">
                        <svg viewBox="0 0 24 24"><polyline points="15 18 9 12 15 6"/></svg>
                    </div>
                    <span class="page-indicator" id="pageIndicator">1 / 1</span>
                    <div class="nav-arrow" id="arrowRight" title="Next">
                        <svg viewBox="0 0 24 24"><polyline points="9 6 15 12 9 18"/></svg>
                    </div>
                </div>
            </div>
        </div>

        <script>
            /* ── Page load fade ── */
            window.addEventListener('load', () => {{
                document.body.classList.add('loaded');
            }});

            /* ── Achievement data ── */
            const ALL_ACH = {ach_js_array};
            const PER_PAGE = 4;
            const totalPages = Math.max(1, Math.ceil(ALL_ACH.length / PER_PAGE));
            let currentPage = 0;

            const achList      = document.getElementById('achList');
            const parchmentNav = document.getElementById('parchmentNav');
            const pageIndicator= document.getElementById('pageIndicator');

            function renderPage(page) {{
                achList.innerHTML = '';

                if (ALL_ACH.length === 0) {{
                    achList.innerHTML = '<div class="ach-empty">No achievements yet.<br>Keep learning to earn some!</div>';
                    return;
                }}

                const start = page * PER_PAGE;
                const slice = [];
                for (let i = 0; i < PER_PAGE; i++) {{
                    const idx = (start + i) % ALL_ACH.length;
                    if (start + i >= ALL_ACH.length && ALL_ACH.length > PER_PAGE) {{
                        // We only wrap when navigating, not on initial overflow
                        break;
                    }}
                    if (start + i >= ALL_ACH.length) break;
                    slice.push(ALL_ACH[start + i]);
                }}

                slice.forEach(a => {{
                    const div = document.createElement('div');
                    div.className = 'ach-item';
                    const dateHtml = a.date ? '<div class="ach-date">' + a.date + '</div>' : '';
                    div.innerHTML = '<div class="ach-info">' + dateHtml + '<div class="ach-name">' + a.name + '</div></div>';
                    achList.appendChild(div);
                }});

                pageIndicator.textContent = (page + 1) + ' / ' + totalPages;
            }}

            /* ── Show / hide nav ── */
            if (totalPages > 1) {{
                parchmentNav.classList.remove('hidden');
            }}

            /* ── Arrow clicks — circular loop ── */
            document.getElementById('arrowRight').addEventListener('click', () => {{
                currentPage = (currentPage + 1) % totalPages;
                renderPage(currentPage);
            }});
            document.getElementById('arrowLeft').addEventListener('click', () => {{
                currentPage = (currentPage - 1 + totalPages) % totalPages;
                renderPage(currentPage);
            }});

            /* ── Initial render ── */
            renderPage(0);
        </script>
    </body>
    </html>
    """
