"""Profile screen template"""


def get_profile_page_html(user_name: str, nickname: str, avatar_url: str, banner_url: str, user_email: str, current_level: str = "N5", achievements: list = None, owned_banners: list = None, owned_achievements: list = None):
    """Generate HTML profile page with temple background, vertical banner, avatar, nickname,
    achievement slots, bottom navigation bar and settings slide panel"""
    if achievements is None:
        achievements = [
            {"name": "Empty Slot", "description": "Equip an achievement you own", "image_url": "/customisableprofile/defaultsettings/defaultgem.png", "earned": False},
            {"name": "Empty Slot", "description": "Equip an achievement you own", "image_url": "/customisableprofile/defaultsettings/defaultgem.png", "earned": False},
            {"name": "Empty Slot", "description": "Equip an achievement you own", "image_url": "/customisableprofile/defaultsettings/defaultgem.png", "earned": False},
        ]
    if owned_banners is None:
        owned_banners = []
    if owned_achievements is None:
        owned_achievements = []
    
    # Build achievement slot HTML
    achievement_slots_html = ""
    for i, ach in enumerate(achievements):
        earned_class = "earned" if ach.get("earned") else ""
        achievement_slots_html += f'''
                <div class="achievement-slot {earned_class}" data-slot="{i}">
                    <img src="{ach['image_url']}" alt="{ach['name']}">
                    <div class="achievement-tooltip">
                        <div class="tooltip-name">{ach['name']}</div>
                        <div class="tooltip-desc">{ach['description']}</div>
                    </div>
                </div>'''

    # Build owned banners grid HTML
    if owned_banners:
        owned_banners_html = ""
        for b in owned_banners:
            owned_banners_html += f'''<div class="inventory-item" data-id="{b['id']}" data-type="banner">
                <img src="{b['image_url']}" alt="{b['name']}">
                <span>{b['name']}</span>
            </div>'''
    else:
        owned_banners_html = '<div class="inventory-empty">You don\'t have any banners.<br>Participate at events to get more!</div>'

    # Build owned achievements grid HTML
    if owned_achievements:
        owned_achievements_html = ""
        for a in owned_achievements:
            desc = a.get('description', '')
            owned_achievements_html += f'''<div class="inventory-item" data-id="{a['id']}" data-type="achievement">
                <img src="{a['image_url']}" alt="{a['name']}">
                <span>{a['name']}</span>
            </div>'''
    else:
        owned_achievements_html = '<div class="inventory-empty">You don\'t have any achievements.<br>Participate at events to get more!</div>'

    # Build sliding panel banners HTML
    if owned_banners:
        sliding_banners_html = ""
        for b in owned_banners:
            sliding_banners_html += f'''<div class="sliding-item" data-id="{b['id']}" data-type="banner">
                <img src="{b['image_url']}" alt="{b['name']}">
                <div class="sliding-item-title">{b['name']}</div>
            </div>'''
    else:
        sliding_banners_html = '<div class="sliding-empty">Empty</div>'

    # Build sliding panel gems/achievements HTML
    if owned_achievements:
        sliding_gems_html = ""
        for a in owned_achievements:
            desc = a.get('description', '')
            sliding_gems_html += f'''<div class="sliding-item gem-item" data-id="{a['id']}">
                <img src="{a['image_url']}" alt="{a['name']}">
                <div class="sliding-item-title">{a['name']}</div>
                <div class="gem-hover-popup">{desc}</div>
            </div>'''
    else:
        sliding_gems_html = '<div class="sliding-empty">Empty</div>'
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Profile</title>
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
                transition: opacity 1s ease;
            }}
            body.loaded {{
                opacity: 1;
            }}

            /* ── Full-screen temple background ── */
            .bg-layer {{
                position: fixed;
                top: 0; left: 0;
                width: 100%; height: 100%;
                background: url('/textures/templeprofile.png') no-repeat center center;
                background-size: cover;
                z-index: 0;
            }}

            /* ── Right-side vertical banner ── */
            .profile-banner {{
                position: fixed;
                right: 1px;
                top: 0;
                width: 416px;
                height: 100vh;
                z-index: 10;
                display: flex;
                flex-direction: column;
                align-items: center;
                /* Slide-in animation */
                transform: translateX(480px);
                opacity: 0;
                transition: transform 0.9s cubic-bezier(0.25, 0.46, 0.45, 0.94) 0.4s,
                            opacity 0.8s ease 0.4s;
            }}
            .profile-banner.visible {{
                transform: translateX(0);
                opacity: 1;
            }}

            /* Banner background image */
            .banner-bg {{
                position: absolute;
                top: 0; left: 0;
                width: 100%; height: 100%;
                z-index: -1;
                pointer-events: none;
            }}
            .banner-bg img {{
                width: 100%;
                height: 100%;
                object-fit: contain;
                object-position: top center;
                filter: brightness(0.85);
            }}

            /* ── Avatar area ── */
            .avatar-wrapper {{
                position: relative;
                margin-top: 50px;
                width: 100px;
                height: 100px;
                cursor: pointer;
            }}

            .avatar-circle {{
                width: 100px;
                height: 100px;
                border-radius: 50%;
                border: 3px solid rgba(252, 188, 215, 0.7);
                overflow: hidden;
                box-shadow: 0 0 18px 4px rgba(229, 106, 179, 0.25);
                transition: box-shadow 0.4s ease, border-color 0.4s ease;
            }}
            .avatar-circle img {{
                width: 100%;
                height: 100%;
                object-fit: cover;
            }}

            /* ── "Change icon" popup ── */
            .change-icon-popup {{
                display: none;
            }}

            /* ── Nickname ── */
            .nickname {{
                margin-top: 22px;
                font-family: 'Playfair Display', serif;
                font-size: 32px;
                color: #ffffff !important;
                text-align: center;
                letter-spacing: 1.5px;
                text-shadow: 0 2px 8px rgba(0,0,0,0.5);
                max-width: 352px;
                overflow: hidden;
                text-overflow: ellipsis;
                white-space: nowrap;
            }}

            /* ── Achievement slots ── */
            .achievements-row {{
                display: flex;
                justify-content: center;
                align-items: center;
                gap: 13px;
                margin-top: 198px;
            }}

            /* ─── ACHIEVEMENT ICON SIZE ───
               Change width/height below to resize the achievement circles.
               gap = spacing between them, margin-top = distance from nickname.
            */
            .achievement-slot {{
                width: 38px;
                height: 38px;
                border-radius: 50%;
                border: 2px solid rgba(252, 188, 215, 0.35);
                background: rgba(30, 10, 22, 0.45);
                display: flex;
                align-items: center;
                justify-content: center;
                overflow: visible;
                position: relative;
                transition: border-color 0.3s ease, box-shadow 0.3s ease, transform 0.3s ease;
                cursor: pointer;
            }}
            .achievement-slot:hover {{
                border-color: rgba(252, 188, 215, 0.7);
                box-shadow: 0 0 12px 3px rgba(229, 106, 179, 0.25);
                transform: scale(1.08);
            }}
            .achievement-slot img {{
                width: 60%;
                height: 60%;
                object-fit: contain;
                opacity: 0.5;
                filter: grayscale(1);
                transition: opacity 0.3s ease, filter 0.3s ease;
            }}
            .achievement-slot.earned img {{
                opacity: 1;
                filter: grayscale(0);
            }}

            /* ── Achievement tooltip ── */
            .achievement-tooltip {{
                position: absolute;
                bottom: calc(100% + 10px);
                left: 50%;
                transform: translateX(-50%) scale(0.9);
                background: rgba(18, 6, 14, 0.92);
                backdrop-filter: blur(12px);
                -webkit-backdrop-filter: blur(12px);
                border: 1px solid rgba(252, 188, 215, 0.2);
                border-radius: 10px;
                padding: 10px 14px;
                min-width: 160px;
                pointer-events: none;
                opacity: 0;
                transition: opacity 0.3s ease, transform 0.3s ease;
                z-index: 30;
            }}
            .achievement-slot:hover .achievement-tooltip {{
                opacity: 1;
                transform: translateX(-50%) scale(1);
            }}
            .tooltip-name {{
                font-family: 'Playfair Display', serif;
                font-size: 13px;
                color: #FCBCD7;
                letter-spacing: 1px;
                margin-bottom: 4px;
                text-align: center;
            }}
            .tooltip-desc {{
                font-family: 'Playfair Display', serif;
                font-size: 11px;
                color: rgba(252, 188, 215, 0.6);
                text-align: center;
                line-height: 1.3;
            }}

            .achievement-slot .lock-icon {{
                font-size: 21px;
                color: rgba(252, 188, 215, 0.3);
                user-select: none;
            }}

            /* ── Hidden file inputs ── */
            .avatar-file-input, .banner-file-input {{
                display: none;
            }}

            /* ── Back button ── */
            .back-btn {{
                position: absolute; top: 32px; right: 36px; z-index: 50;
                width: 44px; height: 44px; border-radius: 50%;
                background: rgba(252,188,215,0.06);
                border: 1px solid rgba(252,188,215,0.15);
                display: flex; align-items: center; justify-content: center;
                cursor: pointer; transition: all 0.3s ease;
                color: #FCBCD7; text-decoration: none;
            }}
            .back-btn svg {{ width: 24px; height: 24px; fill: currentColor; }}
            .back-btn:hover {{
                background: rgba(252,188,215,0.12);
                border-color: rgba(252,188,215,0.35);
                box-shadow: 0 0 16px rgba(191,80,130,0.3);
                transform: scale(1.08);
            }}

            /* ── Bottom navigation bar ── */
            .bottom-nav {{
                position: fixed;
                bottom: 0;
                left: 0;
                width: 100%;
                height: 432px;
                z-index: 20;
                display: flex;
                align-items: flex-end;
                justify-content: flex-start;
                gap: 60px;
                padding: 0 0 30px 30px;
                background: transparent;
                backdrop-filter: none;
                -webkit-backdrop-filter: none;
                border-top: none;
                pointer-events: none;
                transform: translateY(100%);
                opacity: 0;
                transition: transform 0.7s cubic-bezier(0.25, 0.46, 0.45, 0.94) 0.8s,
                            opacity 0.6s ease 0.8s;
            }}
            .bottom-nav.visible {{
                transform: translateY(0);
                opacity: 1;
            }}

            .nav-item {{
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: 12px;
                cursor: pointer;
                text-decoration: none;
                transition: transform 0.3s ease;
                user-select: none;
                -webkit-user-select: none;
                pointer-events: all;
                position: relative;
            }}
            .nav-item:hover {{
                transform: translateY(-4px);
            }}

            .nav-icon {{
                width: 150px;
                height: 150px;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 50%;
                border: 3px solid transparent;
                overflow: hidden;
                transition: transform 0.3s ease, filter 0.3s ease;
            }}
            .nav-item:hover .nav-icon {{
                transform: scale(1.05);
                filter: drop-shadow(0 0 10px rgba(229, 106, 179, 0.4));
            }}
            .nav-icon img {{
                width: 100%;
                height: 100%;
                object-fit: contain;
            }}

            .nav-label {{
                font-family: 'Playfair Display', serif;
                font-size: 28px;
                color: #8a6b7a;
                letter-spacing: 1.2px;
                text-align: center;
                transition: color 0.3s ease;
            }}
            .nav-item:hover .nav-label {{
                color: #a6889a;
            }}

            /* ── Settings icon rotation ── */
            @keyframes settingsRotate {{
                0%   {{ transform: rotate(0deg);   }}
                100% {{ transform: rotate(360deg); }}
            }}
            .nav-icon.rotating {{
                animation: settingsRotate 0.6s ease-in-out;
            }}

            /* ── Proficiency icon (no circle border) ── */
            .proficiency-icon {{
                width: 120px;
                height: 120px;
                border-radius: 0;
                border: none;
                box-shadow: none;
                overflow: visible;
            }}

            /* ── Settings sliding bars ── */
            .settings-bars {{
                position: absolute;
                bottom: 100%;
                left: -50px;
                display: flex;
                flex-direction: column;
                gap: -8px;
                padding-bottom: 10px;
                pointer-events: none;
            }}
            .settings-bars.open {{
                pointer-events: all;
            }}

            .settings-bar {{
                position: relative;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 12px 40px;
                background: url('/customisableprofile/defaultsettings/settingbar.png?v=2') no-repeat center center;
                background-size: 100% 100%;
                border: none;
                border-radius: 0;
                cursor: pointer;
                white-space: nowrap;
                font-family: 'Playfair Display', serif;
                font-size: 18px;
                color: #4d3040;
                letter-spacing: 1.2px;
                text-shadow: 0 2px 6px rgba(0, 0, 0, 0.7);
                transform: translateX(-120%);
                opacity: 0;
                transition: transform 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94),
                            opacity 0.4s ease,
                            filter 0.25s ease;
            }}
            .settings-bars.open .settings-bar {{
                transform: translateX(0);
                opacity: 1;
            }}
            .settings-bars.open .settings-bar:nth-child(1) {{ transition-delay: 0.06s; }}
            .settings-bars.open .settings-bar:nth-child(2) {{ transition-delay: 0.12s; }}
            .settings-bars.open .settings-bar:nth-child(3) {{ transition-delay: 0.18s; }}
            .settings-bars.open .settings-bar:nth-child(4) {{ transition-delay: 0.24s; }}
            .settings-bars.open .settings-bar:nth-child(5) {{ transition-delay: 0.30s; }}
            .settings-bars.open .settings-bar:nth-child(6) {{ transition-delay: 0.36s; }}
            .settings-bars.open .settings-bar:nth-child(7) {{ transition-delay: 0.42s; }}
            .settings-bars.open .settings-bar:nth-child(8) {{ transition-delay: 0.48s; }}

            .settings-bar:hover {{
                filter: brightness(0.75);
                color: #ffffff;
            }}

            /* ── Inventory selection modal ── */
            .inventory-modal {{
                position: fixed;
                top: 0; left: 0;
                width: 100%; height: 100%;
                z-index: 60;
                display: flex;
                align-items: center;
                justify-content: center;
                background: rgba(0,0,0,0.5);
                opacity: 0;
                pointer-events: none;
                transition: opacity 0.35s ease;
            }}
            .inventory-modal.open {{
                opacity: 1;
                pointer-events: all;
            }}
            .inventory-modal-box {{
                background: rgba(30, 10, 22, 0.95);
                border: 1px solid rgba(252, 188, 215, 0.25);
                border-radius: 14px;
                padding: 28px 32px;
                display: flex;
                flex-direction: column;
                gap: 16px;
                min-width: 320px;
                max-width: 480px;
                max-height: 70vh;
            }}
            .inventory-modal-box h3 {{
                font-family: 'Playfair Display', serif;
                font-size: 18px;
                color: #FCBCD7;
                letter-spacing: 1.5px;
                text-align: center;
                margin: 0;
            }}
            .inventory-grid {{
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 12px;
                overflow-y: auto;
                max-height: 50vh;
                padding: 4px;
            }}
            .inventory-item {{
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: 6px;
                padding: 10px 6px;
                border-radius: 10px;
                border: 1px solid rgba(252, 188, 215, 0.12);
                background: rgba(252, 188, 215, 0.04);
                cursor: pointer;
                transition: background 0.25s ease, border-color 0.25s ease, transform 0.2s ease;
            }}
            .inventory-item:hover {{
                background: rgba(229, 106, 179, 0.15);
                border-color: rgba(252, 188, 215, 0.4);
                transform: scale(1.05);
            }}
            .inventory-item img {{
                width: 64px;
                height: 64px;
                object-fit: contain;
                border-radius: 8px;
            }}
            .inventory-item span {{
                font-family: 'Playfair Display', serif;
                font-size: 11px;
                color: rgba(252, 188, 215, 0.7);
                text-align: center;
                letter-spacing: 0.5px;
            }}
            .inventory-empty {{
                font-family: 'Playfair Display', serif;
                font-size: 14px;
                color: rgba(252, 188, 215, 0.5);
                text-align: center;
                padding: 32px 16px;
                line-height: 1.6;
                letter-spacing: 0.8px;
            }}
            .inventory-close {{
                align-self: center;
                padding: 8px 24px;
                font-family: 'Playfair Display', serif;
                font-size: 13px;
                color: rgba(252, 188, 215, 0.6);
                background: transparent;
                border: 1px solid rgba(252, 188, 215, 0.3);
                border-radius: 8px;
                cursor: pointer;
                letter-spacing: 0.8px;
                transition: background 0.25s ease;
            }}
            .inventory-close:hover {{
                background: rgba(252, 188, 215, 0.08);
            }}

            /* ── Nickname edit modal ── */
            .nickname-modal {{
                position: fixed;
                top: 0; left: 0;
                width: 100%; height: 100%;
                z-index: 60;
                display: flex;
                align-items: center;
                justify-content: center;
                background: rgba(0,0,0,0.5);
                opacity: 0;
                pointer-events: none;
                transition: opacity 0.35s ease;
            }}
            .nickname-modal.open {{
                opacity: 1;
                pointer-events: all;
            }}
            .nickname-modal-box {{
                background: rgba(30, 10, 22, 0.95);
                border: 1px solid rgba(252, 188, 215, 0.25);
                border-radius: 14px;
                padding: 28px 32px;
                display: flex;
                flex-direction: column;
                gap: 16px;
                min-width: 280px;
            }}
            .nickname-modal-box h3 {{
                font-family: 'Playfair Display', serif;
                color: #FCBCD7;
                font-size: 16px;
                letter-spacing: 1px;
                margin: 0;
            }}
            .nickname-modal-box input {{
                font-family: 'Playfair Display', serif;
                font-size: 14px;
                padding: 8px 14px;
                border-radius: 8px;
                border: 1px solid rgba(252, 188, 215, 0.3);
                background: rgba(18, 6, 14, 0.7);
                color: #FCBCD7;
                outline: none;
                transition: border-color 0.3s ease;
            }}
            .nickname-modal-box input:focus {{
                border-color: rgba(252, 188, 215, 0.7);
            }}
            .nickname-modal-btns {{
                display: flex;
                gap: 10px;
                justify-content: flex-end;
            }}
            .nickname-modal-btns button {{
                font-family: 'Playfair Display', serif;
                font-size: 12px;
                padding: 6px 18px;
                border-radius: 8px;
                border: 1px solid rgba(252, 188, 215, 0.3);
                cursor: pointer;
                letter-spacing: 0.8px;
                transition: background 0.25s ease;
            }}
            .btn-cancel {{
                background: transparent;
                color: rgba(252, 188, 215, 0.6);
            }}
            .btn-cancel:hover {{
                background: rgba(252, 188, 215, 0.08);
            }}
            .btn-save {{
                background: rgba(229, 106, 179, 0.35);
                color: #FCBCD7;
            }}
            .btn-save:hover {{
                background: rgba(229, 106, 179, 0.55);
            }}

            /* ── Generic settings modal (password / email) ── */
            .settings-overlay {{
                position: fixed;
                top: 0; left: 0;
                width: 100%; height: 100%;
                z-index: 70;
                display: flex;
                align-items: center;
                justify-content: center;
                background: radial-gradient(ellipse at center, rgba(0,0,0,0.3) 0%, rgba(0,0,0,0.85) 100%);
                backdrop-filter: blur(6px);
                -webkit-backdrop-filter: blur(6px);
                opacity: 0;
                pointer-events: none;
                transition: opacity 0.45s ease;
            }}
            .settings-overlay.open {{
                opacity: 1;
                pointer-events: all;
            }}
            .settings-modal-box {{
                background: rgba(30, 10, 22, 0.96);
                border: 1px solid rgba(252, 188, 215, 0.25);
                border-radius: 14px;
                padding: 32px 36px;
                display: flex;
                flex-direction: column;
                gap: 18px;
                min-width: 320px;
                max-width: 400px;
                transform: scale(0.92);
                transition: transform 0.35s ease;
            }}
            .settings-overlay.open .settings-modal-box {{
                transform: scale(1);
            }}
            .settings-modal-box h3 {{
                font-family: 'Playfair Display', serif;
                color: #FCBCD7;
                font-size: 18px;
                letter-spacing: 1.2px;
                margin: 0;
                text-align: center;
            }}
            .settings-modal-box label {{
                font-family: 'Playfair Display', serif;
                font-size: 12px;
                color: rgba(252, 188, 215, 0.6);
                letter-spacing: 0.8px;
                margin-bottom: -12px;
            }}
            .settings-modal-box input {{
                font-family: 'Playfair Display', serif;
                font-size: 14px;
                padding: 10px 14px;
                border-radius: 8px;
                border: 1px solid rgba(252, 188, 215, 0.3);
                background: rgba(18, 6, 14, 0.7);
                color: #FCBCD7;
                outline: none;
                transition: border-color 0.3s ease;
            }}
            .settings-modal-box input:focus {{
                border-color: rgba(252, 188, 215, 0.7);
            }}
            .settings-modal-error {{
                font-family: 'Playfair Display', serif;
                font-size: 12px;
                color: #e56a8a;
                text-align: center;
                min-height: 16px;
                letter-spacing: 0.5px;
                transition: opacity 0.3s ease;
            }}
            .settings-modal-btns {{
                display: flex;
                gap: 10px;
                justify-content: flex-end;
                margin-top: 4px;
            }}
            .settings-modal-btns button {{
                font-family: 'Playfair Display', serif;
                font-size: 13px;
                padding: 8px 22px;
                border-radius: 8px;
                border: 1px solid rgba(252, 188, 215, 0.3);
                cursor: pointer;
                letter-spacing: 0.8px;
                transition: background 0.25s ease;
            }}

            /* ── Confirmation overlay ── */
            .confirm-overlay {{
                position: fixed;
                top: 0; left: 0;
                width: 100%; height: 100%;
                z-index: 80;
                display: flex;
                align-items: center;
                justify-content: center;
                background: radial-gradient(ellipse at center, rgba(0,0,0,0.3) 0%, rgba(0,0,0,0.85) 100%);
                backdrop-filter: blur(6px);
                -webkit-backdrop-filter: blur(6px);
                opacity: 0;
                pointer-events: none;
                transition: opacity 0.45s ease;
            }}
            .confirm-overlay.open {{
                opacity: 1;
                pointer-events: all;
            }}
            .confirm-box {{
                background: rgba(30, 10, 22, 0.96);
                border: 1px solid rgba(252, 188, 215, 0.25);
                border-radius: 14px;
                padding: 32px 36px;
                display: flex;
                flex-direction: column;
                gap: 20px;
                min-width: 300px;
                max-width: 420px;
                transform: scale(0.92);
                transition: transform 0.35s ease;
            }}
            .confirm-overlay.open .confirm-box {{
                transform: scale(1);
            }}
            .confirm-box p {{
                font-family: 'Playfair Display', serif;
                font-size: 14px;
                color: rgba(252, 188, 215, 0.85);
                text-align: center;
                line-height: 1.6;
                letter-spacing: 0.5px;
                margin: 0;
            }}
            .confirm-btns {{
                display: flex;
                gap: 10px;
                justify-content: center;
            }}
            .confirm-btns button {{
                font-family: 'Playfair Display', serif;
                font-size: 13px;
                padding: 8px 22px;
                border-radius: 8px;
                border: 1px solid rgba(252, 188, 215, 0.3);
                cursor: pointer;
                letter-spacing: 0.8px;
                transition: background 0.25s ease;
            }}

            /* ── Sliding collection panel ── */
            .sliding-panel-overlay {{
                position: fixed;
                top: 0; left: 0;
                width: 100%; height: 100%;
                z-index: 65;
                background: rgba(0,0,0,0.4);
                opacity: 0;
                pointer-events: none;
                transition: opacity 0.4s ease;
            }}
            .sliding-panel-overlay.open {{
                opacity: 1;
                pointer-events: all;
            }}
            .sliding-panel {{
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%) scale(0.9);
                height: 90vh;
                width: calc(90vh * 0.8027);
                min-width: 450px;
                z-index: 66;
                opacity: 0;
                pointer-events: none;
                transition: opacity 0.45s ease, transform 0.45s cubic-bezier(0.25, 0.46, 0.45, 0.94);
                display: flex;
                flex-direction: column;
            }}
            .sliding-panel.open {{
                opacity: 1;
                pointer-events: all;
                transform: translate(-50%, -50%) scale(1);
            }}
            .sliding-panel-border {{
                position: absolute;
                top: 0; left: 0;
                width: 100%; height: 100%;
                pointer-events: none;
                z-index: 1;
            }}
            .sliding-panel-border img {{
                width: 100%; height: 100%;
                object-fit: fill;
            }}
            .sliding-panel-inner {{
                position: absolute;
                z-index: 2;
                top: 17.1%;
                left: 8.5%;
                width: 83.8%;
                height: 61%;
                display: flex;
                flex-direction: column;
                gap: 14px;
                overflow: hidden;
                padding: 10px;
            }}
            .sliding-panel-inner h3 {{
                font-family: 'Playfair Display', serif;
                font-size: 20px;
                color: #ffffff;
                letter-spacing: 1.5px;
                text-align: center;
                margin: 0;
                text-shadow: 0 1px 4px rgba(0,0,0,0.3);
            }}
            .sliding-panel-scroll {{
                overflow-y: auto;
                flex: 1;
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 18px;
                padding: 0;
                background: transparent;
                border-radius: 0;
                border: none;
                align-content: start;
            }}
            .sliding-panel-scroll::-webkit-scrollbar {{
                width: 6px;
            }}
            .sliding-panel-scroll::-webkit-scrollbar-track {{
                background: rgba(77, 48, 64, 0.1);
                border-radius: 3px;
            }}
            .sliding-panel-scroll::-webkit-scrollbar-thumb {{
                background: rgba(77, 48, 64, 0.3);
                border-radius: 3px;
            }}
            .sliding-item {{
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: 10px;
                padding: 16px 12px;
                border-radius: 10px;
                background: transparent;
                border: 1px solid rgba(255, 255, 255, 0.15);
                cursor: pointer;
                transition: background 0.25s ease, transform 0.2s ease, box-shadow 0.25s ease;
                position: relative;
            }}
            .sliding-item:hover {{
                background: rgba(255, 255, 255, 0.1);
                transform: scale(1.05);
                box-shadow: 0 4px 16px rgba(255, 255, 255, 0.1);
            }}
            .sliding-item img {{
                width: 100%;
                height: auto;
                object-fit: contain;
                border-radius: 8px;
            }}
            .sliding-item-title {{
                font-family: 'Playfair Display', serif;
                font-size: 14px;
                color: #ffffff;
                text-align: center;
                letter-spacing: 0.5px;
                line-height: 1.3;
            }}
            .sliding-empty {{
                grid-column: 1 / -1;
                font-family: 'Playfair Display', serif;
                font-size: 15px;
                color: rgba(255, 255, 255, 0.5);
                text-align: center;
                padding: 40px 16px;
                letter-spacing: 1px;
            }}
            .sliding-close-btn {{
                align-self: center;
                margin-top: -8px;
                padding: 0;
                font-family: 'Playfair Display', serif;
                font-size: 14px;
                color: #ffffff;
                background: transparent;
                border: none;
                cursor: pointer;
                letter-spacing: 0.8px;
                transition: opacity 0.25s ease;
                z-index: 2;
                text-shadow: 0 1px 4px rgba(0,0,0,0.3);
            }}
            .sliding-close-btn:hover {{
                opacity: 0.7;
            }}

            /* ── Gem hover popup ── */
            .gem-hover-popup {{
                position: absolute;
                bottom: calc(100% + 8px);
                left: 50%;
                transform: translateX(-50%) scale(0.9);
                background: rgba(18, 6, 14, 0.92);
                backdrop-filter: blur(10px);
                -webkit-backdrop-filter: blur(10px);
                border: 1px solid rgba(252, 188, 215, 0.25);
                border-radius: 10px;
                padding: 10px 14px;
                min-width: 150px;
                max-width: 220px;
                font-family: 'Playfair Display', serif;
                font-size: 11px;
                color: rgba(252, 188, 215, 0.85);
                text-align: center;
                line-height: 1.4;
                letter-spacing: 0.4px;
                pointer-events: none;
                opacity: 0;
                transition: opacity 0.3s ease, transform 0.3s ease;
                z-index: 100;
                white-space: normal;
            }}
            .gem-item:hover .gem-hover-popup {{
                opacity: 1;
                transform: translateX(-50%) scale(1);
            }}
        </style>
    </head>
    <body>
        <!-- Full-screen temple background -->
        <div class="bg-layer"></div>

        <!-- Back button -->
        <a class="back-btn" href="/welcome#selection" title="Back to Menu"><svg viewBox="0 0 24 24"><path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z"/></svg></a>

        <!-- Right-side vertical banner -->
        <div class="profile-banner" id="profileBanner">
            <!-- Banner background -->
            <div class="banner-bg">
                <img src="{banner_url}" alt="banner" id="bannerImg">
            </div>

            <!-- Avatar -->
            <div class="avatar-wrapper" id="avatarWrapper">
                <div class="avatar-circle">
                    <img src="{avatar_url}" alt="avatar" id="avatarImg">
                </div>
                <div class="change-icon-popup" id="changeIconPopup">change icon</div>
            </div>

            <!-- Nickname -->
            <div class="nickname" id="nicknameDisplay" style="color: #ffffff;">{nickname if nickname else user_name}</div>

            <!-- Achievement slots (3 circular badges with tooltips) -->
            <div class="achievements-row">
                {achievement_slots_html}
            </div>

            <!-- Hidden file inputs -->
            <input type="file" class="avatar-file-input" id="avatarInput" accept="image/*">
            <input type="file" class="banner-file-input" id="bannerInput" accept="image/*">
        </div>

        <!-- Bottom navigation bar -->
        <div class="bottom-nav" id="bottomNav">
            <!-- 1) Settings (click to toggle) -->
            <div class="nav-item" id="settingsBtn" title="Settings for your profile and gathered currencies">
                <div class="nav-icon" id="settingsIcon">
                    <img src="/customisableprofile/defaultsettings/settingkey.png?v=2" alt="settings">
                </div>
                <span class="nav-label">Settings</span>
                <!-- Settings bars that slide out -->
                <div class="settings-bars" id="settingsBars">
                    <div class="settings-bar" id="settChangeName">Change Name</div>
                    <div class="settings-bar" id="settChangeBanner">Change Banner</div>
                    <div class="settings-bar" id="settChangeGems">Change Gems</div>
                    <div class="settings-bar" id="settChangeEmail">Change Email</div>
                    <div class="settings-bar" id="settChangePassword">Change Password</div>
                    <div class="settings-bar" id="settViewPlan">View Plan</div>
                    <div class="settings-bar" id="settSubscriptions">Subscriptions</div>
                    <div class="settings-bar" id="settLogout">Logout</div>
                </div>
            </div>

            <!-- 2) Proficiency Level -->
            <a class="nav-item" href="#" title="Your current level of japanese based on your progress in the courses">
                <div class="nav-icon proficiency-icon">
                    <img src="/customisableprofile/defaultsettings/{current_level}.png?v=2" alt="{current_level}">
                </div>
                <span class="nav-label">Proficiency</span>
            </a>

            <!-- 3) Achievements Book -->
            <a class="nav-item" href="/achievements" title="Your book of events commemoration">
                <div class="nav-icon">
                    <img src="/customisableprofile/defaultsettings/book.png?v=2" alt="achievements">
                </div>
                <span class="nav-label">Achievements</span>
            </a>
        </div>

        <!-- Banner selection modal -->
        <div class="inventory-modal" id="bannerSelectModal">
            <div class="inventory-modal-box">
                <h3>Your Banners</h3>
                <div class="inventory-grid" id="bannerGrid">
                    {owned_banners_html}
                </div>
                <button class="inventory-close" id="bannerSelectClose">Close</button>
            </div>
        </div>

        <!-- Achievement selection modal -->
        <div class="inventory-modal" id="achSelectModal">
            <div class="inventory-modal-box">
                <h3>Your Achievements</h3>
                <div class="inventory-grid" id="achGrid">
                    {owned_achievements_html}
                </div>
                <button class="inventory-close" id="achSelectClose">Close</button>
            </div>
        </div>

        <!-- Nickname edit modal -->
        <div class="nickname-modal" id="nicknameModal">
            <div class="nickname-modal-box">
                <h3>Change Nickname</h3>
                <input type="text" id="nicknameInput" value="{nickname if nickname else user_name}" maxlength="24" placeholder="Enter new nickname">
                <div class="nickname-modal-btns">
                    <button class="btn-cancel" id="nickCancel">Cancel</button>
                    <button class="btn-save" id="nickSave">Save</button>
                </div>
            </div>
        </div>

        <!-- Change Password modal -->
        <div class="settings-overlay" id="passwordOverlay">
            <div class="settings-modal-box">
                <h3>Change Password</h3>
                <label>Current Password</label>
                <input type="password" id="currentPasswordInput" placeholder="Enter current password">
                <label>New Password</label>
                <input type="password" id="newPasswordInput" placeholder="Enter new password">
                <div class="settings-modal-error" id="passwordError"></div>
                <div class="settings-modal-btns">
                    <button class="btn-cancel" id="passwordCancel">Cancel</button>
                    <button class="btn-save" id="passwordSave">Save</button>
                </div>
            </div>
        </div>

        <!-- Change Email modal -->
        <div class="settings-overlay" id="emailOverlay">
            <div class="settings-modal-box">
                <h3>Change Email</h3>
                <label>Current Email</label>
                <input type="email" id="currentEmailInput" placeholder="Enter current email">
                <label>New Email</label>
                <input type="email" id="newEmailInput" placeholder="Enter new email">
                <div class="settings-modal-error" id="emailError"></div>
                <div class="settings-modal-btns">
                    <button class="btn-cancel" id="emailCancel">Cancel</button>
                    <button class="btn-save" id="emailSave">OK</button>
                </div>
            </div>
        </div>

        <!-- Email confirmation overlay -->
        <div class="confirm-overlay" id="emailConfirmOverlay">
            <div class="confirm-box">
                <p>Are you sure you want to change your email? You will be getting offers and notifications for upcoming courses on the new email.</p>
                <div class="confirm-btns">
                    <button class="btn-cancel" id="emailConfirmNo">Cancel</button>
                    <button class="btn-save" id="emailConfirmYes">Confirm</button>
                </div>
            </div>
        </div>

        <!-- Sliding Banner Panel -->
        <div class="sliding-panel-overlay" id="bannerPanelOverlay"></div>
        <div class="sliding-panel" id="bannerPanel">
            <div class="sliding-panel-border">
                <img src="/customisableprofile/defaultsettings/bordercollections.png" alt="border">
            </div>
            <div class="sliding-panel-inner">
                <h3>Your Banners</h3>
                <div class="sliding-panel-scroll" id="slidingBannerGrid">
                    {sliding_banners_html}
                </div>
                <button class="sliding-close-btn" id="bannerPanelClose">Close</button>
            </div>
        </div>

        <!-- Sliding Gems Panel -->
        <div class="sliding-panel-overlay" id="gemsPanelOverlay"></div>
        <div class="sliding-panel" id="gemsPanel">
            <div class="sliding-panel-border">
                <img src="/customisableprofile/defaultsettings/bordercollections.png" alt="border">
            </div>
            <div class="sliding-panel-inner">
                <h3>Your Gems</h3>
                <div class="sliding-panel-scroll" id="slidingGemsGrid">
                    {sliding_gems_html}
                </div>
                <button class="sliding-close-btn" id="gemsPanelClose">Close</button>
            </div>
        </div>

        <script>
            /* ── Page load animation ── */
            window.addEventListener('load', () => {{
                document.body.classList.add('loaded');
                setTimeout(() => {{
                    document.getElementById('profileBanner').classList.add('visible');
                }}, 200);
                setTimeout(() => {{
                    document.getElementById('bottomNav').classList.add('visible');
                }}, 300);
            }});

            /* ── Click avatar to change profile image ── */
            const avatarWrapper = document.getElementById('avatarWrapper');
            const avatarInput   = document.getElementById('avatarInput');

            avatarWrapper.addEventListener('click', () => {{
                avatarInput.click();
            }});

            /* Upload chosen avatar */
            avatarInput.addEventListener('change', async () => {{
                const file = avatarInput.files[0];
                if (!file) return;
                const formData = new FormData();
                formData.append('avatar', file);
                try {{
                    const res = await fetch('/profile/update-avatar', {{
                        method: 'POST',
                        body: formData
                    }});
                    if (res.ok) {{
                        const data = await res.json();
                        document.getElementById('avatarImg').src = data.avatar_url + '?t=' + Date.now();
                    }}
                }} catch (err) {{
                    console.error('Avatar upload failed', err);
                }}
            }});

            /* ══════════════════════════════════════
               SETTINGS — click gear to toggle
               ══════════════════════════════════════ */
            const settingsBtn     = document.getElementById('settingsBtn');
            const settingsIcon    = document.getElementById('settingsIcon');
            const settingsBars    = document.getElementById('settingsBars');
            let settingsOpen = false;

            function toggleSettings(e) {{
                e.preventDefault();
                e.stopPropagation();
                settingsOpen = !settingsOpen;
                if (settingsOpen) {{
                    settingsBars.classList.add('open');
                    settingsIcon.classList.add('rotating');
                    settingsIcon.addEventListener('animationend', () => {{
                        settingsIcon.classList.remove('rotating');
                    }}, {{ once: true }});
                }} else {{
                    settingsBars.classList.remove('open');
                    settingsIcon.classList.add('rotating');
                    settingsIcon.addEventListener('animationend', () => {{
                        settingsIcon.classList.remove('rotating');
                    }}, {{ once: true }});
                }}
            }}

            settingsIcon.addEventListener('click', toggleSettings);
            document.querySelector('#settingsBtn > .nav-label').addEventListener('click', toggleSettings);

            /* Close bars when clicking elsewhere */
            document.addEventListener('click', (e) => {{
                if (settingsOpen && !settingsBtn.contains(e.target)) {{
                    settingsOpen = false;
                    settingsBars.classList.remove('open');
                }}
            }});

            /* ── Setting: Change Name ── */
            const nicknameModal = document.getElementById('nicknameModal');
            const nicknameInput = document.getElementById('nicknameInput');

            document.getElementById('settChangeName').addEventListener('click', (e) => {{
                e.stopPropagation();
                settingsOpen = false;
                settingsBars.classList.remove('open');
                setTimeout(() => {{ nicknameModal.classList.add('open'); }}, 350);
            }});

            /* ── Setting: Change Banner ── */
            const bannerInput = document.getElementById('bannerInput');
            const bannerPanel = document.getElementById('bannerPanel');
            const bannerPanelOverlay = document.getElementById('bannerPanelOverlay');

            document.getElementById('settChangeBanner').addEventListener('click', (e) => {{
                e.stopPropagation();
                settingsOpen = false;
                settingsBars.classList.remove('open');
                setTimeout(() => {{
                    bannerPanelOverlay.classList.add('open');
                    bannerPanel.classList.add('open');
                }}, 350);
            }});
            document.getElementById('bannerPanelClose').addEventListener('click', () => {{
                bannerPanel.classList.remove('open');
                bannerPanelOverlay.classList.remove('open');
            }});
            bannerPanelOverlay.addEventListener('click', () => {{
                bannerPanel.classList.remove('open');
                bannerPanelOverlay.classList.remove('open');
            }});
            /* Click a banner in sliding panel to equip it */
            document.querySelectorAll('#slidingBannerGrid .sliding-item').forEach(item => {{
                item.addEventListener('click', async () => {{
                    const bannerId = item.dataset.id;
                    try {{
                        const res = await fetch('/profile/equip-banner', {{
                            method: 'POST',
                            headers: {{ 'Content-Type': 'application/json' }},
                            body: JSON.stringify({{ item_id: parseInt(bannerId) }})
                        }});
                        if (res.ok) {{
                            const data = await res.json();
                            document.getElementById('bannerImg').src = data.banner_url + '?t=' + Date.now();
                            bannerPanel.classList.remove('open');
                            bannerPanelOverlay.classList.remove('open');
                        }}
                    }} catch (err) {{
                        console.error('Equip banner failed', err);
                    }}
                }});
            }});

            /* ── Setting: Change Gems ── */
            const gemsPanel = document.getElementById('gemsPanel');
            const gemsPanelOverlay = document.getElementById('gemsPanelOverlay');

            document.getElementById('settChangeGems').addEventListener('click', (e) => {{
                e.stopPropagation();
                settingsOpen = false;
                settingsBars.classList.remove('open');
                setTimeout(() => {{
                    gemsPanelOverlay.classList.add('open');
                    gemsPanel.classList.add('open');
                }}, 350);
            }});
            document.getElementById('gemsPanelClose').addEventListener('click', () => {{
                gemsPanel.classList.remove('open');
                gemsPanelOverlay.classList.remove('open');
            }});
            gemsPanelOverlay.addEventListener('click', () => {{
                gemsPanel.classList.remove('open');
                gemsPanelOverlay.classList.remove('open');
            }});
            /* Click a gem/achievement in sliding panel to equip it */
            document.querySelectorAll('#slidingGemsGrid .sliding-item').forEach(item => {{
                item.addEventListener('click', async () => {{
                    const achId = item.dataset.id;
                    try {{
                        const res = await fetch('/profile/equip-achievement', {{
                            method: 'POST',
                            headers: {{ 'Content-Type': 'application/json' }},
                            body: JSON.stringify({{ achievement_id: parseInt(achId), slot: 0 }})
                        }});
                        if (res.ok) {{
                            gemsPanel.classList.remove('open');
                            gemsPanelOverlay.classList.remove('open');
                            location.reload();
                        }}
                    }} catch (err) {{
                        console.error('Equip achievement failed', err);
                    }}
                }});
            }});

            /* ── Setting: Change Email ── */
            const emailOverlay = document.getElementById('emailOverlay');
            const emailConfirmOverlay = document.getElementById('emailConfirmOverlay');
            const currentEmailInput = document.getElementById('currentEmailInput');
            const newEmailInput = document.getElementById('newEmailInput');
            const emailError = document.getElementById('emailError');
            let pendingEmailData = null;

            document.getElementById('settChangeEmail').addEventListener('click', (e) => {{
                e.stopPropagation();
                settingsOpen = false;
                settingsBars.classList.remove('open');
                currentEmailInput.value = '';
                newEmailInput.value = '';
                emailError.textContent = '';
                setTimeout(() => {{ emailOverlay.classList.add('open'); }}, 350);
            }});
            document.getElementById('emailCancel').addEventListener('click', () => {{
                emailOverlay.classList.remove('open');
            }});
            document.getElementById('emailSave').addEventListener('click', () => {{
                const curEmail = currentEmailInput.value.trim();
                const newEmail = newEmailInput.value.trim();
                if (!curEmail || !newEmail) {{ emailError.textContent = 'Please fill in both fields.'; return; }}
                emailError.textContent = '';
                pendingEmailData = {{ current_email: curEmail, new_email: newEmail }};
                emailConfirmOverlay.classList.add('open');
            }});
            document.getElementById('emailConfirmNo').addEventListener('click', () => {{
                emailConfirmOverlay.classList.remove('open');
            }});
            document.getElementById('emailConfirmYes').addEventListener('click', async () => {{
                if (!pendingEmailData) return;
                try {{
                    const res = await fetch('/profile/change-email', {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify(pendingEmailData)
                    }});
                    if (res.ok) {{
                        emailConfirmOverlay.classList.remove('open');
                        emailOverlay.classList.remove('open');
                        window.location.href = '/profile';
                    }} else {{
                        const data = await res.json();
                        emailConfirmOverlay.classList.remove('open');
                        emailError.textContent = data.detail || 'Failed to change email.';
                    }}
                }} catch (err) {{
                    emailConfirmOverlay.classList.remove('open');
                    emailError.textContent = 'Something went wrong.';
                }}
            }});

            /* ── Setting: Change Password ── */
            const passwordOverlay = document.getElementById('passwordOverlay');
            const currentPasswordInput = document.getElementById('currentPasswordInput');
            const newPasswordInput = document.getElementById('newPasswordInput');
            const passwordError = document.getElementById('passwordError');

            document.getElementById('settChangePassword').addEventListener('click', (e) => {{
                e.stopPropagation();
                settingsOpen = false;
                settingsBars.classList.remove('open');
                currentPasswordInput.value = '';
                newPasswordInput.value = '';
                passwordError.textContent = '';
                setTimeout(() => {{ passwordOverlay.classList.add('open'); }}, 350);
            }});
            document.getElementById('passwordCancel').addEventListener('click', () => {{
                passwordOverlay.classList.remove('open');
            }});
            document.getElementById('passwordSave').addEventListener('click', async () => {{
                const curPass = currentPasswordInput.value;
                const newPass = newPasswordInput.value;
                if (!curPass || !newPass) {{ passwordError.textContent = 'Please fill in both fields.'; return; }}
                if (newPass.length < 4) {{ passwordError.textContent = 'New password must be at least 4 characters.'; return; }}
                passwordError.textContent = '';
                try {{
                    const res = await fetch('/profile/change-password', {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify({{ current_password: curPass, new_password: newPass }})
                    }});
                    if (res.ok) {{
                        passwordOverlay.classList.remove('open');
                        window.location.href = '/profile';
                    }} else {{
                        const data = await res.json();
                        passwordError.textContent = data.detail || 'Failed to change password.';
                    }}
                }} catch (err) {{
                    passwordError.textContent = 'Something went wrong.';
                }}
            }});
            newPasswordInput.addEventListener('keydown', (e) => {{
                if (e.key === 'Enter') document.getElementById('passwordSave').click();
            }});

            /* ── Setting: View Plan ── */
            document.getElementById('settViewPlan').addEventListener('click', (e) => {{
                e.stopPropagation();
                settingsOpen = false;
                settingsBars.classList.remove('open');
                alert('View Plan – coming soon!');
            }});

            /* ── Setting: Subscriptions ── */
            document.getElementById('settSubscriptions').addEventListener('click', (e) => {{
                e.stopPropagation();
                settingsOpen = false;
                settingsBars.classList.remove('open');
                alert('Subscriptions – coming soon!');
            }});

            /* ── Setting: Logout ── */
            document.getElementById('settLogout').addEventListener('click', (e) => {{
                e.stopPropagation();
                settingsOpen = false;
                settingsBars.classList.remove('open');
                document.cookie = 'user_email=; Max-Age=0; path=/';
                window.location.href = '/login';
            }});

            document.getElementById('nickCancel').addEventListener('click', () => {{
                nicknameModal.classList.remove('open');
            }});

            document.getElementById('nickSave').addEventListener('click', async () => {{
                const newNick = nicknameInput.value.trim();
                if (!newNick) return;
                try {{
                    const res = await fetch('/profile/update-nickname', {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify({{ nickname: newNick }})
                    }});
                    if (res.ok) {{
                        document.getElementById('nicknameDisplay').textContent = newNick;
                        nicknameModal.classList.remove('open');
                    }}
                }} catch (err) {{
                    console.error('Nickname update failed', err);
                }}
            }});

            /* Enter key saves nickname */
            nicknameInput.addEventListener('keydown', (e) => {{
                if (e.key === 'Enter') document.getElementById('nickSave').click();
            }});
        </script>
    </body>
    </html>
    """
