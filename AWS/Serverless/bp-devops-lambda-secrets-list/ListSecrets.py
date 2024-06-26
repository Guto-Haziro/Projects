import boto3
from prettytable import PrettyTable
from datetime import datetime

def list_secrets_in_all_regions():
    # Obtenha a lista de todas as regiões disponíveis
    ec2_regions = [region['RegionName'] for region in boto3.client('ec2').describe_regions()['Regions']]

    # Crie uma tabela para exibir os resultados
    table = PrettyTable()
    table.field_names = ["Region", "Secret Name", "Last Retrieved (UTC)", "Created On (UTC)"]

    # Itere sobre todas as regiões
    for region_name in ec2_regions:
        # Crie um cliente do AWS Secrets Manager para a região atual
        client = boto3.client('secretsmanager', region_name=region_name)

        # Crie um paginator para lidar com várias páginas de resultados
        paginator = client.get_paginator('list_secrets')
        response_iterator = paginator.paginate()

        # Itere sobre as páginas de resultados
        for page in response_iterator:
            for secret in page['SecretList']:
                secret_name = secret['Name']

                # Obtenha informações detalhadas da secret
                secret_metadata = client.describe_secret(SecretId=secret_name)

                # Converta timestamps para formato legível
                last_retrieved = secret_metadata['LastAccessedDate'].strftime("%Y-%m-%d %H:%M:%S") if 'LastAccessedDate' in secret_metadata else "N/A"
                created_on = secret_metadata['CreatedDate'].strftime("%Y-%m-%d %H:%M:%S")

                # Adicione uma linha à tabela
                table.add_row([region_name, secret_name, last_retrieved, created_on])

    # Imprima a tabela ordenada primeiro por região e depois pelo nome da secret
    print(table.get_string(sortby=["Region", "Secret Name"]))

if __name__ == "__main__":
    list_secrets_in_all_regions()