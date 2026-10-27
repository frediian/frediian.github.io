---
name: "Frediian | Tecnología que resuelve. Tú avanzas."
version: "3.0"
locale: "es-EC"
brand: "frediian."
slogan: "Tecnología que resuelve. Tú avanzas."
source: "Revisión del logotipo y del documento consultor_a_hunaba_DESIGN.md proporcionados por el usuario"
colors:
  brand-trust: "#102F46"
  brand-action: "#17699A"
  brand-cyan: "#51CDE5"
  brand-warmth: "#F6AA71"
  canvas-base: "#FAFBFC"
  canvas-soft: "#EAF3F8"
  canvas-card: "#FFFFFF"
  border-subtle: "#D4E2EA"
  text-primary: "#102F46"
  text-secondary: "#536978"
  status-success: "#247967"
  status-error: "#B23C43"
typography:
  display: { fontFamily: Manrope, fontSize: "clamp(2.5rem, 5vw, 4.5rem)", fontWeight: 800, lineHeight: 1.12, letterSpacing: "-0.03em" }
  headline-lg: { fontFamily: Manrope, fontSize: "2.25rem", fontWeight: 750, lineHeight: 1.2 }
  headline-md: { fontFamily: Manrope, fontSize: "1.375rem", fontWeight: 700, lineHeight: 1.3 }
  body-lead: { fontFamily: "DM Sans", fontSize: "1.125rem", fontWeight: 400, lineHeight: 1.6 }
  body-md: { fontFamily: "DM Sans", fontSize: "1rem", fontWeight: 400, lineHeight: 1.65 }
  body-sm: { fontFamily: "DM Sans", fontSize: "0.875rem", fontWeight: 400, lineHeight: 1.55 }
rounded:
  button: "10px"
  card: "18px"
  media: "20px"
  pill: "9999px"
spacing:
  unit: "4px"
  containerMax: "1200px"
  desktopGutter: "48px"
  mobileGutter: "20px"
  sectionDesktop: "88px"
  sectionMobile: "60px"
---

# DESIGN.md — Frediian / Identidad visual v3

## 1. Propósito y posición de marca

**Nombre comercial:** `frediian.` en minúsculas con punto final cian.

**Eslogan oficial e invariable:** **Tecnología que resuelve. Tú avanzas.**

**Actividad:** desarrollo de software y web, consultoría TI, infraestructura, datos, e-commerce, seguridad y soporte orientado al negocio. Audiencia: negocios y profesionales de Ecuador y Latinoamérica, PYMES, emprendedores y responsables de TI.

**Promesa:** traducir problemas técnicos en soluciones claras, útiles y viables. El tono es experto pero accesible, sin exageraciones ni jerga que aleje al cliente.

**Tono de voz:** humano, preciso, transparente, sencillo, positivo y responsable. Explicar el beneficio antes de enumerar herramientas, hablar de *tu negocio* sin paternalismo y comunicar alcances, plazos y costos con claridad.

## 2. Decisión de rediseño del logotipo

El logotipo aportado utilizaba una letra F predominante y varios recursos —circuitos, nodos, corchetes de código y un contenedor similar a un icono de app—. Aunque reconocible, ese conjunto era más complejo de lo necesario y se acercaba visualmente a algunos iconos sociales.

### Concepto: «Ruta de solución»

- **Símbolo:** marca geométrica construida con un eje estable y dos módulos horizontales de progreso. No usa la tipografía de una «f» minúscula clásica; su geometría propia evoca discretamente la F de Frediian y un camino hacia delante.
- **Azul oscuro:** seguridad, conocimiento y estabilidad.
- **Módulo azul/cian:** acción, claridad y avance.
- **Nodo naranja aislado:** resultado y conexión humana. Es opcional en versiones muy pequeñas.
- **Estética principal plana (flat):** sin líneas de circuito, hexágonos, reflejos 3D, biseles, resplandores, brackets `< >` ni degradados como base.

**Importante:** este diseño es una propuesta gráfica original de trabajo, pero **no equivale a una búsqueda de anterioridades ni garantiza exclusividad jurídica**. Antes de registrarlo o lanzarlo comercialmente, conviene efectuar una revisión de marcas y similitud visual.

### Archivos maestros

| Archivo | Uso |
|---|---|
| `logos/logo-con-eslogan.svg` | Presentaciones, propuestas y hero desktop, siempre que el texto sea legible |
| `logos/logo-horizontal.svg` | Cabecera web, documentos, firmas y espacios medianos |
| `logos/logo-inverso.svg` | Fondos azul oscuro |
| `logos/isotipo-color.svg` | Avatar, marca de agua, tarjetas sociales |
| `logos/isotipo-inverso.svg` | Isotipo sobre fondo oscuro |
| `logos/isotipo-monocromo.svg` | Un solo color, grabado e impresión de economía |
| `logos/favicon.svg` | Favicon para navegador, apps |
| `logos/favicon-simplificado.svg` | Favicon mínimo, con detalle reducido |

### Reglas y medidas

- Zona de protección: al menos `1/4` de la altura del isotipo libre en torno a la marca.
- Logotipo horizontal **sin eslogan** bajo un ancho de 320 px; con eslogan a partir de 460 px, idealmente más.
- Isotipo: 40 px o mayor para cabecera pequeña. Usar favicon simplificado a 16–24 px.
- No estirar, inclinar, recolorear arbitrariamente ni sustituir el nombre por una sola `f` tipográfica.
- No colocar letras o pictogramas de redes sociales dentro del isotipo.
- En redes sociales usar **solo isotipo** para avatar; el eslogan en la portada o descripción.
- Mantener suficiente contraste para uso sobre fotografía; preferir placa lisa semitransparente si el fondo es complejo.

## 3. Paleta cromática principal

| Token | Hex | Función |
|---|---|---|
| Azul profundo | `#102F46` | Identidad, títulos, fondos hero, secciones premium |
| Azul acción | `#17699A` | Botones principales, enlaces, iconos e indicadores |
| Cian dinámico | `#51CDE5` | Acento, avance y énfasis sobre fondos oscuros |
| Naranja humano | `#F6AA71` | Un pequeño punto de conexión / resultados, detalles esporádicos |
| Blanco suave | `#FAFBFC` | Fondo principal |
| Azul niebla | `#EAF3F8` | Secciones alternas, tarjetas muy suaves |
| Blanco puro | `#FFFFFF` | Superficie de tarjetas y texto inverso |
| Borde suave | `#D4E2EA` | Límites funcionales |
| Texto secundario | `#536978` | Metadatos y párrafos accesorios |

**Distribución orientativa:** 72 % fondos neutros, 19 % azul profundo, 7 % azul de acción/cian y 2 % naranja. Son proporciones guía, no una medición rígida.

### Accesibilidad

- El azul principal `#102F46` sobre blanco tiene contraste aproximado **13.8:1**.
- El azul de acción `#17699A` sobre blanco tiene contraste aproximado **6.0:1**, apto para texto normal y botones.
- El cian `#51CDE5` sobre azul oscuro tiene contraste aproximado **7.4:1**; utilizarlo principalmente en secciones oscuras.
- El naranja `#F6AA71` sobre azul oscuro tiene contraste aproximado **7.2:1**; reservarlo para acentos.
- **No utilizar texto pequeño en cian o naranja sobre blanco**, porque no alcanza WCAG AA para texto normal.
- Texto de apoyo `#536978` sobre blanco ofrece contraste aproximado **5.7:1**.

## 4. Tipografía

**Manrope** (700–800): logotipo editable, títulos, cifras e indicadores. **DM Sans** (400–600): párrafos, botones y formularios. No usar tipografías futuristas de ciencia ficción ni texto monoespaciado como familia principal.

- H1: `clamp(40px, 5vw, 72px)`, peso 800, línea 1.12.
- H2: 30–42 px, peso 750, línea 1.2.
- H3: 21–24 px, peso 700, línea 1.3.
- Texto base: 16 px, línea 1.65.
- Texto secundario: mínimo 14 px para contenido funcional.
- Botones: 15–16 px, peso 600 o 700.
- Etiquetas organizativas no cruciales pueden tener 12 px; evitar texto funcional más pequeño.
- Acentos de color en títulos: enfatizar una frase, no cada palabra.

## 5. Iconografía del sistema

Estilo **línea simple redondeada (monoline)**: caja de 24×24, trazo 1.8 px, terminaciones `round`, sin relleno ni sombras. Color estándar `#17699A`. Sobre secciones oscuras utilizar blanco/cian.

| Icono | Archivo | Contexto |
|---|---|---|
| Desarrollo | `iconos/desarrollo.svg` | Web, software, integraciones |
| Consultoría | `iconos/consultoria.svg` | Acompañamiento y decisiones |
| Datos | `iconos/datos.svg` | Power BI, BI, reportes |
| Infraestructura | `iconos/infraestructura.svg` | Servidores, nube, redes |
| Seguridad | `iconos/seguridad.svg` | Gestión de riesgos, protección |
| Automatización | `iconos/automatizacion.svg` | Flujos e integraciones |
| Monitoreo | `iconos/monitoreo.svg` | Control operativo y métricas |
| Comercio electrónico | `iconos/ecommerce.svg` | Tiendas y POS |
| Avance | `iconos/direccion.svg` | Navegación y llamados a la acción |
| Contacto | `iconos/contacto.svg` | Conversación directa |

No mezclar iconografía filled, emoji 3D y monoline en la misma vista. No usar los íconos de servicios como marcas registrables; son elementos de interfaz.

## 6. Sistema de composición y componentes

- **Contenedor máximo:** 1200 px. Escritorio: 12 columnas y 24 px entre columnas; móvil: una columna para tarjetas.
- **Espaciado:** múltiplos de 4 px. Sección desktop: 88–104 px. Móvil: 56–72 px. Márgenes móviles: 20 px.
- **Tarjetas:** fondo blanco, borde `#D4E2EA`, radio 18 px, 24–32 px de padding, sombra apenas perceptible.
- **Botones:** radio 10 px, alto mínimo 44 px (preferido 48–52), `background #17699A` con texto blanco. Hover `#102F46`.
- **Formulario:** altura mínima 48 px, labels explícitos, errores visibles y claros; anillo de foco de 3 px.
- **Etiquetas:** radio total, fondo `#EAF3F8`, texto `#17699A`; no más de tres por tarjeta.
- **Iconos en tarjeta:** 24–28 px con espacio alrededor. Evitar seis elementos decorativos para un mismo concepto.
- **Animación:** transiciones sutiles de 150–200 ms y respeto por `prefers-reduced-motion`.

### Hero recomendado para frediian.dev

**Eyebrow:** DESARROLLO · CONSULTORÍA · SERVICIOS TI

**Titular:** Tecnología que resuelve. **Tú avanzas.**

**Bajada:** Desarrollo de software, datos e infraestructura para que tu negocio funcione mejor, sin complicaciones innecesarias.

**CTA principal:** Hablemos de tu proyecto

**CTA secundario:** Ver soluciones

Usar la foto o retrato propio que ya tenga el sitio, evitando ilustraciones de ingenieros genéricos. El logo completo va en la sección hero solo si no compite con el titular.

### Tarjetas de servicio

1. Beneficio del cliente en título.
2. Descripción de 1–2 frases sin jerga.
3. 2–4 funcionalidades verificables.
4. Un CTA contextual: «Consultar», «Conocer más», «Solicitar propuesta».

## 7. Aplicaciones y formatos

| Soporte | Variante | Recomendación |
|---|---|---|
| Web en escritorio | Horizontal con o sin eslogan | SVG, preferible sin eslogan en header |
| Web móvil | Horizontal corto o isotipo | Mantener nav limpia |
| Favicon navegador | Simplificado | 16, 32, 48 px |
| Avatar social | Isotipo | 1:1, con margen interior de 16–20 % |
| Portada LinkedIn / presentación | Logo + eslogan | Suficiente aire y jerarquía |
| Publicación social | Logo sin eslogan + gran promesa | Composición 1:1, 4:5 o 9:16 según canal |
| Propuesta comercial | Logo con eslogan en portada | Luego logo compacto en pie de página |
| Tarjeta de contacto | Horizontal sin eslogan | Eslogan solo si es legible |

## 8. Microcopy en español para Ecuador y Latinoamérica

- «Tu negocio necesita soluciones, no más complicaciones».
- «Conectemos tus ideas con resultados».
- «Desarrollo y consultoría con trato directo».
- «Hablemos de lo que necesitas resolver».

Evitar promesas absolutas de seguridad, disponibilidad, «100 % sin riesgos», precios no comprobados o independencia total de proveedores. No usar frases como «sin licencias» para servicios que dependan de condiciones específicas sin explicarlas.

## 9. Checklist de implementación

- [ ] Integrar `frediian-tokens.css` en la web.
- [ ] Cambiar `favicon.svg` por el favicon v3, conservando copia del original.
- [ ] Sustituir el logo de cabecera por `logo-horizontal.svg` sin eslogan.
- [ ] Revisar portada, encabezado y CTA para incorporar el eslogan completo.
- [ ] Usar el isotipo solo en avatar, app y piezas sociales.
- [ ] Sustituir iconos inconsistentes por el set incluido.
- [ ] Validar legibilidad real a 16, 32, 48 y 320 px.
- [ ] Comprobar contraste WCAG AA, navegación por teclado y vista móvil.
- [ ] Verificar posibles conflictos marcarios antes de registro o uso comercial a gran escala.

**Nota técnica:** Los SVG incluyen texto editable con `font-family: Manrope` y `DM Sans`; se deben instalar/cargar esas familias en el proyecto donde se utilicen. Para imprenta, convertir tipografía a contornos en el software de diseño si el proveedor no dispone de las fuentes. No se incluyen archivos de fuentes.
