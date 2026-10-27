# Implementación de FREDIIAN_WEB_CODEX.md

La web conserva su arquitectura estática y la identidad de `docs/brand-v3/DESIGN.md`: logotipos v3, Manrope/DM Sans y paleta azul, cian y naranja. El brief entregado se conserva en la raíz como referencia.

| Requisito | Implementación |
| --- | --- |
| Mensaje y navegación | Eslogan exacto «Tecnología que resuelve. Tú avanzas.», navegación Inicio / Soluciones / Arquitectura e IA / Sobre mí / Contacto y portada conceptual de sistemas conectados. |
| Especialidades principales | Software y APIs; arquitectura C4 y ADR; IA, agentes y MCP; harness y controles; desarrollo seguro SSDLC; datos, SSRS e infraestructura. |
| Servicios anteriores | Seis áreas operativas en un bloque desplegable: web, e-commerce, POS y facturación; compras; Power BI y SQL; servidores y redes; Active Directory, MDM y endpoints; monitoreo. Se conservan todos los detalles y anclas anteriores. |
| Arquitectura e IA | Tres pilares, ejemplo C4 con Contexto / Contenedores / Componentes, flujo conceptual de harness y glosario. Los ejemplos se identifican como ilustrativos, sin atribuirlos a clientes. |
| Controles de IA | Permisos, contexto y estado, herramientas/MCP, datos autorizados, validación, observabilidad/evaluaciones y aprobación humana antes de acciones sensibles. No hay agentes ni conexiones a proveedores operando en la web. |
| Método y biografía | Cuatro pasos y biografía resumida de la experiencia financiera/pública suministrada. Sin empleadores, certificaciones, resultados ni años calculados. |
| Contacto | WhatsApp existente, recomendaciones gratuitas y consulta técnica de USD 40/2 h. No se añade un formulario sin backend. Cobertura Loja/Zamora/Yantzaza y reuniones para Ecuador. |
| Presupuesto | Se conserva «Proyectos desde USD 300», sujeto a tamaño y alcance. No se asignan nuevos precios a productos. |
| Compartir | Doce PNG de 1080 × 1920, con el eslogan exacto, descarga, QR y vista previa. Los seis QR anteriores continúan abriendo su tarjeta aunque la sección esté cerrada. |
| SEO | Título y descripción del brief, canonical, Open Graph con retrato autorizado, un H1 y JSON-LD `WebSite`/`Person` con datos conocidos. |

## Archivos editables y generación

- `content/services.json`: catálogo único para tarjetas, descripciones técnicas y piezas sociales.
- `scripts/build_services.py`: valida el catálogo y genera los fragmentos y los datos sociales derivados.
- `content/architecture.html`: módulo editorial de arquitectura, IA y glosario.
- `scripts/build_site.py`: compone los fragmentos dentro de `index.html` y actualiza las versiones de recursos.
- `scripts/generate-social.py`: regenera todas las imágenes y compone el sitio. `--skip-html` permite generar solo piezas/datos sin modificar la portada.
- `assets/architecture.js`: mejora progresiva de las pestañas, con flechas, Home y End. Sin JavaScript se muestran las tres vistas en secuencia.
- `assets/app.js`: revela los contenedores desplegables al entrar por enlaces y QR antiguos.

Los archivos `content/generated-*.html`, `social/services.json` y `assets/social/*` son resultados generados; no editarlos como fuente de contenido.

## Validación

Se verifican con navegador la distribución de seis tarjetas principales y seis operativas, el eslogan, los metadatos, las vistas C4, el teclado, el foco, los enlaces QR heredados, la descarga de las doce imágenes y los escenarios de compartir/cancelar/fallo. Las llamadas de compartir y portapapeles se simulan en las pruebas; no se envían mensajes ni publicaciones.

Los PNG se validan por dimensiones, carga de fuentes, zonas seguras y ausencia de solapamientos. Los QR se decodifican para comprobar su destino. Se revisa responsive de móvil a escritorio, incluidos los módulos abiertos y la alternativa sin JavaScript.

El HTML ya compuesto se publica desde `main` mediante GitHub Pages. Los cambios de contenido no modifican DNS ni el CNAME existente.
