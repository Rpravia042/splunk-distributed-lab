# Reconstrucción personal en Google Cloud

Propuesta preparada el 20 de noviembre de 2026. Proyecto personal creado y verificado en su panel de Google Cloud el 20 de noviembre de 2026. Pendientes: red del piloto, instancias, instalación de Splunk y prueba del recorrido completo; el guion del ensayo de dos horas está abajo y no se ha ejecutado. La cuenta de prueba comparte su crédito entre proyectos.

| Nodo | Tipo propuesto | Memoria | Disco pd-balanced |
|---|---|---|---|
| personal-sh | e2-standard-2 | 8 GiB | 40 GiB |
| personal-idx | e2-standard-2 | 8 GiB | 40 GiB |
| personal-uf | e2-small | 2 GiB | 20 GiB |

Dimensionamiento experimental para un volumen sintético pequeño. Verificar mínimos de la versión elegida, cuota y uso real antes de mantener el piloto encendido.

## Estimación en Iowa

Dos instancias a USD 0,06701142/h y una a USD 0,016752855/h suman USD 0,150775695/h. Cuarenta horas de uso simultáneo cuestan unos USD 6,03. Conservar 100 GiB durante 730 horas cuesta unos USD 10 a USD 0,000136986 por GiB-h. Total base aproximado USD 16,03. El cómputo continuo durante las mismas 730 horas elevaría el total base a unos USD 120,07. Red, copias, impuestos aplicables y otros proyectos se calculan aparte. El crédito y los límites de prueba se comparten por cuenta de facturación.

Una sesión de dos horas cuesta unos USD 0,30 de cómputo. Con los 100 GiB conservados, el primer mes ronda USD 10,30.

El almacenamiento temporal de los instaladores y las operaciones del bucket se calculan aparte. Crear el bucket en la misma región y retirarlo al terminar el ensayo. Comprobar la política de eliminación diferida al crearlo para saber cuánto tiempo seguirían almacenados los objetos.

## Ensayo de dos horas

Revisado el 24 de noviembre de 2026 para Splunk Enterprise 10.6 (rama 10.6.2, con los dos instaladores del mismo build verificados localmente mediante SHA-512). Objetivo único: un evento sintético sale de personal-uf, llega a personal-idx y aparece en personal-sh. El medidor capacity.py y el panel quedan para otra sesión. Las VMs de entrevista quedan fuera. Definir `PERSONAL_PROJECT` con el ID del proyecto personal y pasarlo expresamente en cada comando de Google Cloud. Verificar su número antes de aprovisionar. Para detener las VMs, pasar sus tres nombres en lugar de seleccionar todas las instancias del proyecto.

### A. Preparación con las VMs apagadas

| # | Qué preparar | Comprobación observable |
|---|---|---|
| A1 | Confirmar el proyecto de destino y que la API de Compute Engine está activa. | `gcloud projects describe "$PERSONAL_PROJECT" --format='value(projectNumber)'` coincide con el número visible en el panel del proyecto personal. |
| A2 | Saldo y fecha de fin de la prueba gratuita. Al terminar, la cuenta se cierra y se detienen todos sus proyectos, incluido el de entrevista. | Fecha de fin posterior al ensayo y saldo suficiente. |
| A3 | Cuotas disponibles de CPU E2, instancias y discos en us-central1. | Hay capacidad para las tres VMs y 100 GiB en el proyecto personal. |
| A4 | VPC en modo personalizado con una subred privada dedicada que no se solape con la red de entrevista y con Private Google Access. Sin IP externas, sin NAT ni peering. | `gcloud compute networks list` muestra la VPC del ensayo. |
| A5 | IAP permite SSH por tcp:22. Abrir Splunk Web con reenvío local por SSH y mantener tcp:8000 fuera del firewall. Permitir UF→IDX por tcp:9997 y SH→IDX por tcp:8089. Denegar el resto de la salida, salvo tcp:443 temporal hacia la IP virtual publicada de restricted.googleapis.com. | Revisar las reglas de la VPC personal y que el acceso HTTPS no tenga un destino abierto a Internet. |
| A6 | Comprobar que quien ejecuta el ensayo tiene permiso para el túnel IAP y para iniciar sesión en la VM según use OS Login o claves de instancia. | Verificar acceso a Cloud Shell y permisos de proyecto antes de crear las VMs. |
| A7 | Instaladores oficiales de Enterprise y del UF en la Mac, con sus sumas SHA-512 publicadas. Usar los paquetes Linux x86-64 de la misma build. | `shasum -a 512 -c` da OK. |
| A8 | Bucket privado regional con los dos instaladores, acceso uniforme y prevención de acceso público. Adjuntar a las VMs una cuenta de servicio dedicada sin llaves, con scope de lectura de Cloud Storage y permiso Storage Object Viewer únicamente en ese bucket. | Verificar los dos objetos, la política del bucket y que la cuenta carezca de roles de proyecto. Preparar la resolución de storage.googleapis.com a la IP virtual publicada de restricted.googleapis.com para que HTTPS conserve el dominio y valide el certificado. |
| A9 | CA propia y certificados de los nodos personales. Usar nombres y SAN coherentes con los destinos, EKU según el rol y hora de emisión válida tras sincronizar los relojes. La clave de la CA permanece en la preparación privada y cada VM recibe solo su material por SSH/IAP. | `openssl verify -CAfile` da OK; `openssl x509 -noout -ext subjectAltName,extendedKeyUsage` muestra lo esperado. |
| A10 | Configuración escrita. IDX: `inputs.conf` con `[splunktcp-ssl:9997]` y `[SSL]` (`serverCert`, `requireClientCert = true`, `sslCommonNameToCheck`), y `server.conf` con `[sslConfig] sslRootCAPath`. UF: `outputs.conf` con `clientCert`, `sslVerifyServerCert = true` y `sslCommonNameToCheck`, y `server.conf` con `sslRootCAPath`, también necesario en el cliente. | Los nombres coinciden con los SAN de A9. Configurar también la CA y la validación de nombre en el canal SH→IDX por 8089. Si una clave está cifrada, configurar su contraseña en la VM. |
| A11 | Guion de instalación por rol: crear el usuario de servicio, extraer, copiar `user-seed.conf`, cambiar el propietario, `enable boot-start -systemd-managed 1 -user … --accept-license` y arrancar. | `bash -n` sin errores. |
| A12 | Plantilla de evidencia con las búsquedas de C y una tabla de tiempos. | — |

### B. Errores que pueden hacer perder la sesión

**Licencia.** La Enterprise Trial está pensada para una instancia. En una prueba distribuida, cada instancia usa su propia Trial autogenerada y no se puede centralizar la gestión de licencias. No configurar license manager ni license peers. Elegir Free elimina la búsqueda distribuida y la autenticación. El UF usa la licencia Forwarder automáticamente. La Trial dura 60 días desde la instalación.

**Permisos.** Splunk no crea el usuario de servicio. `user-seed.conf` va en `etc/system/local` antes del primer arranque y se ignora si ya existe `etc/passwd`; el hash puede generarse con `splunk hash-passwd` en la VM, después de extraer. El IDX solo actúa como peer si su contraseña de admin ya no es la predeterminada, y `add search-server` exige credenciales de nivel admin en el peer. Con `systemd-managed`, `splunk start|stop` se traduce a `systemctl`. La descarga desde el invitado puede usar curl y un token obtenido del servidor de metadatos, sin instalar gcloud en la VM. Pasar el encabezado de autorización por entrada estándar y evitar que el token aparezca en argumentos, historial o registros.

**Certificados.** Un CN igual al de la CA hace fallar la validación. Si `sslPassword` no coincide, el IDX no abre el 9997. Un `notBefore` futuro produce «not yet valid». 10.6 ya no admite TLS 1.0 ni 1.1 entre componentes.

### C. Secuencia con el reloj en marcha (T = creación de las VMs)

| T | Operación | Resultado observable | Si falla |
|---|---|---|---|
| +0 | Crear las tres VMs con `--max-run-duration=2h --instance-termination-action=STOP` y sin IP externa. | `describe` muestra `RUNNING` y `terminationTimestamp` en T+2h. | Sin timestamp: detener ya (corte 0). |
| +5 | SSH por IAP a los tres nodos: `hostname`, `timedatectl`, `curl -m5 https://example.com`. | Nombres personal-*, reloj sincronizado y curl falla porque no hay salida a Internet. | — |
| +10 | Descargar del bucket en cada VM y verificar SHA-512. Revocar el permiso del bucket y retirar la regla temporal tcp:443. | Sumas OK. | Sin instaladores a T+20: apagar (corte 1). Verificar después que se revoque la lectura del bucket y se retire el permiso temporal de salida. |
| +15 | Instalar SH e IDX en paralelo; después, el UF. | `systemctl is-active` da `active`; `splunk version` coincide; el IDX escucha 9997 y 8089; licencia Trial activa. | — |
| +40 | Arrancar el UF con TLS. | `splunk list forward-server` muestra personal-idx:9997 activo; ningún error SSL en `splunkd.log`. | A T+60: recopilar el diagnóstico y detener si no se confirma TLS. |
| +60 | Agregar el peer personal por Splunk Web desde el túnel SSH, con TLS y validación de nombre en el enlace SH→IDX. | `splunk list search-server` muestra el peer en estado Up. | Corte 2 a T+75. |
| +75 | En el UF: UUID nuevo, una línea en un archivo nuevo y `splunk add oneshot <archivo> -index main -sourcetype ensayo:ruta`, sin `-host`. | — | — |
| +78 | En personal-sh: `index=main sourcetype=ensayo:ruta "UUID" \| addinfo \| eval lag=_indextime-_time \| table _time _indextime info_search_time lag host splunk_server`. | Una sola fila con host=personal-uf y splunk_server=personal-idx. | — |
| +80 | `\| rest /services/server/info splunk_server=local`, lista de peers e `index=_internal host=personal-idx group=tcpin_connections`. | serverName=personal-sh, solo personal-idx como peer y conexión de personal-uf desde su subred. | Sin evento a T+100: capturar en privado el tramo de `splunkd.log` relevante y apagar a T+105. |
| +100 | Guardar evidencia saneada. | — | — |
| +105 | `gcloud compute instances stop personal-sh personal-idx personal-uf --zone=… --project="$PERSONAL_PROJECT"`. | Las tres en `TERMINATED`. | El límite de ejecución las detiene a T+2h. |

Apagar en cuanto el siguiente paso dependa de algo que solo se corrige fuera de las VMs (red, certificados o licencia), y nunca después de T+105. Ampliar el límite exige detener y volver a arrancar.

### D. Confirmar el apagado aunque la Mac esté cerrada

La app móvil de Google Cloud muestra las tres VMs detenidas en el proyecto personal. Después, `gcloud compute instances list --project="$PERSONAL_PROJECT" --format="table(name,status,lastStartTimestamp,lastStopTimestamp)"`. Una detención por límite deja una operación `compute.instances.deferredStop`; una manual deja `v1.compute.instances.stop` en la auditoría de administración.

### E. Lo que sigue consumiendo crédito

Los 100 GiB de disco cuestan unos USD 0,33 al día mientras existan, incluso con las VMs detenidas. Este diseño no usa IP públicas ni NAT. Revisar costo y retención del bucket y de cualquier snapshot antes de cerrar la sesión. El proyecto de entrevista comparte el crédito.

### Supuestos pendientes

Queda por verificar en vivo la cuota efectiva, el permiso de IAP, la descarga mediante Private Google Access, la configuración de ambos canales TLS y la búsqueda de extremo a extremo. El límite de ejecución se aplica por VM y se reinicia desde el último arranque. Registrar la hora que devuelve Compute Engine en cada caso. Los instaladores de la misma build ya pasaron la comprobación SHA-512 en la Mac.

Fuentes: [cómputo](https://cloud.google.com/products/compute/pricing/general-purpose), [discos](https://cloud.google.com/compute/disks-image-pricing), [prueba](https://docs.cloud.google.com/free/docs/free-cloud-features), [cuotas](https://docs.cloud.google.com/compute/quotas), [ciclo de vida](https://docs.cloud.google.com/compute/docs/instances/instance-life-cycle), [límite de ejecución](https://docs.cloud.google.com/compute/docs/instances/limit-vm-runtime), [IAP](https://docs.cloud.google.com/iap/docs/using-tcp-forwarding), [Private Google Access](https://docs.cloud.google.com/vpc/docs/configure-private-google-access), [instalación 10.6](https://help.splunk.com/en/splunk-enterprise/get-started/install-and-upgrade/10.6/install-splunk-enterprise-on-linux-or-macos/install-on-linux), [user-seed.conf 10.6](https://help.splunk.com/en/splunk-enterprise/administer/admin-manual/10.6/configuration-file-reference/10.6.0-configuration-file-reference/user-seed.conf), [systemd 10.6](https://help.splunk.com/en/data-management/splunk-enterprise-admin-manual/10.6/start-splunk-enterprise-and-perform-initial-tasks/run-splunk-enterprise-as-a-systemd-service), [search peers 10.6](https://help.splunk.com/en/splunk-enterprise/administer/distributed-search/10.6/deploy-distributed-search/add-search-peers-to-the-search-head), [TLS 10.6](https://help.splunk.com/en/splunk-enterprise/administer/manage-users-and-security/10.6/secure-splunk-platform-communications-with-transport-layer-security-certificates/configure-splunk-indexing-and-forwarding-to-use-tls-certificates), [validación de nombre 10.6](https://help.splunk.com/en/splunk-enterprise/administer/manage-users-and-security/10.6/secure-splunk-platform-communications-with-transport-layer-security-certificates/configure-tls-certificate-host-name-validation-for-secured-connections-between-splunk-software-components), [licencias 10.6](https://help.splunk.com/en/data-management/splunk-enterprise-admin-manual/10.6/configure-splunk-licenses/types-of-splunk-enterprise-licenses), [cuentas de servicio de Compute Engine](https://docs.cloud.google.com/compute/docs/access/service-accounts), [precios de Cloud Storage](https://cloud.google.com/storage/pricing), [eliminación diferida](https://docs.cloud.google.com/storage/docs/soft-delete).
