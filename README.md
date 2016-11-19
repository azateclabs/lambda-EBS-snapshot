# Lambda EBS Automated Snapshots
Questa funzione ha lo scopo di lanciare una snapshot su base giornaliera (o a scelta) per i propri volumi EBS legati ad istanze EC2. Quello che sarà necessario fare sarà inserire dei tag che possono essere backup\environment e che dovranno avere come valori yes\production.

La funzione si preoccuperà di fare anche un ulteriore tagging per la retention, verrà inserita una seconda funzione da schedulare con la stessa frequenza per la cancellazione delle snapshot al fine di non incrementare inutilmente il costo dell'infrastruttura su AWS.

Per avere maggiori dettagli sull'implementazione fare riferimento al video:

# IAM Policy
Create una policy contenente le seguenti permissions associandolo, poi, ad un ruolo da usare per AWS Lambda

{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "logs:*"
            ],
            "Resource": "arn:aws:logs:*:*:*"
        },
        {
            "Effect": "Allow",
            "Action": "ec2:Describe*",
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "ec2:CreateSnapshot",
                "ec2:DeleteSnapshot",
                "ec2:CreateTags",
                "ec2:ModifySnapshotAttribute",
                "ec2:ResetSnapshotAttribute"
            ],
            "Resource": [
                "*"
            ]
        }
    ]
}

# EBS Snapshots
Implementare la funzione che effettua la snapshot automatica non ha alcun suggerimento. Una volta creata la funzione AWS Lambda, impostare come trigger una schedulazione Cron (rules) da impostare su Cloudwatch. Assicurarsi di aver taggato correttamente le istanze come indicato sopra. Per poter rientrare nella schedulazione basterà aver creato un tag relativo all'ambiente, selezionando in automatico quelle di produzione, o nel caso inserire un tag backup da valorizzare con yes. Effettuare sempre una prova della funzione.
Non è possibile stimare preventivamente il costo della funzione, tuttavia essendo asincrona Lambda difficilmente avrà un costo visto che rientra nell'utilizzo gratuito della funzionalità. Discorso diverso per le snapshot di EBS che dipendono dal Business e dal dimensionamento delle istanze in flotta.

# EBS Delete Snapshots
La funzione di snapshot aggiunge alle snapshot effettuate un tag "DeleteOn" nel quale vi è un valore in formato YYYY-MM-DD della data dopo 7gg (retention impostata). Questa funzione si preoccupa di controllare, giorno dopo giorno, se la data corrisponde a quella odierna e, per quelle le quali rientrano in questa casistica, si preoccupa di cancellare le snapshot così da evitare costi ulteriori su EBS. Qualora la retention dev'essere modificata è possibile modificare il valore per rispettare le esigenze specifiche.

# ATTENZIONE
Nella funzione di Delete Snapshots è necessario inserire l'account ID del proprio ambiente AWS nella riga "account_ids = ['<accountid>']"
