# AlarmaEdenly

Este proyecto implementa una alarma inteligente con capacidad de activación remota, watchdog y actualizaciones OTA.

Duración de batería: diría un target mínimo aceptable sería 1 mes entre recargas.

Cuándo sonar:


Watchdog de la controladora principal. Suena si no recibe respuesta/ACK desde un host o si pierde conectividad inalámbrica local.

API para poder hacerla sonar a través de la red inalámbrica que utilice.

Red inalámbria:

La instalación ya tiene red WiFi y Zigbee.

Sería interesante estudiar LoRa por su bajo consumo y alto alcance pero ahora mismo no tenemos gateway (haría falta algo para convertir LoRa<>Ethernet).

Botón/interruptor para apagado.

Sistema para configurar los parámetros: puede ser una conexión USB/TTL o mediante WiFi ad-hoc o botón de emparejamiento.

Se colocará en el exterior pero cubierta de la lluvia.

intensidad: >100 dB a un metro.

Carga mediante:

o USB-c 5V, para que sea fácil reutilizar otros cargadores y unificar con soluciones futuras,

o pilas recargables de 1,2V (Ni-CD) o de 1,5V (Litio) (tal vez sea la opción más sencilla para arrancar),

o un cargador específico que no sea difícil de comprar recambios.

## Instalación
1. Clona el repositorio.
2. Instala las dependencias: `pip install -r requirements.txt`.
3. Ejecuta el programa: `python src/main.py`.
