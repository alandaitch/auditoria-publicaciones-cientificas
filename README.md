# Auditoría independiente de artículos científicos

¿Puede la inteligencia artificial encontrar errores comprobables en artículos que ya pasaron revisión científica?
Alan Daitch impulsa este experimento. Contrastamos afirmaciones concretas con tablas, cálculos o código del estudio.
Enviamos la observación a sus autores. Si aparece evidencia que cambia nuestra interpretación, rectificamos la ficha.

[Explorá el experimento](https://alandaitch.github.io/auditoria-publicaciones-cientificas/) · [Preguntas frecuentes](https://alandaitch.github.io/auditoria-publicaciones-cientificas/#preguntas)

El sitio muestra **190 observaciones públicas**.
Otras **129** esperan que pasen diez días completos desde el envío verificado.
Ese plazo corresponde a publicar nuestra ficha. La revista tiene su propio proceso de corrección.
Las consultas pendientes de envío suman **0**.
Las consultas cuyo envío falta confirmar suman **1**.
El sitio muestra ambos grupos como totales.

Cada ficha explica la afirmación, nuestra observación y qué cambiaría si se comprueba.
Las citas cuentan publicaciones que referencian el artículo. Cada recuento indica su fuente y fecha.
La prioridad indica qué observaciones revisamos primero.

## Consultar

- [Explorador de fichas públicas](https://alandaitch.github.io/auditoria-publicaciones-cientificas/#explorar).
- [Datos detallados en JSON](hallazgos.json).
- [Tabla resumida en CSV](hallazgos.csv).
- [Tres comprobaciones reproducibles de código](reproducciones/README.md).

Cada estado describe el seguimiento **sin reproducir correspondencia privada**.
“Reconocida” refleja una respuesta específica, no una aceptación editorial del artículo completo.
“Corrección anunciada” no equivale a una corrección publicada.
“Parche público verificado” indica un cambio de código, no una fe de erratas editorial.
“Sin evaluación científica registrada” indica ausencia de respuesta sustantiva en nuestros registros.
Las respuestas automáticas, entregas fallidas y contactos cerrados se distinguen expresamente.

Al corte del **2026-11-26**, los estados son:

- Consulta enviada; sin evaluación científica registrada: 177
- Consulta reenviada; evaluación pendiente: 1
- Contacto cerrado; sin evaluación científica: 1
- Detalles solicitados y enviados; evaluación pendiente: 1
- Entrega sin confirmar; sin evaluación científica: 4
- Hallazgo inicial rectificado por esta auditoría: 1
- Inconsistencia reconocida; parche público verificado: 1
- Limitación reconocida por equipo; derivada al editor: 1
- Observación reconocida; corrección anunciada: 1
- Respuesta automática; sin evaluación científica: 2

No verificamos ninguna corrección editorial publicada para los casos visibles al corte indicado.
Los estados podrán actualizarse con nueva evidencia pública o respuestas posteriores.

## Alcance y método

La auditoría interna contiene **19 casos de prioridad alta** y **301 media**.
Cada observación identifica un pasaje, cálculo o fragmento de código y expresa su límite.
Las reproducciones sintéticas prueban propiedades del método; no sustituyen resultados clínicos.
La ausencia de un antecedente localizado no certifica prioridad mundial.
Las 39 observaciones históricas de baja prioridad quedan fuera de este conjunto.

Para comunicar evidencia adicional o solicitar una rectificación, abrí un issue en este repositorio.
No publiques correos privados, datos de pacientes ni información personal en los issues.
