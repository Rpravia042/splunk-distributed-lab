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

## Antes de cerrar Google Cloud

Consulta la [lista de preservación](preservation-checklist.md). El propietario solicitó conservar también todos los eventos; su copia privada se verifica por separado. Las VMs siguen encendidas y consumen recursos. No se ha autorizado ni realizado su eliminación, cambios de red, rotación de credenciales o reconfiguración de Splunk. Apagar o eliminar requiere una autorización posterior y concreta.

Hay limitaciones documentadas: HTTP en Splunk Web, forwarding sin TLS, avisos de espacio/I/O y ausencia de alta disponibilidad. La sanitización automática ayuda, pero no sustituye la revisión humana antes de hacer público el repositorio.

## Estado para la entrevista

Se conservarán las mismas tres VMs. No se reinstaló Splunk ni se modificaron sus configuraciones originales. En Search Head, cinco archivos clave coinciden con sus hashes originales, incluido el dashboard y la unidad de servicio.

El respaldo comprimido de 8.697.141 eventos pasó la validación completa en la VM, pero todavía requiere una copia local verificada. Su almacenamiento dejó poco espacio libre en Search Head y Splunk rechazó una búsqueda nueva por el mínimo de 5.000 MB. Antes de una demostración hay que liberar el almacenamiento del respaldo después de verificar su copia y repetir una búsqueda pequeña. El servicio continúa activo; los datos originales siguen en sus índices.
