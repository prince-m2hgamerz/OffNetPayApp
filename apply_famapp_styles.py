import glob
import re

# We will refactor the root CSS and component CSS to support dynamic shapes/shadows
# First, let's define the new base variables for both themes.

for filepath in glob.glob('website/*.html'):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update :root to include layout variables
    if '--btn-radius' not in content:
        content = content.replace(
            ':root {',
            ':root {\n      --btn-radius: 0px;\n      --card-radius: 0px;\n      --btn-shadow: 3px 3px 0 var(--lime-dim);\n      --btn-shadow-hover: 4px 4px 0 var(--lime-dim);\n      --btn-shadow-active: none;\n      --btn-translate-hover: translate(-1px, -1px);\n      --btn-translate-active: translate(3px, 3px);\n      --card-bg: transparent;\n      --card-border: 1px solid var(--border);\n      --font-weight-headings: 800;'
        )

    # 2. Update [data-theme="fampay"] to include FamApp style overrides
    if '--btn-radius: 50px;' not in content:
        fampay_css_new = """[data-theme="fampay"] {
      --black:        #000000;
      --surface:      #0E0F12;
      --surface-hi:   #1A1C20;
      --surface-hir:  #282A30;
      --border:       rgba(255, 255, 255, 0.08);
      --border-s:     rgba(255, 255, 255, 0.12);
      --text-1:       #FFFFFF;
      --text-2:       #A0A5AD;
      --text-3:       #5A6068;
      --lime:         #FFC700;
      --lime-dim:     #FABE00;
      --pattern-color: rgba(255, 199, 0, 0.00); /* Hidden pattern in fampay mode */
      --nav-bg:       rgba(0,0,0,0.85);

      /* FamApp Specific Overrides */
      --btn-radius: 50px;
      --card-radius: 20px;
      --btn-shadow: none;
      --btn-shadow-hover: 0 4px 14px rgba(255, 199, 0, 0.25);
      --btn-shadow-active: none;
      --btn-translate-hover: translateY(-2px);
      --btn-translate-active: scale(0.98);
      --card-bg: linear-gradient(180deg, #282A30 0%, #1A1C20 100%);
      --card-border: 1px solid rgba(255, 255, 255, 0.05);
      --font-weight-headings: 700;
    }"""
        content = re.sub(r'\[data-theme="fampay"\]\s*\{[^}]+\}', fampay_css_new.strip(), content)

    # 3. Refactor Button CSS to use variables
    content = content.replace('box-shadow: 3px 3px 0 var(--lime-dim);', 'box-shadow: var(--btn-shadow); border-radius: var(--btn-radius);')
    content = content.replace('box-shadow: 4px 4px 0 var(--lime-dim); transform: translate(-1px,-1px);', 'box-shadow: var(--btn-shadow-hover); transform: var(--btn-translate-hover);')
    content = content.replace('box-shadow: none; transform: translate(3px,3px);', 'box-shadow: var(--btn-shadow-active); transform: var(--btn-translate-active);')

    content = content.replace('box-shadow: 3px 3px 0 var(--border);', 'box-shadow: var(--btn-shadow); border-radius: var(--btn-radius);')
    content = content.replace('box-shadow: 4px 4px 0 var(--border-s); transform: translate(-1px,-1px);', 'box-shadow: var(--btn-shadow-hover); transform: var(--btn-translate-hover);')
    # active already replaced generically if we are careful, but let's do targeted:

    # 4. Refactor feature cards (if any). If feature cards exist, let's update them.
    if '.feature {' in content:
        content = content.replace(
            '.feature {',
            '.feature {\n      background: var(--card-bg);\n      border: var(--card-border);\n      border-radius: var(--card-radius);'
        )

    # 5. Update typography weight variables
    if 'font-weight: 800;' in content:
        content = content.replace('font-weight: 800;', 'font-weight: var(--font-weight-headings);')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Updated {filepath}')
