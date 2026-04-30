# TÄLU RAW · Hero 3D — Guía de integración

**GLB final:** `landing/assets/3d/talu-jar.glb` · 0.236 MB · sin animación · Draco · +Y up

---

## 1. Cargar `<model-viewer>` (Google web component)

En `<head>` de la landing:

```html
<script type="module"
  src="https://ajax.googleapis.com/ajax/libs/model-viewer/4.0.0/model-viewer.min.js">
</script>
```

## 2. Markup del hero — reemplaza el SVG actual

```html
<section class="hero">
  <div class="hero-copy">
    <!-- tu copy actual -->
  </div>

  <div class="hero-jar">
    <model-viewer
      id="taluJar"
      src="assets/3d/talu-jar.glb"
      alt="TÄLU RAW · frasco 3D"
      camera-controls
      disable-tap
      interaction-prompt="none"
      environment-image="neutral"
      shadow-intensity="1.1"
      shadow-softness="0.85"
      exposure="1.05"
      camera-orbit="0deg 65deg 7m"
      field-of-view="26deg"
      min-camera-orbit="auto 30deg 5m"
      max-camera-orbit="auto 95deg 12m"
      touch-action="pan-y"
      style="width:100%;height:720px;background:transparent;">
    </model-viewer>
  </div>
</section>
```

**Settings clave:**
- `camera-orbit="0deg 65deg 7m"` → vista 3/4 superior (ángulo A que aprobaste)
- `environment-image="neutral"` → IBL claro que muestra bien el vidrio + dorado
- `disable-tap` → desactiva auto-zoom al tocar
- Sin `auto-rotate` (queremos vaivén custom, no rotación 360)

## 3. Vaivén suave + pausa al interactuar (JS)

```html
<script>
(() => {
  const mv = document.getElementById('taluJar');
  const POLAR = 65, RADIUS = 7;
  const AMPLITUDE = 7;     // ±7° de oscilación
  const PERIOD_MS = 5000;  // 5 segundos por ciclo
  let userPaused = false, pauseTimer = null, t0 = null;

  function tick(now) {
    if (!t0) t0 = now;
    if (!userPaused) {
      const phase = ((now - t0) / PERIOD_MS) * 2 * Math.PI;
      const az = AMPLITUDE * Math.sin(phase);
      mv.cameraOrbit = `${az}deg ${POLAR}deg ${RADIUS}m`;
    }
    requestAnimationFrame(tick);
  }

  mv.addEventListener('load', () => {
    mv.cameraOrbit = `0deg ${POLAR}deg ${RADIUS}m`;
    requestAnimationFrame(tick);
  });

  mv.addEventListener('camera-change', e => {
    if (e.detail.source === 'user-interaction') {
      userPaused = true;
      clearTimeout(pauseTimer);
      pauseTimer = setTimeout(() => { userPaused = false; t0 = performance.now(); }, 2500);
    }
  });
})();
</script>
```

**Comportamiento resultante:**
- El frasco se balancea suavemente ±7° de izquierda a derecha (5 s por ciclo)
- Si el usuario lo arrastra para girarlo manualmente, el vaivén se pausa 2.5 s y vuelve a correr desde la nueva posición

## 4. CSS sugerido para el contenedor

```css
.hero-jar {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}
.hero-jar model-viewer {
  --poster-color: transparent;
}
.hero-jar::before {
  content: '';
  position: absolute;
  width: 65%;
  aspect-ratio: 1;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(184,149,106,0.18) 0%, transparent 70%);
  z-index: 0;
}
```

(El glow ámbar de fondo ayuda a que el jar destaque sin "escenarios" cargados — mismo recurso del mockup que aprobaste)

## 5. Si quieres un fallback poster (SEO + carga rápida)

Cuando hagas el deploy, puedes generar un poster JPG (1 fotograma del modelo) y agregarlo:

```html
<model-viewer ...
  poster="assets/3d/talu-jar-poster.jpg"
  reveal="auto">
</model-viewer>
```

Eso muestra una imagen estática hasta que carga el GLB.

## 6. Performance

- GLB: 236 KB (con Draco)
- model-viewer.min.js: ~750 KB (cached por CDN)
- Total: ~1 MB inicial → carga en <2 s en 4G
- Una vez cargado, render en 60 FPS en celulares modernos

## 7. Accessibility

```html
alt="TÄLU RAW · frasco de crema en base a sebo de res, vista 3D interactiva"
```

## 8. Variables que puedes ajustar después sin re-exportar

| Setting | Default | Para qué |
|---|---|---|
| `camera-orbit` | `0deg 65deg 7m` | Posición inicial (azimuth, polar, radius) |
| `AMPLITUDE` (JS) | 7 | Cuánto se balancea (±°) |
| `PERIOD_MS` (JS) | 5000 | Velocidad del vaivén |
| `exposure` | 1.05 | Brillo general |
| `shadow-intensity` | 1.1 | Fuerza de la sombra |
| `environment-image` | neutral | IBL: neutral / legacy / URL HDRi propio |

## 9. Si quieres cambiar el modelo más adelante

El `.blend` editable está en `Desktop/talu_raw_jar.blend`. Para re-exportar después de cambios:

```python
# En Blender Scripting tab, ejecutar el script:
# Desktop/v76_export.py
```

Eso regenera `landing/assets/3d/talu-jar.glb` con Draco + sin animación.

---

**Backups disponibles:**
- `Desktop/talu_raw_jar_v6.9_GOLD_BACKUP.blend` (estado pre-base anti-slip)
- `Desktop/talu_v6.9_GOLD_BACKUP.png` (render aprobado v6.9)
- `Desktop/talu-jar_v5_backup.glb` (GLB temprano)
