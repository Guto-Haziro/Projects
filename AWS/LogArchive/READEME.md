# Centralização de logs em uma conta LogArchive

Esta solução visa otimizar os custos de armazenamento fazendo um backup dos logs armazenados no seu loggroup, utilizando os serviços:
* Kinesis
* Lambda
* S3
* Cloudwatch
* 
![image](https://github.com/Guto-Haziro/Projects/assets/118192092/b51e5801-3739-464b-b502-30b8b6958f2c)


Para essa solução já há dois templates de Cloudformation que criarão os recursos nas Accounts distintas. Na qual seránecessário apenas o apontamento dos S3 criados para o armazenamento dos logs.
