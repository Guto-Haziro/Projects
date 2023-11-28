# Objetivo
Alterar retenção de loggroups HML/DEV através de uma automatização via Python.

Passo-a-Passo
* Gerar um comando para listar os loggroups HML/DEV
* Baixar as extenções necessárias Python, BOTO3, AWS CLI
* Gerar código de alteração

## Listar loggroups
### Code
~~~comandline
$ aws logs describe-log-groups --query "logGroups[?contains(logGroupName,'hml') || contains(logGroupName,'HML') || contains(logGroupName,'dev') || contains(logGroupName,'DEV') && retentionInDays != \`1\`].[logGroupName,to_string(retentionInDays || 'Never')]" --output=table
~~~

Com esse comando apontamos os carecteres HML/DEV que estão acrescentados nos loggroups em tabela.


## Baixar extensão 
Instale o awscli usando a documentação oficial:
https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html

Instale o python na maquina ou vscode:
https://www.python.org/downloads/
![image](https://github.com/Guto-Haziro/Projects/assets/118192092/c46f147a-917e-4a53-8168-a0046b40112e)


Instale o BOTO3 para integração com as configurações da AWS:
~~~comandline:
pip install boto3
~~~

## Gerar o código de alteração:
### Code
~~~ python
##Retention modify
import re
import boto3

client = boto3.client('logs', region_name='sa-east-1', aws_access_key_id='Key', aws_secret_access_key='secret', aws_session_token='token')

newlist = []

response = client.describe_log_groups()

for logs in response['logGroups']:
    log_group_name = logs['logGroupName']
    if re.search('dev', log_group_name.lower()) or re.search('hml', log_group_name.lower()):
        if not re.search(r'devops|development', log_group_name.lower()):
            newlist.append(log_group_name)

while 'nextToken' in response:
    response = client.describe_log_groups(nextToken=response['nextToken'])
    for logs in response['logGroups']:
        log_group_name = logs['logGroupName']
        if re.search('dev', log_group_name.lower()) or re.search('hml', log_group_name.lower()):
            if not re.search(r'devops|development', log_group_name.lower()):
                newlist.append(log_group_name)

print(newlist)

for i in newlist:
 log=client.put_retention_policy(
     logGroupName=i,
     retentionInDays=1
 )
print(newlist)
~~~
Com isso a retenção dos loggroups mencionados é alterada conforme o valor em 'retentionInDays':
![image](https://github.com/Guto-Haziro/Projects/assets/118192092/18e2a71c-51e4-4e7a-a7e7-2e9cf25aca4b)


