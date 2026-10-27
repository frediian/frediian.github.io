# frediian · Portafolio y servicios TI

Sitio estático en español, sin dependencias de compilación. Compatible con GitHub Pages. La portada incluye el video de presentación de `https://frediian.dev/frediian-animated.mp4` y dos fotogramas extraídos de ese video: un póster y un retrato de perfil. Los archivos se sirven localmente desde `assets/`.

**Eslogan:** «Tecnología que resuelve, tú avanzas». Ubicación en Loja, Ecuador; atención directa en Loja, Zamora y Yantzaza, y reuniones agendadas para todo el país. La comparación con la primera versión está en [docs/REDISENO.md](docs/REDISENO.md).

## Desarrollo local

Desde `/workspace/frediian.github.io` (o la raíz de este repositorio):

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

No requiere Ruby, Jekyll, npm ni claves. La página se entrega directamente desde `index.html`; `.nojekyll` evita una compilación de Jekyll en GitHub Pages. Las fuentes Manrope y DM Sans están incluidas localmente, con sus licencias SIL Open Font License en `assets/fonts/`. No hay dependencias externas para renderizar la página.

## Validación

Comprueba la portada y los recursos mediante peticiones HTTP locales. En un navegador revisa el menú móvil, los detalles desplegables de las seis categorías de servicios, las preguntas frecuentes, el retorno al inicio y los botones contextuales de WhatsApp. El botón de consulta técnica solicita coordinar una cita de USD 40 por 2 horas; no realiza cobros ni reserva horarios automáticamente. Las referencias a $800 y $1.400 representan presupuestos del cliente para revisar alcance, no tarifas de productos ni ofertas garantizadas.

El video tiene control de pausa, respeta la preferencia de movimiento reducido y se pausa fuera de pantalla. El número de contacto no aparece en texto ni en un enlace HTML: JavaScript construye el destino al pulsar un botón. Esto reduce la extracción básica, pero no impide que un rastreador con JavaScript o un usuario de WhatsApp obtenga el número. Ocultarlo por completo requeriría un intermediario de contacto y no un enlace directo a WhatsApp.

## Personalización y publicación

- Contenido y condiciones: `index.html`.
- Logos originales y tokens suministrados: `assets/brand/`. La cabecera y el pie usan los logos SVG inline para renderizar Manrope local correctamente.
- Estilos: `assets/styles.css`; paleta y tokens: `assets/brand/tokens.css`.
- Mensajes y contacto: `assets/app.js`. Al cambiar estilos, scripts, tokens o favicon, actualiza su parámetro `v` en `index.html` para que las visitas anteriores reciban la versión nueva.
- Configuración descriptiva de GitHub Pages: `_config.yml`.
- Si se publica en un dominio diferente, actualizar `og:url` y `og:image` con la dirección pública definitiva.

GitHub Pages publica desde la raíz de `main`. El dominio `frediian.dev` ya estaba configurado en el remoto mediante `CNAME` y se conserva. El rediseño no cambia DNS ni la asociación del dominio; la URL pública de metadatos es `https://frediian.dev/`.

## Referencias para los temas de consultoría

Las áreas de seguridad, continuidad y optimización de costos se contrastaron con [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework) y [Microsoft Azure Well-Architected: Cost Optimization](https://learn.microsoft.com/en-us/azure/well-architected/cost-optimization/). Son referencias de buenas prácticas, no certificaciones ni afiliaciones de frediian.
