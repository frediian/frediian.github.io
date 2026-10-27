# frediian · Portafolio y servicios TI

Sitio estático en español, sin dependencias de compilación. Compatible con GitHub Pages. La portada incluye el video de presentación de `https://frediian.dev/frediian-animated.mp4` y dos fotogramas extraídos de ese video: un póster y un retrato de perfil. Los archivos se sirven localmente desde `assets/`.

## Desarrollo local

Desde `/workspace/frediian.github.io` (o la raíz de este repositorio):

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

No requiere Ruby, Jekyll, npm ni claves. La página se entrega directamente desde `index.html`; `.nojekyll` evita una compilación de Jekyll en GitHub Pages. Las fuentes Manrope y DM Sans están incluidas localmente, con sus licencias SIL Open Font License en `assets/fonts/`. No hay dependencias externas para renderizar la página.

## Validación

Comprueba la portada y los recursos mediante peticiones HTTP locales. En un navegador revisa el menú móvil, las seis categorías de servicios, las preguntas desplegables, el retorno al inicio y los botones de WhatsApp. El botón de consulta técnica solicita coordinar una cita de USD 40 por 2 horas; no realiza cobros ni reserva horarios automáticamente.

El video tiene control de pausa, respeta la preferencia de movimiento reducido y se pausa fuera de pantalla. El número de contacto no aparece en texto ni en un enlace HTML: JavaScript construye el destino al pulsar un botón. Esto reduce la extracción básica, pero no impide que un rastreador con JavaScript o un usuario de WhatsApp obtenga el número. Ocultarlo por completo requeriría un intermediario de contacto y no un enlace directo a WhatsApp.

## Personalización y publicación

- Contenido y precios: `index.html`.
- Estilos y paleta azul/cian: `assets/styles.css`.
- Mensajes y contacto: `assets/app.js`.
- Configuración descriptiva de GitHub Pages: `_config.yml`.
- Si se publica en un dominio diferente, actualizar `og:image` con la dirección pública definitiva.

Publicar desde la raíz de la rama seleccionada en la configuración de GitHub Pages. No se ha cambiado la configuración DNS ni publicado automáticamente en `frediian.dev`.

## Referencias para los temas de consultoría

Las áreas de seguridad, continuidad y optimización de costos se contrastaron con [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework) y [Microsoft Azure Well-Architected: Cost Optimization](https://learn.microsoft.com/en-us/azure/well-architected/cost-optimization/). Son referencias de buenas prácticas, no certificaciones ni afiliaciones de frediian.
