# Corso di Big Data - Progetto Finale
Nel seguente progetto è stata realizzata un'architettura di Big Data per il monitoraggio in real time di dati provenienti da sensori IoT. L'architettura è composta da 5 blocchi principali:
- **Sensori IoT**: non avendo accesso ai sensori l'invio dei dati è stato simulato con un script Python presente all'interno della cartella *iot-data-producer*.
- **Kafka**: per lo scambio di messaggi tra i sensori e il blocco di processamento dei dati.
- **Spark Structured Streaming**: per il processamento dei dati. Lo script è presento all'interno della cartella *spark*.
- **InfluxDB**: time series database per il salvataggio dei dati.
- **Grafana**: per la visualizzazione in real time dei dati salvati nel database.

Il tutto è stato testato utilizzando contenitori Docker.
