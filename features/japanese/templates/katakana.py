"""Katakana page templates and utilities"""

def get_katakana_table_html(katakana_list):
    """Generate HTML table for katakana characters in grid layout"""
    
    # Create a dictionary for quick lookup
    katakana_dict = {k.romaji: k for k in katakana_list}
    
    # Traditional katakana table layout (gojūon)
    katakana_table = [
        ['a', 'i', 'u', 'e', 'o'],
        ['ka', 'ki', 'ku', 'ke', 'ko'],
        ['sa', 'shi', 'su', 'se', 'so'],
        ['ta', 'chi', 'tsu', 'te', 'to'],
        ['na', 'ni', 'nu', 'ne', 'no'],
        ['ha', 'hi', 'fu', 'he', 'ho'],
        ['ma', 'mi', 'mu', 'me', 'mo'],
        ['ya', 'yu', 'yo'],
        ['ra', 'ri', 'ru', 're', 'ro'],
        ['wa', 'wo', 'n']
    ]
    
    # Build HTML table
    html_content = """
    <html>
        <head>
            <title>Katakana Characters</title>
            <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&display=swap" rel="stylesheet">
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; background-image: url('/textures/vignettepinkflower.png'); background-size: cover; background-position: center; background-attachment: fixed; }
                p { font-family: 'Playfair Display', serif; font-size: 18px; line-height: 1.6; max-width: 900px; color: #FCBCD7; font-weight: 500; }
                h1 { font-family: 'Playfair Display', serif; font-size: 48px; color: #FCBCD7; font-weight: 700; letter-spacing: 2px; margin-left: 160px; }
                .romaji { font-family: 'Playfair Display', serif; font-size: 16px; color: #666; margin-bottom: 8px; font-weight: 600; }
                .katakana-grid { display: table; border-collapse: collapse; margin-top: 20px; }
                .row { display: table-row; }
                .cell { 
                    display: table-cell; 
                    border: 2px solid #ddd; 
                    padding: 15px; 
                    text-align: center;
                    min-width: 120px;
                }
                .cell-header { background-color: #ff9d9d; color: white; font-weight: bold; }
                .cell-content { background-color: #fadce9; }
                .cell-content:nth-child(even) { background-color: #bf8ea3; }
                .katakana-char { font-size: 32px; margin-bottom: 8px; }
                .romaji { font-size: 14px; color: #666; margin-bottom: 8px; }
                .char-image { max-width: 100px; height: auto; margin-bottom: 8px; }
                button { background: none; border: none; cursor: pointer; padding: 5px; }
                button img { width: 30px; height: 30px; }
                .cell { position: relative; }
                .cell:hover .fill-heart .heart-fill { animation: fillHeart 3s linear forwards; }
                .cell:hover { filter: brightness(1.18); transition: filter 0.2s; }
                .fill-heart {
                    position: absolute;
                    bottom: 6px;
                    right: 6px;
                    width: 20px;
                    height: 20px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                }
                .heart-outline {
                    position: absolute;
                    width: 16px;
                    height: 16px;
                    z-index: 2;
                }
                .heart-fill {
                    position: absolute;
                    width: 16px;
                    height: 16px;
                    z-index: 1;
                    clip-path: inset(100% 0 0 0);
                    transition: clip-path 0s;
                    background: #EF87BE;
                    mask: url('data:image/svg+xml;utf8,<svg width="16" height="16" viewBox="0 0 16 16" fill="white" xmlns="http://www.w3.org/2000/svg"><path d="M8 14s-4.477-3.548-6.13-5.353C-0.753 6.087 0.753 2.913 3.87 2.913c1.313 0 2.537 0.807 3.13 2.06C7.593 3.72 8.817 2.913 10.13 2.913c3.117 0 4.623 3.174 1.76 5.734C12.477 10.452 8 14 8 14z"/></svg>') center/contain no-repeat;
                }
                @keyframes fillHeart {
                    from { clip-path: inset(100% 0 0 0); }
                    to { clip-path: inset(0 0 0 0); }
                }
                
                /* Video Popup Modal */
                .modal { display: none; position: fixed; z-index: 1000; left: 0; top: 0; width: 100%; height: 100%; background-color: rgba(0,0,0,0.6); }
                .modal.show { display: flex; align-items: center; justify-content: center; }
                .modal-content { background-color: white; padding: 30px; border-radius: 8px; width: 90%; max-width: 600px; box-shadow: 0 4px 20px rgba(0,0,0,0.3); }
                .close-modal { float: right; font-size: 28px; font-weight: bold; color: #aaa; cursor: pointer; }
                .close-modal:hover { color: #000; }
                .modal video { width: 100%; max-height: 400px; border-radius: 4px; margin-top: 15px; }

                /* Back button */
                .back-btn {
                    position: fixed;
                    top: 30px;
                    left: 30px;
                    z-index: 500;
                    background: rgba(239, 135, 190, 0.15);
                    border: 2px solid #EF87BE;
                    color: #FCBCD7;
                    font-family: 'Playfair Display', serif;
                    font-size: 18px;
                    padding: 10px 24px;
                    border-radius: 30px;
                    cursor: pointer;
                    transition: background 0.3s ease, transform 0.2s ease, box-shadow 0.3s ease;
                    letter-spacing: 1px;
                }
                .back-btn:hover {
                    background: rgba(239, 135, 190, 0.35);
                    transform: scale(1.05);
                    box-shadow: 0 0 15px rgba(239, 135, 190, 0.4);
                }

                /* Page fade-out overlay */
                .page-fade {
                    position: fixed;
                    top: 0; left: 0;
                    width: 100%; height: 100%;
                    background: #0a0a0a;
                    z-index: 9999;
                    opacity: 0;
                    pointer-events: none;
                    transition: opacity 0.6s ease;
                }
                .page-fade.active {
                    opacity: 1;
                    pointer-events: all;
                }
            </style>
        </head>
        <body>
            <div class="page-fade" id="pageFade"></div>
            <button class="back-btn" onclick="goBack()">&#8592; Back</button>
            <h1>Katakana Characters</h1>
            <p>Here is a list of all the basic katakana characters, without any additional transformations (dakuten), along with the correct stroke order for writing them. Make sure to review this table before proceeding with the exercises.</p>
            <div class="katakana-grid">
    """
    
    # Generate grid
    for row in katakana_table:
        html_content += '<div class="row">'
        for romaji in row:
            if romaji in katakana_dict:
                char = katakana_dict[romaji]
                html_content += f"""
                <div class="cell cell-content" onmouseenter="startHoverFill(this)" onmouseleave="cancelHoverFill(this)" onclick="if(this.hoverComplete) showVideoModal('{char.romaji}')">
                    <div class="fill-heart">
                        <svg class="heart-outline" viewBox="0 0 16 16" width="16" height="16">
                            <path d="M8 14s-4.477-3.548-6.13-5.353C-0.753 6.087 0.753 2.913 3.87 2.913c1.313 0 2.537 0.807 3.13 2.06C7.593 3.72 8.817 2.913 10.13 2.913c3.117 0 4.623 3.174 1.76 5.734C12.477 10.452 8 14 8 14z" fill="none" stroke="#EF87BE" stroke-width="1.5"/>
                        </svg>
                        <div class="heart-fill"></div>
                    </div>
                    <div class="katakana-char">{char.character}</div>
                    <div class="romaji">{char.romaji}</div>
                    <button onclick="event.stopPropagation(); document.getElementById('audio_{char.romaji}_k').play()">
                        <img src="/icons/replysound.png">
                    </button>
                    <audio id="audio_{char.romaji}_k" style="display:none;">
                        <source src="/katakana_assets/audio/{char.romaji}.mp3" type="audio/mpeg">
                    </audio>
                    <br><img src="/katakana_assets/images/{char.image_filename}" class="char-image" alt="{char.character}">
                </div>
                """
        html_content += '</div>'
    
    html_content += """
            </div>
            
            <!-- Video Modal Popup -->
            <div id="videoModal" class="modal">
                <div class="modal-content">
                    <span class="close-modal" onclick="closeVideoModal()">&times;</span>
                    <h2 id="videoTitle" style="color: #300825; font-family: 'Playfair Display', serif; font-size: 32px; margin-top: 0;">How to Write: <span id="charDisplay"></span></h2>
                    <video id="videoPlayer" autoplay loop muted playsinline style="pointer-events: none;"></video>
                </div>
            </div>
            
            <script>
                let hoverTimers = {};
                
                function startHoverFill(element) {
                    const romaji = element.querySelector('.romaji').textContent;
                    const heartFill = element.querySelector('.heart-fill');
                    // Reset heart fill animation
                    heartFill.style.animation = 'none';
                    heartFill.style.clipPath = 'inset(100% 0 0 0)';
                    setTimeout(() => {
                        heartFill.style.animation = 'fillHeart 3s linear forwards';
                    }, 10);
                    
                    // Set timer for 3 seconds
                    hoverTimers[romaji] = setTimeout(() => {
                        element.hoverComplete = true;
                        showVideoModal(romaji);
                    }, 3000);
                }
                
                function cancelHoverFill(element) {
                    const romaji = element.querySelector('.romaji').textContent;
                    const heartFill = element.querySelector('.heart-fill');
                    // Clear the timer
                    if (hoverTimers[romaji]) {
                        clearTimeout(hoverTimers[romaji]);
                        delete hoverTimers[romaji];
                    }
                    // Reset heart fill animation
                    heartFill.style.animation = 'none';
                    heartFill.style.clipPath = 'inset(100% 0 0 0)';
                    element.hoverComplete = false;
                }
                
                function showVideoModal(romaji) {
                    const modal = document.getElementById('videoModal');
                    const videoPlayer = document.getElementById('videoPlayer');
                    const charDisplay = document.getElementById('charDisplay');
                    
                    // Get the character
                    const charCell = document.querySelector(`[onclick*="showVideoModal('${romaji}')"]`);
                    if (charCell) {
                        const character = charCell.querySelector('.katakana-char').textContent;
                        charDisplay.textContent = character;
                    }
                    
                    // Video URL mapping
                    const videoUrls = {
                        'a': '/katakana_assets/videos/a.mp4', 'i': '/katakana_assets/videos/i.mp4', 'u': '/katakana_assets/videos/u.mp4', 'e': '/katakana_assets/videos/e.mp4', 'o': '/katakana_assets/videos/o.mp4',
                        'ka': '/katakana_assets/videos/ka.mp4', 'ki': '/katakana_assets/videos/ki.mp4', 'ku': '/katakana_assets/videos/ku.mp4', 'ke': '/katakana_assets/videos/ke.mp4', 'ko': '/katakana_assets/videos/ko.mp4',
                        'sa': '/katakana_assets/videos/sa.mp4', 'shi': '/katakana_assets/videos/shi.mp4', 'su': '/katakana_assets/videos/su.mp4', 'se': '/katakana_assets/videos/se.mp4', 'so': '/katakana_assets/videos/so.mp4',
                        'ta': '/katakana_assets/videos/ta.mp4', 'chi': '/katakana_assets/videos/chi.mp4', 'tsu': '/katakana_assets/videos/tsu.mp4', 'te': '/katakana_assets/videos/te.mp4', 'to': '/katakana_assets/videos/to.mp4',
                        'na': '/katakana_assets/videos/na.mp4', 'ni': '/katakana_assets/videos/ni.mp4', 'nu': '/katakana_assets/videos/nu.mp4', 'ne': '/katakana_assets/videos/ne.mp4', 'no': '/katakana_assets/videos/no.mp4',
                        'ha': '/katakana_assets/videos/ha.mp4', 'hi': '/katakana_assets/videos/hi.mp4', 'fu': '/katakana_assets/videos/fu.mp4', 'he': '/katakana_assets/videos/he.mp4', 'ho': '/katakana_assets/videos/ho.mp4',
                        'ma': '/katakana_assets/videos/ma.mp4', 'mi': '/katakana_assets/videos/mi.mp4', 'mu': '/katakana_assets/videos/mu.mp4', 'me': '/katakana_assets/videos/me.mp4', 'mo': '/katakana_assets/videos/mo.mp4',
                        'ya': '/katakana_assets/videos/ya.mp4', 'yu': '/katakana_assets/videos/yu.mp4', 'yo': '/katakana_assets/videos/yo.mp4',
                        'ra': '/katakana_assets/videos/ra.mp4', 'ri': '/katakana_assets/videos/ri.mp4', 'ru': '/katakana_assets/videos/ru.mp4', 're': '/katakana_assets/videos/re.mp4', 'ro': '/katakana_assets/videos/ro.mp4',
                        'wa': '/katakana_assets/videos/wa.mp4', 'wo': '/katakana_assets/videos/wo.mp4', 'n': '/katakana_assets/videos/n.mp4'
                    };
                    
                    // Set video source if it exists
                    if (videoUrls[romaji]) {
                        videoPlayer.src = videoUrls[romaji];
                        videoPlayer.load();
                        setTimeout(() => { videoPlayer.play(); }, 100);
                    } else {
                        videoPlayer.src = '';
                    }
                    // Show modal
                    modal.classList.add('show');
                }
                
                function closeVideoModal() {
                    const modal = document.getElementById('videoModal');
                    const videoPlayer = document.getElementById('videoPlayer');
                    videoPlayer.pause();
                    modal.classList.remove('show');
                }
                
                // Close modal when clicking outside of it
                window.onclick = function(event) {
                    const modal = document.getElementById('videoModal');
                    if (event.target === modal) {
                        closeVideoModal();
                    }
                }

                // Back button with fade transition
                function goBack() {
                    document.getElementById('pageFade').classList.add('active');
                    setTimeout(() => {
                        window.location.href = '/course/vocabulary';
                    }, 500);
                }
            </script>
        </body>
    </html>
    """
    return html_content
