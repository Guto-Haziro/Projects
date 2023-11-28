# Centralização de logs em uma conta LogArchive

Esta solução visa otimizar os custos de armazenamento fazendo um backup dos logs armazenados no seu loggroup, utilizando os serviços:
* Kinesis
* Lambda
* S3
* Cloudwatch
  
![image](https://github.com/Guto-Haziro/Projects/assets/118192092/b51e5801-3739-464b-b502-30b8b6958f2c)

## Passo-a-Passo

Para essa solução já há dois templates de Cloudformation que criarão os recursos nas Accounts distintas. Na qual será necessário apenas o apontamento dos S3 criados para o armazenamento dos logs.

A configuração é simples. Existe apenas um modelo CloudFormation e os parâmetros padrão devem ser bons para a maioria.

1. Baixe o modelo CloudFormation
2. Abra o console AWS
3. Vá para a página CloudFormation
4. Clique em “ Criar pilha ”
5. Em “Especificar modelo”, escolha “Carregar um arquivo de modelo”, escolha o arquivo baixado na etapa 1 e clique em “Avançar”
6. Em “Nome da pilha” escolha um nome como “CloudWatch2S3”
7. Se você tiver um grande volume de logs, considere aumentar a contagem de fragmentos do Kinesis
8. Revise outros parâmetros e clique em “Avançar”
9. Adicione tags se necessário e clique em “Avançar”
10. Marque “Reconheço que o AWS CloudFormation pode criar recursos IAM” e clique em “Criar pilha”
11. Espere a pilha terminar
12. Vá para a aba “Saídas” e observe o bucket onde os logs serão gravados
É isso!


Outro recurso é a capacidade de exportar logs de várias contas para o mesmo bucket. Para configurar isso, você precisa definir o parâmetro AllowedAccounts como uma lista separada por vírgulas de identificadores de contas da AWS com permissão para exportar logs. Depois de criar a pilha, vá até a aba “Saídas” e copie o valor de LogDestination. Em seguida, implante CloudWatch2S3-additional-account.template nas outras contas enquanto configura LogDestination com o valor copiado anteriormente.

Para solução de problemas e mais detalhes técnicos, consulte [Como exportar todos os logs do CloudWatch de várias contas para um único bucket S3 ](https://github.com/CloudSnorkel/CloudWatch2S3/blob/master/README.md)https://github.com/CloudSnorkel/CloudWatch2S3/blob/master/README.md.


