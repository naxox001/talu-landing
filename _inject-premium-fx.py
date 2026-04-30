#!/usr/bin/env python3
"""Inyecta premium-fx.css + premium-fx.js + Lucide en TODAS las PDPs."""
import os, re, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = r'C:\Users\sd_ig\OneDrive\Documents\CLAUDE FILES\landing'

# Marcadores únicos para evitar duplicados
CSS_MARKER = 'premium-fx.css'
JS_MARKER = 'premium-fx.js'

# Tag a inyectar antes del </head>
def inject_head(content, css_path):
    if CSS_MARKER in content:
        return content, False
    tag = f'<link rel="stylesheet" href="{css_path}">\n</head>'
    return content.replace('</head>', tag, 1), True

# Tag a inyectar antes del </body>
def inject_body(content, js_path):
    if JS_MARKER in content:
        return content, False
    tag = f'<script src="{js_path}" defer></script>\n</body>'
    return content.replace('</body>', tag, 1), True


total_files = 0
total_changes = 0

for dirpath, _, filenames in os.walk(ROOT):
    if '.git' in dirpath or '_mockups' in dirpath:
        continue
    for fname in filenames:
        if not fname.endswith('.html'):
            continue
        path = os.path.join(dirpath, fname)

        # Calcular ruta relativa al CSS/JS
        rel_dir = os.path.relpath(dirpath, ROOT)
        depth = 0 if rel_dir == '.' else len(rel_dir.split(os.sep))
        prefix = '../' * depth
        css_path = f'{prefix}styles/premium-fx.css'
        js_path = f'{prefix}scripts/premium-fx.js'

        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        original = content
        changes = []

        new_content, changed_css = inject_head(content, css_path)
        if changed_css:
            changes.append('CSS')
            content = new_content

        new_content, changed_js = inject_body(content, js_path)
        if changed_js:
            changes.append('JS')
            content = new_content

        if content != original:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            total_files += 1
            total_changes += len(changes)
            rel = os.path.relpath(path, ROOT)
            print(f'  {rel:<48} ← inyectado: {", ".join(changes)}')

print(f'\n{"="*55}')
print(f'TOTAL: {total_files} archivos · {total_changes} inyecciones')
