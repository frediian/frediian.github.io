# Comparación del rediseño

> Registro del rediseño anterior. La actualización vigente según `FREDIIAN_WEB_CODEX.md` está documentada en [IMPLEMENTACION-BRIEF.md](IMPLEMENTACION-BRIEF.md).

La nueva versión conserva los servicios del sitio publicado y adopta la identidad visual y el enfoque comercial de los documentos aportados. Los adjuntos se trataron como referencias; las decisiones del usuario prevalecen sobre sus ejemplos y promesas.

| Aspecto | Versión anterior | Documentos aportados | Nueva versión |
| --- | --- | --- | --- |
| Mensaje | «Tu tecnología, bien resuelta» y explicación extensa. | Beneficios comerciales, con titulares y argumentos largos. | «Tecnología que resuelve, tú avanzas». Introducción breve y un llamado a conversar. |
| Identidad | Marca tipográfica creada para el primer sitio; azules y cian del video. | Logotipos, isotipo, favicon y tokens de marca. | Identidad minimalista v3 del enlace compartido: símbolo geométrico, paleta azul/cian/naranja, iconos propios y video original. |
| Servicios | Seis tarjetas con listas técnicas visibles. | Seis áreas similares, acompañadas de más texto y promesas. | Se conservan las seis áreas; una frase por tarjeta y detalles bajo «Qué incluye». |
| Equipos y accesos | Active Directory, GPO y endpoints dentro del catálogo. | Énfasis en seguridad y respaldos. | Sección específica de control centralizado: Active Directory para usuarios y computadoras, MDM compatible para celulares y tablets. |
| Presupuesto | Propuesta por alcance; solo la consulta técnica tenía una tarifa. | Casos y cifras de ahorro no acreditados. | Proyectos desde USD 300, según la actualización del usuario; el importe final depende del tamaño y alcance del negocio. |
| Atención | Ecuador y asesoría remota de forma general. | Algunos ejemplos sitúan la actividad en Quito y mencionan otros países. | Ubicación: Loja, Ecuador. Atención directa y personalizada en Loja, Zamora y Yantzaza; todo Ecuador por agenda o videorreunión. |
| Confianza | Trato directo y alcance transparente. | Años, resultados, disponibilidad y garantías sin evidencia aportada. | Mensajes verificables, sin testimonios, estadísticas ni garantías inventadas. |

## Texto reducido en el primer rediseño

Registro de la comparación de `<main>` entre `f305ec2` y el primer rediseño `d0c4907`. Estas cifras preceden a la actualización posterior de identidad v3 y del presupuesto a USD 300:

| Medida | Anterior | Nueva | Cambio |
| --- | ---: | ---: | ---: |
| Palabras con los desplegables cerrados | 807 | 537 | 270 menos; reducción del 33,5 % |
| Palabras incluyendo el contenido desplegable | 962 | 788 | 174 menos; reducción del 18,1 % |
| Promedio de palabras por título `h1`–`h3` | 4,11 | 3,16 | Títulos más breves en promedio |

Medición sobre el HTML: solo texto dentro de `<main>`, excluyendo SVG, scripts, estilos, fallback del video y `noscript`. La medida inicial conserva el texto de cada `<summary>` y omite el resto de los `<details>` cerrados. Se contaron palabras Unicode, incluidos importes y números; no se midieron píxeles ni texto alternativo de imágenes. Estas cifras corresponden al primer rediseño documentado, no a la cantidad de texto en una única pantalla ni a modificaciones posteriores.

## Alcance y condiciones

- **Presupuesto actual.** El usuario actualizó el punto de partida a proyectos desde USD 300. La propuesta final varía según tamaño del negocio, usuarios, equipos, funciones, integraciones y soporte; no es una tarifa fija para todos los productos.
- **Consulta técnica.** Se conserva la única tarifa ya indicada expresamente por el usuario: $40 por dos horas, con cita previa. No se añaden descuentos, cupos semanales ni garantías.
- **Software libre y facturación.** Se distingue la ausencia de cuotas por licencia en las soluciones con software libre de los posibles costos de dominio, alojamiento y soporte. La facturación electrónica mantiene suscripción mensual o anual y revisión de requisitos del SRI.
- **Active Directory y MDM.** Active Directory centraliza identidades, permisos y computadoras compatibles. La gestión de celulares y tablets se integra mediante MDM compatible; no se atribuye a Active Directory por sí solo el control completo de cualquier dispositivo.
- **Cifras descartadas.** No se incorporan los «más de ocho años», respuesta menor a dos horas, ahorros de $1.400 o de $600–$1.200, margen de +28,4 %, disponibilidad del 99,9 %, porcentajes del 70 %, tres cupos semanales, descuento del 50 % ni resultados de supuestos clientes presentes en los ejemplos. Tampoco se prometen restauraciones en minutos ni protección absoluta.

La comparación documenta el contenido. El despliegue se verifica por separado en GitHub Actions. Se conserva el CNAME `frediian.dev` añadido al remoto por el usuario; no se modifica DNS.
