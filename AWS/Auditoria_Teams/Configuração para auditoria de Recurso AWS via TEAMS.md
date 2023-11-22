# Configuração para auditoria de Recurso AWS via Teams
### Documentação criada visando guiar a criação de notificações de alterações nos Recursos da AWS

* Criar um grupo no Teams com Webhook
* Criar o código que irá notificar via Lambda
* Criar um Cloud Trail para coleta das alterações nos serviços
* Criar conf no Cloudwatch para filtrar as alterações feitas
* Criar um SNS para gerar a notificação via Teams

# Passo-a-Passo

## Teams

Será necessário criar um _Chat_ no Teams e baixar a extenção _Webhook_ para gerar o link de intergração.

## Lambda
Será necessário criar uma função Lambda para gerar as notificações automaticas. Nessa função será necessário descrever os _eventnames_ e as descrições das mensagens(OBS: Todos os exemplos abaixo, estão em python 3.7), como os exemplos a seguir:


### Eventos para Bucket S3

#### Code
~~~python
import json
import os
import urllib.request

def lambda_handler(event, context):
  teams ="(Webhook gerado)"
  s1 = json.dumps(event)
  d2 = json.loads(s1)
  print(d2) # adicione esta linha para imprimir o valor de "d2"
  message = {'text': 'Uma alteração foi realizada no S3.'}
  if d2['detail']['eventName'] == 'DeleteBucketTagging':
    message['text'] = f"Uma tag foi removida do bucket {d2['detail']['requestParameters']['bucketName']} bucket pelo usuário {d2['detail']['userIdentity']['userName']}."
  if d2['detail']['eventName'] == 'PutBucketTagging':
    message['text'] = f"Uma tag foi adicionada do bucket {d2['detail']['requestParameters']['bucketName']} bucket pelo usuário {d2['detail']['userIdentity']['userName']}."
  if d2['detail']['eventName'] == 'DeleteBucket':
    message['text'] = f"Um bucket de nome {d2['detail']['requestParameters']['bucketName']} foi deletado pelo usuário {d2['detail']['userIdentity']['userName']}."
  if d2['detail']['eventName'] == 'CreateBucket':
    message['text'] = f"Um bucket de nome {d2['detail']['requestParameters']['bucketName']} foi criado pelo usuário {d2['detail']['userIdentity']['userName']}."  
  data = json.dumps(message).encode('ascii')
  req = urllib.request.Request(teams, data)
  try:
    response = urllib.request.urlopen(req)
    response.read()
  except Exception as e:
    print(e)
~~~

#### Test
~~~json
{
  "source": [
    "aws.s3"
  ],
  "detail-type": [
    "AWS API Call via CloudTrail"
  ],
  "detail": {
    "eventSource": [
      "s3.amazonaws.com"
    ],
    "eventName": [
      "DeleteBucketTagging",
      "PutBucketTagging",
      "DeleteBucket",
      "CreateBucket"
    ]
  }
}
~~~

### Eventos para o RDS

#### Code
~~~python
import json
import os
import urllib.request

def lambda_handler(event, context):
  teams ="(webhook gerado)"
  s1 = json.dumps(event)
  d2 = json.loads(s1)
  print(d2) # adicione esta linha para imprimir o valor de "d2"
  message = {'text': 'An RDS event occurred.'}
  if d2['detail']['eventName'] == 'RemoveTagsFromResouce':
    message['text'] = f"A tag foi removida do banco {d2['detail']['requestParameters']['resourceName']} pelo usuário {d2['detail']['userIdentity']['userName']}."
  if d2['detail']['eventName'] == 'AddTagsToResource':
    message['text'] = f"A tag foi adicionada no banco {d2['detail']['requestParameters']['resourceName']} pelo usuário {d2['detail']['userIdentity']['userName']}."
  data = json.dumps(message).encode('ascii')
  req = urllib.request.Request(teams, data)
  try:
    response = urllib.request.urlopen(req)
    response.read()
  except Exception as e:
    print(e)
~~~

#### Test
~~~json
{
  "source": [
    "aws.rds"
  ],
  "detail-type": [
    "AWS API Call via CloudTrail"
  ],
  "detail": {
    "eventSource": [
      "rds.amazonaws.com"
    ],
    "eventName": [
      "RemoveTagsFromResouce",
      "AddTagsToResource"
    ]
  }
}
~~~

### Eventos para o ASG

#### Code
~~~python
import json
import os
import urllib.request
def lambda_handler(event, context):
    teams = "(Webhook gerado)"
    s1 = json.dumps(event)
    d2 = json.loads(s1)
    print(d2) # adicione esta linha para imprimir o valor de "d2"
    message = {'text': 'An ASG event occurred.'}
    if d2['detail']['eventName'] == 'DeleteTags':
        tags = d2['detail']['requestParameters']['tags']
        resourceId = tags[0]['resourceId'] if tags else None
        message['text'] = f"Uma tag foi deletada do ASG {resourceId} pelo usuário {d2['detail']['userIdentity']['userName']}."
    elif d2['detail']['eventName'] == 'CreateOrUpdateTags':
        tags = d2['detail']['requestParameters']['tags']
        resourceId = tags[0]['resourceId'] if tags else None
        message['text'] = f"Uma tag foi adicionada ao ASG {resourceId} pelo usuário {d2['detail']['userIdentity']['userName']}."
    data = json.dumps(message).encode('ascii')
    req = urllib.request.Request(teams, data)
    try:
        response = urllib.request.urlopen(req)
        response.read()
    except Exception as e:
        print(e)
~~~
#### Test
~~~json
{
  "source": [
    "aws.autoscaling"
  ],
  "detail-type": [
    "AWS API Call via CloudTrail"
  ],
  "detail": {
    "eventSource": [
      "autoscaling.amazonaws.com"
    ],
    "eventName": [
      "DeleteTags",
      "CreateOrUpdateTags"
    ]
  }
}
~~~

OBS: O _eventname_ irá variar para cada serviço da AWS, o recomendado é localizar o _eventname_ através do CloudTrail ou Cloudwatch. Ou na seguinte referencia: <https://www.gorillastack.com/blog/real-time-events/cloudtrail-event-names/>.

## CloudTrail
Ao criar o CloudTrail, deverá ser:
* Criar um _bucket_s3_ para armazenar os logs gerados. 
* Habilitar _tópico-SNS_ e também o _CloudWatch-Logs_.
* Desabilitar _Criptografia SSE-KMS do arquivo de log_. 
* Habilitar a opção _Evento de dados_ e selecionar a fonte de dados = S3.
* Revisar e criar a tilha.
  1. Exemplo
    ![image-2.png](./image-2.png)

## CloudWatch
Ao abrir a guia do CloudWatch, ir na opção _Regras_ localizada dentro de _Eventos_, ao criar a _Regras_, deverá ser:
* Informar a origem do evento no campo _Nome do Serviço_.
* Em tipo de evento informar _AWS API Call via CloudTrail_.
* Marcar _Operações específicas_e informar os _eventsnames_ desejados.
* Em destino, informar o _SNS_ desejado e deverá ser adicionado mais um destino informando o _ARN LAMBDA CRIADO PARA EVENTO ESPECÍFICO_.
* Revisar e criar o evento.
  1. Exemplo
    ![Exemplo](./image-1.png)

## SNS
Após abrir o SNS deverá ser informado uma assinatura para o mesmo para isso deverá ser:
* Ir em _Assinaturas_ e criar uma nova assinatura.
* Informar o _ ARN DO TÓPICO_.
* Informar o protocolo = _lambda_ e na sequencia informar o _ARN LAMBDA CRIADO PARA EVENTO ESPECÍFICO_.
* Revisar e criar a assinatura.
  1. Exemplo
    ![image.png](./image.png)

## Após realizar todas as configurações efetuar o teste, caso o mesmo tenha exito, será notificado no seu teams.

## Referências
* <https://aws.plainenglish.io/how-to-send-aws-notifications-to-microsoft-teams-2f4df243543f>
* <https://www.gorillastack.com/blog/real-time-events/cloudtrail-event-names/>
* <https://cybersecurity.att.com/documentation/usm-anywhere/user-guide/events/cloudtrail-events-rules.htm>
* <https://www.intelligentdiscovery.io/tools/cloudtrailevents>

