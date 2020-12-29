# EVA_laserbridge
# Il progetto consente di utilizzare una raspberry come lettore digitale pilotato da seriale
# Protocolli implementati attualmente 
# -Philips ad uso specifico con schede ATARI DL e SA
# -Pioneer LDV4400 e 4300
# -Sony 1450
# il progetto non è completo e vuole presentare un idea di utilizzo del sistema VLC + Seriale + raspberry al fine di sostituire il vecchio
# lettore laserdisc con un sistema digitale.
# Ogni modifica o suggerimento è ben accetto

Il software utilizza una seriale USB collegata la raspberry per ricevere ed inviare i comandi alla scheda o software che crede di dialogare con
un lettore laserdisc.
Una volta interpretati i comandi ricevuti dalla seriale il sistema comanda il lettore VLC al fine di visualizzare su uscita composita o hdmi il video.
Quindi restituisce alla serial i comandi di risposta.

Testato su raspberry PI 1 e 2. con raspian 5. Attenzione VLC deve avere attive le api per HTTP
