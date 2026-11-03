# Guía de continuación

El repositorio conserva la estructura profesional del laboratorio y la evidencia que sí se ha observado. Las tres VMs están detenidas; todavía no se han recuperado sus archivos ni validado el funcionamiento de Splunk.

## Confirmado

- Tres nodos: `splunk-sh`, `splunk-idx` y `splunk-uf`, en `us-central1-c`.
- Los tres usan `e2-medium`, imagen CentOS Stream 10 y disco de arranque de 20 GB.
- Existen reglas específicas para los puertos 8000, 8089 y 9997, además de reglas predeterminadas más amplias.
- Los discos están configurados para borrarse con las VMs. No se ha borrado ni modificado ningún recurso de Google Cloud.

## Pendiente

Encender las VMs y registrar acceso SSH, si hace falta, requiere autorización explícita del propietario. Después se recuperarán configuraciones, scripts, dashboards y evidencia real. Los archivos nuevos en `configs/examples/` son referencias y **no representan archivos recuperados**.

Consulta el [procedimiento de recuperación](recovery.md), el [registro de evidencia](../evidence/README.md) y la [lista de preservación](preservation-checklist.md). No elimines el proyecto mientras el rescate siga incompleto.
