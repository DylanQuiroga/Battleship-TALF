# Battleship TALF

## Descripción general

Combate Naval (nombre de la aplicación creada) es un juego de estrategia basado en el clásico juego de ”Batalla Naval”. Los jugadores colocan sus barcos en un tablero y tratan de adivinar la ubicación de los barcos del oponente para hundirlos antes de que sus propios barcos sean hundidos.

Para llevar a cabo este proyecto de replicar el Battleship con Python y con comandos permitidos por una gramática, buscamos un repositorio en GitHub de un sistema de chat, esto con la idea de que el juego tu viera también un sistema de chat y además de reducir tiempo a la hora de crear un sistema de mensajería. Luego de una búsqueda y probando distintos códigos nos quedamos con el siguiente:

https://github.com/arijitiiest/Socket-Chat-App

Decidimos quedarnos con este programa, ya que es bastante robusto a la hora de generar errores y el código se entiende muy bien.

[![img1](https://media.canva.com/v2/image-resize/format:PNG/height:474/quality:100/uri:ifs%3A%2F%2FM%2F4f01bf73-8776-40db-b69d-a20991d1680a/watermark:F/width:395?csig=AAAAAAAAAAAAAAAAAAAAABTW4ka9AeBGBqsN2kaXwhRntDCpWhhW6ShugCHvmoCL&exp=1790839398&osig=AAAAAAAAAAAAAAAAAAAAALxqLSvn8n6RilNlb47h40yVb_RAduknpVn2FB67CMdi&signer=media-rpc&x-canva-quality=screen_3x)]


[![img2](https://media.canva.com/v2/image-resize/format:PNG/height:531/quality:100/uri:ifs%3A%2F%2FM%2F912cb75e-4f7a-4410-99db-7ec0fe5b5442/watermark:F/width:468?csig=AAAAAAAAAAAAAAAAAAAAAAdkR-PSz_3X4HPL648dDV3lNGSaeZShPfSusAgLxggN&exp=1790841200&osig=AAAAAAAAAAAAAAAAAAAAAI_ZTYpHY4hIT7whyMAiTu9oZHSxJINXVmUpsN0bVtnc&signer=media-rpc&x-canva-quality=screen_3x)]

Reflexionamos sobre qué extras podríamos añadir al juego, ya que Battleship solo incluye dos acciones: colocar barcos y atacar al enemigo utilizando coordenadas. Sin embargo, implementar solo estas acciones no haría el juego tan emocionante, por lo que añadimos los siguientes extras:

* Defender: Defiende una parte del barco (una casilla) y hace que el ataque del enemigo tenga una probabilidad del 50 por ciento de fallar. Ej: Defender A1
* Escanear: Escanea una casilla en un ´area de 3x3 casillas. Ej.: Escanear G5

Además de incluir los siguientes comandos para hacer funcionar el juego mediante comandos:

* Atacar: Ataca una casilla. Ej: Atacar A1
* Comenzar: Comienza el juego de Battleship.
* Cambio: Cambia el turno.
* Tablero: Permite ver tu tablero o el del enemigo. Ej: Tablero propio / Tablero enemigo.
* Ayuda: Muestra todos los comandos disponibles

Con esto decidido, comenzamos a investigar cómo implementar estos comandos con PLY. Optamos por PLY debido a su facilidad de uso y porque no requiere tanto código como ANTLR, además de no necesitar JAVA para funcionar. Finalmente, obtuvimos la siguiente estructura:

[![img3](https://media.canva.com/v2/image-resize/format:PNG/height:550/quality:100/uri:ifs%3A%2F%2FM%2Fd4f8d5d3-a293-4e61-82b8-0284bc12275b/watermark:F/width:296?csig=AAAAAAAAAAAAAAAAAAAAAF-nkBQohOi_9iC3S2WE1MafBHAHCwDhLu9cjjwgah5t&exp=1790838974&osig=AAAAAAAAAAAAAAAAAAAAACvUDWdddMeORefkmF7QUJtWFTm6pM1aaPrXGVd8yKoT&signer=media-rpc&x-canva-quality=thumbnail_large)]

Continue leyendo el pdf
[Proyecto_final_TALF.pdf](https://github.com/user-attachments/files/16111804/Proyecto_final_TALF.pdf)
