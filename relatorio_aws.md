# RELATÓRIO DE IMPLEMENTAÇÃO DE SERVIÇOS AWS

**Data:** 19/08/2025  
**Empresa:** Abstergo Farmacêutica  
**Responsável:** Enaile Lopes

## Introdução
Este relatório apresenta o processo de implementação de ferramentas na empresa *Abstergo Farmacêutica*, realizado por Enaile Lopes.  
O objetivo do projeto foi elencar **3 serviços AWS** com a finalidade de realizar **redução imediata de custos** e aumento da eficiência.  

## Descrição do Projeto
O projeto de implementação de ferramentas foi dividido em **3 etapas**, cada uma com seus objetivos específicos:

### Etapa 1: 
- **Amazon RDS**
- **Foco:** Reduzir custos de manutenção de banco de dados local.  
- **Caso de uso:** Migração do banco de dados on-premise para o Amazon RDS, garantindo escalabilidade, backup automático e alta disponibilidade.  

### Etapa 2: 
- **Amazon S3**
- **Foco:** Armazenamento econômico e seguro.  
- **Caso de uso:** Utilização do Amazon S3 para armazenar relatórios, documentos e dados históricos da farmácia, reduzindo custos com servidores locais.  

### Etapa 3: 
- **AWS Lambda**
- **Foco:** Automação sem servidor (Serverless).  
- **Caso de uso:** Implementação de funções para processar dados de vendas e relatórios de estoque automaticamente, sem necessidade de servidores dedicados.  

## Estimativa de Custos (AWS Pricing Calculator)

| Serviço      | Uso estimado | Custo aproximado/mês | Comparativo On-Premise |
|--------------|-------------|-----------------------|------------------------|
| Amazon RDS   | 1 instância db.t3.micro, 20 GB storage | **US$ 20** | >US$ 200/mês (infra local + licenciamento) |
| Amazon S3    | 100 GB armazenados, acesso moderado | **US$ 2** | ~US$ 50/mês (discos locais + backup) |
| AWS Lambda   | 1M execuções/mês, 128MB, <1s | **US$ 0** (free tier) | ~US$ 100/mês (infra e manutenção scripts) |

**Total estimado na AWS:** ~ **US$ 22/mês**  
**Custo aproximado On-Premise:** ~ **US$ 350/mês**  

➡️ **Economia estimada:** ~ **US$ 328/mês** (~R$ 1.600)  


## Conclusão
A implementação de ferramentas na empresa *Abstergo Industries* trará como resultado:  
- **Redução significativa de custos** com infraestrutura local.  
- **Maior escalabilidade e disponibilidade dos serviços.**  
- **Automação de processos críticos.**  

Recomenda-se a continuidade do uso das ferramentas implementadas e a busca por novas tecnologias AWS que possam otimizar ainda mais os processos internos.  


## Anexos
- Scripts de configuração utilizados (POC em Python – S3 + Lifecycle)  

**Assinatura do Responsável pelo Projeto:**  
Enaile Lopes
