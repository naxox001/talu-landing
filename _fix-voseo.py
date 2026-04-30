#!/usr/bin/env python3
"""Reemplaza voseo argentino por tuteo chileno/neutral en todos los HTMLs."""
import os, re, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Mapeo voseo argentino → tuteo chileno
REPLACEMENTS = [
    # Verbos en presente vos → tú
    (r'\btenés\b', 'tienes'),
    (r'\bTenés\b', 'Tienes'),
    (r'\babrís\b', 'abres'),
    (r'\bAbrís\b', 'Abres'),
    (r'\bprobás\b', 'pruebas'),
    (r'\bProbás\b', 'Pruebas'),
    (r'\bpodés\b', 'puedes'),
    (r'\bPodés\b', 'Puedes'),
    (r'\bquerés\b', 'quieres'),
    (r'\bQuerés\b', 'Quieres'),
    (r'\bsabés\b', 'sabes'),
    (r'\bSabés\b', 'Sabes'),
    (r'\bhacés\b', 'haces'),
    (r'\bHacés\b', 'Haces'),
    (r'\bvenís\b', 'vienes'),
    (r'\bVenís\b', 'Vienes'),
    (r'\bsalís\b', 'sales'),
    (r'\bSalís\b', 'Sales'),
    (r'\bponés\b', 'pones'),
    (r'\bPonés\b', 'Pones'),
    (r'\belegís\b', 'eliges'),
    (r'\bElegís\b', 'Eliges'),
    (r'\bagregás\b', 'agregas'),
    (r'\bAgregás\b', 'Agregas'),
    (r'\bcomés\b', 'comes'),
    (r'\bComés\b', 'Comes'),
    (r'\bnotás\b', 'notas'),
    (r'\bNotás\b', 'Notas'),
    (r'\bconocés\b', 'conoces'),
    (r'\bConocés\b', 'Conoces'),
    (r'\breemplazás\b', 'reemplazas'),
    (r'\bReemplazás\b', 'Reemplazas'),
    (r'\bescogés\b', 'escoges'),
    (r'\bEscogés\b', 'Escoges'),
    (r'\btirás\b', 'tiras'),
    (r'\bTirás\b', 'Tiras'),
    (r'\bchequeás\b', 'chequeas'),
    (r'\bChequeás\b', 'Chequeas'),
    (r'\bquedás\b', 'quedas'),
    (r'\bQuedás\b', 'Quedas'),
    (r'\bpedís\b', 'pides'),
    (r'\bPedís\b', 'Pides'),
    (r'\bdecís\b', 'dices'),
    (r'\bDecís\b', 'Dices'),
    (r'\bcocinás\b', 'cocinas'),
    (r'\bCocinás\b', 'Cocinas'),
    # Imperativos vos → tú
    (r'\bescribinos\b', 'escríbenos'),
    (r'\bEscribinos\b', 'Escríbenos'),
    (r'\bescribime\b', 'escríbeme'),
    (r'\bEscribime\b', 'Escríbeme'),
    (r'\bcontame\b', 'cuéntame'),
    (r'\bContame\b', 'Cuéntame'),
    (r'\bregalale\b', 'regálale'),
    (r'\bRegalale\b', 'Regálale'),
    # Pronombre "vos" como palabra suelta → "tú"
    (r'\bvos\b', 'tú'),
    (r'\bVos\b', 'Tú'),
]

def fix_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content
    changes = []
    for pattern, replacement in REPLACEMENTS:
        new_content, n = re.subn(pattern, replacement, content)
        if n > 0:
            changes.append((pattern, replacement, n))
        content = new_content
    if content != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return changes
    return None

ROOT = r'C:\Users\sd_ig\OneDrive\Documents\CLAUDE FILES\landing'
total_files = 0
total_changes = 0

for dirpath, _, filenames in os.walk(ROOT):
    if '.git' in dirpath or '_mockups' in dirpath:
        continue
    for fname in filenames:
        if not fname.endswith(('.html', '.md')):
            continue
        path = os.path.join(dirpath, fname)
        result = fix_file(path)
        if result:
            total_files += 1
            file_changes = sum(n for _, _, n in result)
            total_changes += file_changes
            rel = os.path.relpath(path, ROOT)
            print(f'\n{rel}  ({file_changes} cambios):')
            for pattern, replacement, n in result:
                clean_pat = pattern.replace(r'\b', '').replace(r'\\', '')
                print(f'  {clean_pat:>16} → {replacement:<16} ({n})')

print(f'\n{"="*50}')
print(f'TOTAL: {total_files} archivos · {total_changes} reemplazos')
