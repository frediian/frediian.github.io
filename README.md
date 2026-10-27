# frediian · Portafolio y servicios TI

Sitio estático en español, sin dependencias en producción. Compatible con GitHub Pages. El video de presentación de `https://frediian.dev/frediian-animated.mp4` se conserva en Sobre mí. El video, su póster y el retrato extraído se mantienen localmente en `assets/`; el póster también se utiliza en los metadatos.

**Eslogan:** «Tecnología que resuelve. Tú avanzas.» Ubicación en Loja, Ecuador; atención directa en Loja, Zamora y Yantzaza, y reuniones agendadas para todo el país. La comparación con la primera versión está en [docs/REDISENO.md](docs/REDISENO.md).

## Desarrollo local

Desde `/workspace/frediian.github.io` (o la raíz de este repositorio):

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

No requiere Ruby, Jekyll, npm ni claves. La página se entrega directamente desde `index.html`; `.nojekyll` evita una compilación de Jekyll en GitHub Pages. Las fuentes Manrope y DM Sans están incluidas localmente, con sus licencias SIL Open Font License en `assets/fonts/`. No hay dependencias externas para renderizar la página.

## Validación

Comprueba la portada y los recursos mediante peticiones HTTP locales. En un navegador revisa el menú móvil, las seis soluciones principales, las seis áreas operativas desplegables y los ejemplos conceptuales C4/IA, las preguntas frecuentes, el retorno al inicio y los botones contextuales de WhatsApp. El botón de consulta técnica solicita coordinar una cita de USD 40 por 2 horas; no realiza cobros ni reserva horarios automáticamente. El presupuesto de proyectos parte de USD 300; el valor final depende del tamaño del negocio y el alcance. No se asignan tarifas fijas a productos.

El video tiene control de pausa, respeta la preferencia de movimiento reducido y se pausa fuera de pantalla. El número de contacto no aparece en texto ni en un enlace HTML: JavaScript construye el destino al pulsar un botón. Esto reduce la extracción básica, pero no impide que un rastreador con JavaScript o un usuario de WhatsApp obtenga el número. Ocultarlo por completo requeriría un intermediario de contacto y no un enlace directo a WhatsApp.

## Personalización y publicación

- Brief aplicado: `FREDIIAN_WEB_CODEX.md`; identidad vigente: `docs/brand-v3/DESIGN.md`.
- Catálogo editable único: `content/services.json`. Generar tarjetas con `scripts/build_site.py`; el resto del contenido público y condiciones está en `index.html`.
- Módulo conceptual de arquitectura: `content/architecture.html`, `assets/architecture.css` y `assets/architecture.js`.
- Identidad v3: maestros en `assets/brand/logos/`, iconos en `assets/brand/iconos/` y [manual de diseño](docs/brand-v3/DESIGN.md). [Descargar kit SVG/CSS](assets/brand/frediian-identidad-v3.zip).
- La cabecera y el pie usan los logos SVG inline para renderizar Manrope local correctamente. Se recorta el espacio sobrante del viewBox; el pie compacto omite el eslogan del maestro inverso para mantenerlo legible. Se preservan todos los maestros completos.
- Estilos: `assets/styles.css`; paleta y tokens: `assets/brand/tokens.css`.
- Mensajes y contacto: `assets/app.js`. Al cambiar estilos, scripts, tokens o favicon, actualiza su parámetro `v` en `index.html` para que las visitas anteriores reciban la versión nueva.
- Configuración descriptiva de GitHub Pages: `_config.yml`.
- Si se publica en un dominio diferente, actualizar `og:url` y `og:image` con la dirección pública definitiva.

GitHub Pages publica desde la raíz de `main`. El dominio `frediian.dev` ya estaba configurado en el remoto mediante `CNAME` y se conserva. El rediseño no cambia DNS ni la asociación del dominio; la URL pública de metadatos es `https://frediian.dev/`.

## Referencias para los temas de consultoría

Las áreas de seguridad, continuidad y optimización de costos se contrastaron con [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework) y [Microsoft Azure Well-Architected: Cost Optimization](https://learn.microsoft.com/en-us/azure/well-architected/cost-optimization/). Son referencias de buenas prácticas, no certificaciones ni afiliaciones de frediian.

La identidad v3 se recuperó de los SVG, constantes y plantillas visibles en la [conversación compartida por el usuario](https://chatgpt.com/share/6ae0e1e4-9468-83e9-b16f-fe903a8b1b0c?ogimg=multicolor). El código de esa conversación no se ejecutó. Origen, método y hashes en `docs/brand-v3/RECOVERY.json`. El ZIP reúne 22 archivos vectoriales y de diseño recuperados; no contiene las previsualizaciones PNG del paquete original. La hoja de tokens activa conserva los valores v3 con alias para los componentes existentes; no importa las reglas de layout de la demo. El eslogan se sincronizó con la forma exacta del brief: «Tecnología que resuelve. Tú avanzas.»

## Imágenes para compartir

Cada tarjeta de servicio incluye «Compartir»: abre una vista previa de su PNG vertical 1080 × 1920, con opción de compartir, descargar y copiar el enlace. Los navegadores con soporte para archivos reciben el PNG en su menú nativo; si solo admiten enlaces se identifica esa opción. La descarga está disponible en ambos casos, y sin JavaScript el enlace descarga directamente la imagen.

Las piezas usan necesidad → beneficio → contacto, con la identidad v3, texto breve, zonas seguras para estados y un QR al servicio correspondiente. El QR y el texto muestran la web, no el teléfono. Se mantienen las condiciones reales del software libre y la facturación; no se incorporan las estadísticas, ahorros o escasez de los ejemplos adjuntos.

- Textos editables: `content/services.json`. `social/services.json` y los fragmentos HTML se derivan de este catálogo; no editarlos a mano.
- Plantilla de exportación: `social/template.html`.
- PNG y manifiesto público: `assets/social/`.
- Interacción: `assets/share.js`; pruebas de navegador: `tests/test_share.py`.

El sitio utiliza archivos estáticos; las herramientas de renderizado son solo para mantenimiento. Desde la raíz del repositorio, instala las dependencias en un entorno virtual fuera del checkout:

```sh
python3 -m venv /workspace/.venvs/frediian-social
/workspace/.venvs/frediian-social/bin/pip install -r social/requirements.txt
/workspace/.venvs/frediian-social/bin/python -m playwright install chromium
/workspace/.venvs/frediian-social/bin/python scripts/generate-social.py
```

El generador carga el catálogo único, produce doce PNG, valida dimensiones y zonas seguras, genera el manifiesto y compone los servicios y el módulo de arquitectura en `index.html`. También actualiza las versiones de recursos. Las seis anclas de servicios anteriores se conservan para no romper los QR ya publicados. Acepta `--chromium /ruta/al/navegador` si el navegador ya está instalado. Para cambios de datos o textos de servicios, regenera las imágenes. Para cambios de `content/architecture.html`, ejecuta `python3 scripts/build_site.py`. Para cambios únicamente de CSS o JavaScript, ejecuta `python3 scripts/update_asset_versions.py`.

Si cambia el dominio público, actualiza `ORIGIN` en el generador y regenera las imágenes para actualizar sus QR y enlaces.

Pruebas del menú de compartir, archivos descargados, enlaces, cancelaciones, recuperación de errores y navegación por teclado:

```sh
/workspace/.venvs/frediian-social/bin/python -m unittest discover -s tests -p test_share.py -v
```

Las pruebas simulan las API de compartir y portapapeles; no envían publicaciones ni mensajes a servicios externos. La publicación en una red social se confirma en la aplicación que elija la persona.

## Actualización del brief

El catálogo principal presenta software/API, arquitectura C4, IA/MCP, harness de agentes, desarrollo seguro y datos/infraestructura. Las seis áreas operativas previas permanecen disponibles en un bloque secundario. Los ejemplos de arquitectura e IA son ilustrativos; la web pública no ejecuta agentes ni integra credenciales de proveedores. Contacto reutiliza WhatsApp, sin un formulario con backend ficticio. Ver [decisiones y validación](docs/IMPLEMENTACION-BRIEF.md).
