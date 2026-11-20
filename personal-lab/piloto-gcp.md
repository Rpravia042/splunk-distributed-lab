# Reconstrucción personal en Google Cloud

Propuesta preparada el 20 de noviembre de 2026. Proyecto personal creado y verificado en su panel de Google Cloud el 20 de noviembre de 2026. Pendientes: red del piloto, instancias, instalación de Splunk y prueba del recorrido completo. La cuenta de prueba comparte su crédito entre proyectos.

| Nodo | Tipo propuesto | Memoria | Disco pd-balanced |
|---|---|---|---|
| personal-sh | e2-standard-2 | 8 GiB | 40 GiB |
| personal-idx | e2-standard-2 | 8 GiB | 40 GiB |
| personal-uf | e2-small | 2 GiB | 20 GiB |

Dimensionamiento experimental para un volumen sintético pequeño. Verificar mínimos de la versión elegida, cuota y uso real antes de mantener el piloto encendido.

## Estimación en Iowa

Dos instancias a USD 0,06701142/h y una a USD 0,016752855/h suman USD 0,150775695/h. Cuarenta horas de uso simultáneo cuestan unos USD 6,03. Conservar 100 GiB durante 730 horas cuesta unos USD 10 a USD 0,000136986 por GiB-h. Total base aproximado USD 16,03. El cómputo continuo durante las mismas 730 horas elevaría el total base a unos USD 120,07. Red, copias, impuestos aplicables y otros proyectos se calculan aparte. El crédito y los límites de prueba se comparten por cuenta de facturación.

## Secuencia para la primera sesión

1. Crear un proyecto personal nuevo y registrar su ID y número. Verificar que ambos corresponden al proyecto nuevo antes de aprovisionar. Usar el proyecto explícito en cada operación. Filtrar alertas de presupuesto por proyecto y programar la detención de las VMs al acabar la sesión. Una alerta informa del gasto y por sí sola no lo limita.
2. Crear una VPC propia con subred privada, sin peering ni rutas hacia el entorno de entrevista. Preparar acceso administrativo restringido por IAP. Obtener los instaladores oficiales en la Mac y transferirlos por el acceso administrativo para evitar un NAT permanente. Revisar imágenes de SO, licencia y dependencias antes de iniciar el cómputo.
3. Instalar Search Head e Indexer desde cero, con identidades, credenciales y confianza nuevas. Usar el Universal Forwarder en el tercer nodo. Las reglas entre nodos deben limitarse al origen, destino y puerto de cada flujo: UF a IDX para ingestión y SH a IDX para búsqueda. Verificar cifrado y validación de certificados.
4. Generar un evento sintético con un identificador de prueba, buscarlo desde personal-sh y verificar host personal-uf y splunk_server personal-idx. Registrar hora del evento, indexación y recuperación. Probar después el medidor capacity.py y distinguir falta de espacio de falta de muestras.
5. Registrar tiempos de actividad y costos del proyecto personal; conservar evidencia saneada y detener solo las instancias personales al acabar la práctica.

Fuentes: [cómputo](https://cloud.google.com/products/compute/pricing/general-purpose), [discos](https://cloud.google.com/compute/disks-image-pricing), [prueba](https://cloud.google.com/free/docs/free-cloud-features).
