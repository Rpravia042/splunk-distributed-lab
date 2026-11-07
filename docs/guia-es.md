# Guía breve en español

El laboratorio ya tiene un repositorio privado con documentación en inglés, configuración original revisada, script de CPU/RAM, tarea programada, dashboard y capturas reales.

## Confirmado

- Tres VMs en `us-central1-c`, encendidas con autorización del propietario; los tres servicios Splunk están activos.
- UF envía tres tipos de datos al índice `linux_os` del Indexer.
- Search Head consulta el Indexer: una búsqueda documentada devolvió 129.310 eventos y el peer estaba `Up / Healthy`.
- El dashboard mostró CPU 5,4 % y RAM 21,02 %. Se conservaron su definición y comportamiento originales.
- Se verificaron 41 archivos recuperados y se seleccionaron 19 derivados revisados para publicar. Los originales y las exportaciones de eventos quedan fuera de GitHub.

## Cómo recorrerlo

Empieza por el [README](../README.md), luego revisa [arquitectura](architecture.md), [validaciones](validation.md) y [configuración recuperada](../configs/recovered/README.md). La [guía de reconstrucción](rebuild.md) explica cómo recrear el diseño en otro entorno.

## Preservación de Google Cloud

Consulta la [lista de preservación](preservation-checklist.md). Se conservarán las mismas VMs para la entrevista; siguen encendidas y consumen recursos. No se eliminaron VMs ni índices, ni se cambiaron la red, las contraseñas o la configuración de Splunk. Se autorizó ampliar únicamente el disco de Search Head de 20 a 30 GB y completar su partición y sistema de archivos. Apagar o eliminar requiere una autorización posterior y concreta.

Hay limitaciones documentadas: HTTP en Splunk Web, forwarding sin TLS, avisos de espacio/I/O y ausencia de alta disponibilidad. La sanitización automática ayuda, pero no sustituye la revisión humana antes de hacer público el repositorio.

## Estado para la entrevista

Se conservarán las mismas tres VMs. No se reinstaló Splunk ni se modificaron sus configuraciones originales. En Search Head, cinco archivos clave coinciden con sus hashes originales, incluido el dashboard y la unidad de servicio.

El respaldo comprimido de **8.697.141 eventos** pasó la validación completa en la VM y su copia local coincide en tamaño y SHA-256. Ambas copias se conservan de forma privada. La clave temporal limitada a leer ese respaldo se retiró tras la transferencia; también se eliminó su clave privada local. No es una restauración completa probada.

El bloqueo de búsquedas por espacio quedó resuelto el **7 de noviembre de 2026**. Google Cloud ya mostraba 30 GB, pero faltaba ampliar la partición de Linux y XFS. Se completó sin reiniciar la VM ni Splunk. La comprobación final encontró unos **15 GB libres**, cuatro muestras recientes de UF consultadas desde SH en IDX y el dashboard original con CPU **4 %** / RAM **23,23 %**. [Cambios y comprobaciones](change-record.md).

Para la próxima entrevista, enciende las tres VMs si están detenidas, confirma la dirección actual de `splunk-sh` en Google Cloud y abre Splunk Web en su puerto 8000. Inicia sesión con tus credenciales habituales. Ejecuta la consulta breve de [validación](validation.md) y abre **Dashboards → UF System Performance**. Comprueba de nuevo los resultados y el espacio antes de demostrarlo; esta captura no garantiza su estado futuro.
