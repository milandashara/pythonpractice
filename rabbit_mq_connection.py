import pika
import pika.connection
import pika.credentials as pika_credentials

connection = pika.BlockingConnection(pika.ConnectionParameters('contrail.rabbitmq.uk2.prod.skyscanner.local',5672,  'contrail', socket_timeout=300,credentials=pika_credentials.PlainCredentials('svc_travelrankings', 'svC_7R4Nsp0R7_S7472')))
connection.channel()
print connection