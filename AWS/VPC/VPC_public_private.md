# Virtual Private Cloud 

* Gerar VPC  
* Criar Sub-Rede pub e priv 
* Criar EC2 para teste de conexão 
* Copiar credencias e conectar via ubuntu 
* Criar Internet Gateway 
* Criar Route Table pub e priv 
* Criar NAT Gateway 
* Para ter alta disponibilidade deve-se criar duas sub-redes, uma pública e uma privada. 


## VPC 

1. Crie uma VPC 
 * Somente VPC 
 * CIDR Block (Class Inter Domain Route) : 10.0.0.0/16 
 * Nenhum CIDR IPv6 
 * Locação padrão 

2. Crie a sub-rede publica 
 * Selecione a VPC criada 
 * Zona de disponibilidade que está usando 
 * CIDR Block (Class Inter Domain Route) : 10.0.0.0/24 

 

3. Crie a sub-rede privada 
* Selecione a VPC criada 
* Zona de disponibilidade que está usando 
* CIDR Block (Class Inter Domain Route) : 10.0.1.0/24 


CIDR Block (Class Inter Domain Route) : 
https://jodies.de/ipcalc?host=10.0.0.0&mask1=16&mask2 

Quanto menos bits definido na máscara, menor será o número de sub-redes e consequentemente, maior o número de IPs(Maquinas) disponíveis para alocar na rede. 

 ![unnamed](https://github.com/MAGAMEN/documentosAWS/assets/39193235/0c4da5e5-3d12-4fdf-be3b-a611dabafc38)

## EC2 

1. Crie uma instancia publica 

* Ubuntu 22.04 
* T2.micro 
* Crie ou anexe o par de chaves 
* Edite as configurações de rede 
* Adicione a VPC criada 
* Sub-rede publica 
* Habilitar IP publico 
* Crie ou selecione o grupo de segurança (Em caso de teste deixe as portas abertas para qualquer conexão) 

 

2. Crie uma instancia privada 

* Ubuntu 22.04 
* T2.micro 
* Crie ou anexe o par de chaves 
* Edite as configurações de rede 
* Adicione a VPC criada 
* Sub-rede privada 
* Desabilitar IP publico 
* Crie ou selecione o grupo de segurança (Em caso de teste deixe as portas abertas para qualquer conexão) 

 

3. Copie a chave.pem em .ssh para poder acessar as instancias externamente: 
* cp /mnt/c/Users/TBS/Downloads/pub.pem ~/.ssh/aws.pem (para copiar) 
* ls ~/.ssh/ (para listar) 
* chmod 400 ~/.ssh/aws.pem (para restringir permissões) 

 ![unnamed (1)](https://github.com/MAGAMEN/documentosAWS/assets/39193235/c11a0693-8fe9-4de3-b3bd-75f145f0bf5a)

## Internet Gateway 

Será necessário a criação do Internet Gateway para que a instancia tenha acesso a internet. E com a VPC essa conexão será de forma mais assertiva e segura. 

1. Criar internet gateway 
2. Associar a VPC 

 

## Route Table 

O Route Table será necessário para apontar a rota do Internet Gateway na instancia. 

1. Criar Route Table Publico 
* Adicione a VPC 
* Após criação, associe a sub-rede publica 
* Adicione a rota 0.0.0.0/0 - Internet Gateway 

 

2. Teste a conexão no IP da EC2 publica  
* ssh ubuntu@(IP público da máquina) -i ~/.ssh/aws.pem 

 

3. Copie a chave pem dentro da instancia para acesso a máquina privada 
* scp -i ~/.ssh/aws.pem /home/augustohaziro/.ssh/aws.pem ubuntu@75.101.206.130:/home/ubuntu/.ssh/aws.pem 

 

4. Acesse a máquina privada dentro da máquina publica 
* ssh ubuntu@(IP da máquina) -i ~/.ssh/aws.pem 

 

## NAT Gateways 

1.  Criar NAT Gateway 
* Associar a sub-rede publica 
* Conectividade publica 
* Gerar/Associar IP elástico 

 

2. Criar uma route table privada 

* Adicionar VPC 
* Associar a sub-rede privada 
* Adicionar a rota  0.0.0.0/0 - NAT gateway 
