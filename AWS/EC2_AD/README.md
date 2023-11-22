# Alta Disponibilidade

![image](https://github.com/Guto-Haziro/Projects/assets/118192092/07be5e8e-ce78-4d5f-a1a1-6b067a7a2369)


# Implementação de Instancia com Alta Disponibilidade


# Instancia com RDS e S3 

# Passo-a-passo 

## IAM 

1. Criar uma função (IAM) 

2. Alterar grupo de segurança deixar aberto para qualquer trafego. (para facilitar no bootcamp) (EC2) 

  

## EC2 

1. Criar instancia. (EC2): 
* Ubuntu 20.04 LTS 
* t2.micro 
* Criar par de chaves 
* Adicionar subrede equivalente a que esta usando 
* Selecionar o grupo de segurança criado anteriormente 
* Config. de armazenamento padrão 

### Em detalhes avançados: 
* Adicionar o perfil de instancia IAM criado anteriormente 
* Adicionar dados do usuário (Cod. enviado) 

> 

'#!/bin/bash'

sudo apt-get update -y 

sudo apt-get install apache2 php7.4 libapache2-mod-php7.4 php7.4-common php7.4-curl php7.4-intl php7.4-mbstring php7.4-json php7.4-xmlrpc php7.4-soap php7.4-mysql php7.4-gd php7.4-xml php7.4-cli php7.4-zip wget mysql-client unzip git binutils ruby -y 

sudo systemctl start apache2 

sudo systemctl enable apache2 

sudo systemctl restart apache2 

wget https://aws-codedeploy-us-east-1.s3.us-east-1.amazonaws.com/latest/install 

chmod +x ./install 

sudo ./install auto 

sudo service codedeploy-agent start 

sudo chmod 777 /etc/init.d/codedeploy-agent 

sudo wget https://s3.sa-east-1.amazonaws.com/pages.cloudtreinamentos.com/aws/bootcamp/Bootcamp9.zip  

sudo unzip -o Bootcamp9.zip -d /var/www/html/ 

sudo rm /var/www/html/index.html 

sudo chmod -R 777 /var/www/html 

  

2. Executar a instancia e após subir, acessar o IP publico  

 

## RDS 
1. Criar Banco de dados padrão 
* MySQL 8.0.32 
* Nivel gratuito 
* Acesso Admin 
* Senha: senha 
* Db.t2.micro 
* 20gb 

2. Criar o banco 

3. Adicionar as informações na aplicação 

  

## S3 

1. Criar um bucket para armazenar imagens no site. 
* Us-east-1 
* ACLs habilitada 
* Desbloquear todo acesso ao publico 
* Reconhecer as configurações 
* Ativar versionamento 

2. Configurações de segurança 
* Habilitar hospedagem de site estático 
* Alterar Permissões em política de Bucket (ir em "Gerador de política") 
* Gerar a seguinte política: 


3. Adicionar um usuário no IAM para dar acesso a aplicação no S3 
* Dar um nome 
* Anexar política "AmazonS3FullAccess" 
* Criar o usuário 
* Editar as credenciais de segurança 
* Criar chave de acesso "Aplicação em execução em um serviço computacional da AWS" 

4. Adicionar as informações no site

5. Após isso, será possível subir imagens dentro da aplicação e serão armazenadas no bucket criado 


# AMI, LoadBalancer, AutoScalling 

## Alta Disponibilidade 

### Criando imagem EC2 

1. Vamos criar uma imagem da instancia para que possamos deixar registrado a aplicação, para isso siga as opções: 


2. Dê um nome a imagem. 
* Após criar, veja a imagem criada em "AMIs"  
          

### Criando nova instancia com a nova AMI 

1. Execute uma nova instancia EC2 
* Com o mesmo nome 
* Em AMIs, selecione a AMI criada em " Minhas AMIs" 
* T2.micro 
* Defina a chave de segurança 
* Grupo de segurança default (única VPC criada) 
* Editar configurações de rede e escolher uma subnet em outra região 
* Em detalhes avançados, definir o perfil de instancia IAM 

 
Com essa instancia criada com essa AMI, teremos duas maquinas em regiões diferentes funcionando simultaneamente, causando a alta disponibilidade. Porém as duas instancias apresentam dois IPs diferentes, sendo assim, caso uma instancia pare de funcionar, teríamos que acessar o IP da outra. Podemos fazer uma distribuição automática com o serviço Load Balacer. 


### Criando Load Balancer 

1. Crie um Grupo de Destino 
* Crie um nome 
* Registre o destino das Duas instâncias criadas 

2. Crie um load balnacer  
* Crie um "Application load balancer" 
* Crie um nome 
* Selecione todas as zonas de disponibilidade 
* O grupo de segurança default 
* Em Listeners e roteamento, selecione o GrupoWeb criado 

 

3. Acesse o IP gerado do load balancer no navegador, e teremos o acesso a aplicação, e a cada reload feito na página, ele alterna entre as regiões. 

 

 

### Alterando a Aplicação 

1. em Funções no IAM 


2. Criar nova Função 
* Serviço AWS 
* Caso de uso: CodeDeploy > CodeDeploy 
* Dar um nome para a função e criar 

 
3. Criar mais um Bucket S3 
* Apenas ativar o versionamento 

 
4. Será enviado a nova versão da aplicação para ser colocado dentro deste Bucket 


5. Criar um Deploy automatizado (CodeDeploy) 
* Ir para CodeDeploy > Aplicativo > Criar aplicativo 
* Dê um nome e crie 

 
6. Criar um Grupo de implantação 
* De um nome 
* Selecione o Deploy criado 
* LocalSelecione a Chave=Name e Valor=web 
* Desabilite o Load Balancer 


7. Criar Implantação 
* Crie o nome 
* Revisão no S3 criado 
* Local da revisão, pegar o local do bucket que está a versão da aplicação: 
* Configurações de conteúdo > substituir o conteúdo 

 

Com isso será rodado o deploy e a aplicação terá atualizado: 

 

8. Criar Pipeline (CodePipeline) 
* Origem Amazon S3 
* Bucket Repo 
* Chave webapp.zip 
* Ignorar compilação 
* Implantação Codeploy 
* Aplicativo AppWeb 
* Grupo de implantação Grupo AppWeb 

 

9. Após criada a Pipeline, atualize a aplicação e suba no bucket, assim o pipeline ira rodar automaticamente, atualizando a aplicação: 

 
### Auto Scalling 

1. Ir em Criar configuração de execução em Auto Scalling (EC2) 
* De o nome 
* Escolha a AMI da aplicação criada 
* Instancias t2.micro 
* Perfil do IAM criado para o projeto 
* Selecionar o grupo de segurança criado para a aplicação 
* Selecionar o par de chaves criado para a aplicação 

 

2. Criar Grupo de Auto Scalling (EC2) 
* De o nome 
* Selecionar o grupo de execução criado anteriormente 
* Selecionar VPC 
* Selecionar todas as zonas de disponibilidade 
* Selecione "Anexar a um balanceador de carga existente" 
* Selecione o grupo de destino criado para a aplicação 
* Habilite a coleta de métricas 
* Selecione as capacidades de escalonamento 
* Crie um tag 


3. Configurar no CodeDeploy 
* Ir em Aplicativos 
* Editar o aplicativo que foi criado para a aplicação 
* Mudar de "Instâncias do Amazon EC2" para ''Grupos de Auto Scaling do Amazon EC2'' 
 

4. Para testar, exclua as instâncias criadas anteriormente

 
5. Criar métricas para escalonamento no Auto Scalling 
* Selecionar o grupo de Auto Scalling criado 
* Ir em escalabilidade automática 
* Criar escalabilidade dinâmica 

 
6. Subir o CPU da aplicação para testar o escalonamento. 
 

7. Após a instancia inicializar, abaixar o CPU para verificar se a mesma será excluída. 
  
