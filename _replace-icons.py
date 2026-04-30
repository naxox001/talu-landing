#!/usr/bin/env python3
"""Reemplaza iconos SVG custom por Lucide icons (i data-lucide="..." class="icon-big-pro")."""
import os, re, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = r'C:\Users\sd_ig\OneDrive\Documents\CLAUDE FILES\landing'

# ============ Mapeo h3-text → lucide-icon ============
# Si el h3 que sigue al icono contiene alguna de estas frases (case-insensitive), usar el icono Lucide indicado
HEADING_TO_ICON = [
    # cocina
    (r'punto de humo|250|230', 'flame'),
    (r'biocompatib|reconoce|metaboliza', 'heart-pulse'),
    (r'grass.?fed|chileno|pasto|trazabilidad', 'leaf'),
    (r'sabor|paladar|aroma', 'utensils'),
    (r'sellar|sellado|carnes', 'chef-hat'),
    (r'sart[eé]n', 'cooking-pot'),
    (r'tabla|condimento|cortar', 'square-stack'),
    (r'reposter|empanada|masa', 'cake-slice'),
    (r'verduras|wok', 'leaf'),
    (r'salsa|fina|finas', 'droplet'),
    (r'lípidos|liviano|delicado|fino', 'feather'),
    (r'cubre toda|completa|toda la cocina', 'check-check'),
    (r'ahorra|descuento|17%|23%|25%|30%', 'badge-percent'),
    (r'1 mes|30 d[ií]as|d[ií]as de cocina|rinde|stock', 'calendar-days'),
    (r'garant[ií]a|60 d[ií]as|prueba', 'shield-check'),
    (r'lunes|semana', 'calendar'),
    (r's[aá]bado', 'cake-slice'),
    (r'domingo|familiar|mesa', 'utensils-crossed'),
    # día de la madre
    (r'edici[oó]n limitada|limitada', 'clock'),
    (r'solo mayo|mayo', 'calendar-days'),
    (r'empaque|regalo|caja regalo', 'gift'),
    (r'env[ií]o gratis|env[ií]o', 'truck'),
    (r'hecho a la medida|mam[áa]', 'heart'),
    (r'stock limitado', 'alert-circle'),
    # skincare warm
    (r'rutina ancestral|rutina completa', 'sparkles'),
    (r'sebo de ternero|biocompatible|piel', 'sun'),
    # ternero page
    (r'lípidos m[aá]s cortos|cadenas grasas', 'atom'),
    (r'grass.?fed real', 'leaf'),
    (r'crema biocompatible', 'droplet'),
    (r'punto humo|cocina', 'flame'),
    (r'sello t[äa]lu|sello', 'award'),
    # gift card
    (r'eliges el monto|monto', 'wallet'),
    (r'email destinatario', 'mail'),
    (r'instante|llega', 'send'),
    # pack-familia / unidos
    (r'regalo perfecto', 'gift'),
    (r'una sola filosof', 'sparkles'),
    (r'stock para 60', 'package'),
]

def find_icon_for_heading(heading_text):
    """Devuelve el lucide icon name según el texto del heading."""
    text_lower = heading_text.lower()
    for pattern, icon in HEADING_TO_ICON:
        if re.search(pattern, text_lower, re.IGNORECASE):
            return icon
    return 'star'  # fallback


def replace_in_file(path, container_class, h3_class, icon_class):
    """Reemplaza .container_class > <svg>...</svg> por <i data-lucide="X"> usando el h3 siguiente como pista."""
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content

    # Patrón: <div class="container_class">[contenido SVG]</div>...<h3>TEXTO</h3>
    # Usamos non-greedy para capturar UN bloque a la vez
    pattern = re.compile(
        r'<div class="' + container_class + r'">\s*<svg[^>]*>.*?</svg>\s*</div>\s*'
        r'(.*?)<h3>([^<]+)</h3>',
        re.DOTALL
    )

    def repl(m):
        between = m.group(1)
        heading = m.group(2).strip()
        icon = find_icon_for_heading(heading)
        return (
            f'<div class="{container_class} {icon_class}">'
            f'<i data-lucide="{icon}"></i></div>{between}<h3>{heading}</h3>'
        )

    content = pattern.sub(repl, content)

    if content != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return content.count(icon_class) - original.count(icon_class)
    return 0


# Procesar archivos por tipo de container
TARGETS = [
    # (container class, h3 class hint, css class to add for styling)
    ('por-que-icon', 'h3', 'icon-box-pro'),
    ('big-icon-svg', 'h3', 'icon-big-pro'),
    ('razon-icon', 'h3', 'icon-big-pro'),
    ('pq-icon', 'h3', 'icon-box-pro'),
]

total_changes = 0

for dirpath, _, filenames in os.walk(ROOT):
    if '.git' in dirpath or '_mockups' in dirpath:
        continue
    for fname in filenames:
        if not fname.endswith('.html'):
            continue
        path = os.path.join(dirpath, fname)

        for container, h3, css in TARGETS:
            n = replace_in_file(path, container, h3, css)
            if n:
                rel = os.path.relpath(path, ROOT)
                print(f'  {rel:<50} {container:<15} → {n} icons')
                total_changes += n

print(f'\n{"="*55}')
print(f'TOTAL: {total_changes} iconos reemplazados por Lucide')
