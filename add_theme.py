import glob
import re

fampay_css = """
    [data-theme="fampay"] {
      --black:        #000000;
      --surface:      #0E0F12;
      --surface-hi:   #16181D;
      --surface-hir:  #1F2229;
      --border:       #2A2D34;
      --border-s:     #3A3E47;
      --text-1:       #FFFFFF;
      --text-2:       #9BA1A8;
      --text-3:       #5A6068;
      --lime:         #FFC700;
      --lime-dim:     #E6B300;
      --pattern-color: rgba(255, 199, 0, 0.04);
      --nav-bg:       rgba(0,0,0,0.88);
    }
"""

for filepath in glob.glob('website/*.html'):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace the old light theme block
    content = re.sub(r'\[data-theme="light"\]\s*\{[^}]+\}', fampay_css.strip(), content)

    # In JS, change toggle logic
    # Find: let newTheme = (theme === 'dark' || !theme) ? 'light' : 'dark';
    content = content.replace("let newTheme = (theme === 'dark' || !theme) ? 'light' : 'dark';", "let newTheme = (theme === 'dark' || !theme) ? 'fampay' : 'dark';")

    # Change emoji
    content = content.replace("🌓", "🟨")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Updated {filepath}')
