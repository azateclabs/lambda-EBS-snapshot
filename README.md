# Lambda EBS Automated Snapshot
Questa funzione ha lo scopo di lanciare una snapshot su base giornaliera (o a scelta) per i propri volumi EBS legati ad istanze EC2. Quello che sarà necessario fare sarà inserire dei tag che possono essere backup\environment e che dovranno avere come valori yes\production.

La funzione si preoccuperà di fare anche un ulteriore tagging per la retention, verrà inserita una seconda funzione da schedulare con la stessa frequenza per la cancellazione delle snapshot al fine di non incrementare inutilmente il costo dell'infrastruttura su AWS.
