import os
import glob
import re

css_light_theme = """
    [data-theme="light"] {
      --black:        #F8F9FA;
      --surface:      #FFFFFF;
      --surface-hi:   #F1F3F5;
      --surface-hir:  #E9ECEF;
      --border:       #DEE2E6;
      --border-s:     #CED4DA;
      --text-1:       #212529;
      --text-2:       #495057;
      --text-3:       #6C757D;
      --lime:         #A6F81B;
      --lime-dim:     #8DD613;
      --pattern-color: rgba(0,0,0,0.06);
      --nav-bg:       rgba(248, 249, 250, 0.88);
    }
"""

js_theme_logic = """
  // Theme Toggle Logic
  const themeToggleBtn = document.getElementById('theme-toggle');
  if (themeToggleBtn) {
    themeToggleBtn.addEventListener('click', () => {
      let theme = document.documentElement.getAttribute('data-theme');
      let newTheme = (theme === 'dark' || !theme) ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', newTheme);
      localStorage.setItem('theme', newTheme);
    });
  }
"""

fouc_script = """
  <script>
    const savedTheme = localStorage.getItem('theme') || 'dark';
    document.documentElement.setAttribute('data-theme', savedTheme);
  </script>
"""

for filepath in glob.glob('website/*.html'):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'data-theme="light"' in content:
        continue

    # Insert [data-theme='light'] after :root
    content = re.sub(r'(:root \{[\s\S]*?\n    \})', r'\1\n' + css_light_theme, content)

    # Update background pattern
    content = content.replace('radial-gradient(rgba(197, 245, 66, 0.04) 1px, transparent 1px)', 'radial-gradient(var(--pattern-color, rgba(197, 245, 66, 0.04)) 1px, transparent 1px)')

    # Update nav background
    content = content.replace('background: rgba(0,0,0,0.88);', 'background: var(--nav-bg, rgba(0,0,0,0.88));')

    # Insert toggle button
    btn_html = '<div class="nav-right">\n      <button class="theme-toggle" id="theme-toggle" aria-label="Toggle theme" style="background:transparent; border:none; cursor:pointer; font-size:18px; padding:0 8px; color:var(--text-1); transition: transform 0.2s;">🌓</button>'
    content = content.replace('<div class="nav-right">', btn_html)

    # Insert JS logic before </body>
    content = content.replace('</body>', js_theme_logic + '\n</body>')

    # Insert FOUC script after <head>
    content = content.replace('<head>', '<head>\n' + fouc_script)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Updated {filepath}')
