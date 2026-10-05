import glob
import re

css_toggle = """
    /* ─── Perfect Theme Toggle ─── */
    .theme-switch {
      position: relative;
      display: inline-flex;
      align-items: center;
      width: 48px;
      height: 24px;
      margin-right: 12px;
      -webkit-tap-highlight-color: transparent;
    }
    .theme-switch input {
      opacity: 0;
      width: 0;
      height: 0;
    }
    .theme-switch .slider {
      position: absolute;
      cursor: pointer;
      top: 0; left: 0; right: 0; bottom: 0;
      background-color: var(--surface-hir);
      transition: .4s cubic-bezier(0.4, 0.0, 0.2, 1);
      border-radius: 30px;
      border: 1px solid var(--border-s);
      box-shadow: inset 0 2px 4px rgba(0,0,0,0.4);
    }
    .theme-switch .slider:before {
      position: absolute;
      content: "";
      height: 16px;
      width: 16px;
      left: 3px;
      bottom: 3px;
      background-color: var(--lime);
      transition: .4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
      border-radius: 50%;
      box-shadow: 0 2px 5px rgba(0,0,0,0.5);
    }
    .theme-switch input:checked + .slider {
      background-color: #1A1C20;
      border-color: rgba(255, 255, 255, 0.1);
    }
    .theme-switch input:checked + .slider:before {
      transform: translateX(24px);
    }
"""

js_toggle = """
  // Perfect Theme Toggle Logic
  const themeToggleCheckbox = document.getElementById('theme-toggle');
  if (themeToggleCheckbox) {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    themeToggleCheckbox.checked = currentTheme === 'fampay';
    
    themeToggleCheckbox.addEventListener('change', (e) => {
      let newTheme = e.target.checked ? 'fampay' : 'dark';
      document.documentElement.setAttribute('data-theme', newTheme);
      localStorage.setItem('theme', newTheme);
    });
  }
"""

for filepath in glob.glob('website/*.html'):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Insert CSS
    if '.theme-switch {' not in content:
        # Insert before layout helpers
        content = content.replace('/* ─── layout helpers ─── */', css_toggle + '\n    /* ─── layout helpers ─── */')

    # 2. Replace button HTML
    old_btn_regex = r'<button class="theme-toggle".*?>.*?</button>'
    new_html = '<label class="theme-switch" aria-label="Toggle Theme" title="Toggle FamApp/NeoPOP Theme">\n        <input type="checkbox" id="theme-toggle">\n        <span class="slider"></span>\n      </label>'
    content = re.sub(old_btn_regex, new_html, content)

    # 3. Replace JS
    old_js_regex = r'// Theme Toggle Logic[\s\S]*?\}\);[\s\S]*?\}'
    content = re.sub(old_js_regex, js_toggle.strip(), content)
    
    # Check if there is an old JS block that didn't match the regex precisely
    if 'themeToggleBtn.addEventListener' in content:
         # Fallback manual replace if regex failed
         pass

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Updated {filepath}')
