#!/usr/bin/env python3
"""
AWS POC – S3 para Redução de Custos
-----------------------------------
O que este script faz:
1) Cria (ou reutiliza) um bucket S3.
2) Ativa bloqueio de acesso público (boa prática).
3) Configura Lifecycle para reduzir custos:
   - Após 30 dias: STANDARD_IA
   - Após 90 dias: GLACIER_IR (Glacier Instant Retrieval)
4) Faz upload de um arquivo de exemplo (sample/report.txt).
5) Lista objetos e exibe a lifecycle rule aplicada.

Pré-requisitos:
- Python 3.10+
- boto3 instalado:  pip install -r requirements.txt
- Credenciais AWS configuradas (aws configure) ou via variáveis de ambiente:
  AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION

Uso:
  python aws_poc_s3.py --bucket <nome-do-bucket> [--region <regiao>]
Exemplo:
  python aws_poc_s3.py --bucket minha-farmacia-abstergo --region us-east-1
"""

import argparse
import sys
import json
from pathlib import Path
import boto3
from botocore.exceptions import ClientError

def ensure_bucket(s3_client, bucket_name: str, region: str):
    # Verifica se o bucket existe
    try:
        s3_client.head_bucket(Bucket=bucket_name)
        print(f"[OK] Bucket já existe: {bucket_name}")
        return
    except ClientError as e:
        if e.response.get('Error', {}).get('Code') in ('404', 'NoSuchBucket', 'NotFound'):
            pass
        else:
            print(f"[INFO] head_bucket: {e}")
    # Cria o bucket
    params = {'Bucket': bucket_name}
    if region and region != 'us-east-1':
        params['CreateBucketConfiguration'] = {'LocationConstraint': region}
    s3_client.create_bucket(**params)
    print(f"[OK] Bucket criado: {bucket_name} ({region})")

def block_public_access(s3_control, account_id: str, bucket_name: str):
    # Bloqueia acesso público (boa prática para dados internos)
    s3_control.put_public_access_block(
        PublicAccessBlockConfiguration={
            'BlockPublicAcls': True,
            'IgnorePublicAcls': True,
            'BlockPublicPolicy': True,
            'RestrictPublicBuckets': True
        },
        AccountId=account_id,
        Bucket=bucket_name
    )
    print("[OK] Public Access Block configurado para o bucket.")

def put_lifecycle(s3_client, bucket_name: str):
    # Regra de lifecycle para otimização de custos
    rules = {
        'Rules': [
            {
                'ID': 'cost-optimization-rule',
                'Filter': {'Prefix': ''},
                'Status': 'Enabled',
                'Transitions': [
                    {'Days': 30, 'StorageClass': 'STANDARD_IA'},
                    {'Days': 90, 'StorageClass': 'GLACIER_IR'}
                ],
                'NoncurrentVersionTransitions': [
                    {'NoncurrentDays': 30, 'StorageClass': 'STANDARD_IA'},
                    {'NoncurrentDays': 90, 'StorageClass': 'GLACIER_IR'}
                ],
                'AbortIncompleteMultipartUpload': {'DaysAfterInitiation': 7}
            }
        ]
    }
    s3_client.put_bucket_lifecycle_configuration(
        Bucket=bucket_name,
        LifecycleConfiguration=rules
    )
    print("[OK] Lifecycle configurado (30d IA, 90d Glacier IR, abort 7d).")

def upload_example(s3_client, bucket_name: str, path: Path):
    key = f"reports/{path.name}"
    s3_client.upload_file(str(path), bucket_name, key)
    print(f"[OK] Upload: s3://{bucket_name}/{key}")
    return key

def list_objects(s3_client, bucket_name: str, prefix: str = ''):
    resp = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    print("[INFO] Objetos no bucket:")
    for item in resp.get('Contents', []):
        print(f" - {item['Key']} ({item['Size']} bytes)")

def get_account_id(sts):
    return sts.get_caller_identity()['Account']

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--bucket', required=True, help='Nome do bucket S3')
    parser.add_argument('--region', default=None, help='Região (ex.: us-east-1)')
    parser.add_argument('--file', default='sample/report.txt', help='Arquivo local para upload')
    args = parser.parse_args()

    session = boto3.Session(region_name=args.region)
    s3_client = session.client('s3')
    sts = session.client('sts')
    s3_control = session.client('s3control')

    account_id = get_account_id(sts)
    region = session.region_name or 'us-east-1'

    ensure_bucket(s3_client, args.bucket, region)
    block_public_access(s3_control, account_id, args.bucket)
    put_lifecycle(s3_client, args.bucket)

    # Upload arquivo de exemplo
    path = Path(args.file)
    if not path.exists():
        print(f"[ERRO] Arquivo não encontrado: {path}", file=sys.stderr)
        sys.exit(2)
    upload_example(s3_client, args.bucket, path)

    # Lista objetos e imprime lifecycle atual
    list_objects(s3_client, args.bucket, prefix='reports/')
    lc = s3_client.get_bucket_lifecycle_configuration(Bucket=args.bucket)
    print("[INFO] Lifecycle atual:")
    print(json.dumps(lc, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    try:
        main()
    except ClientError as e:
        print(f"[AWS ERROR] {e}", file=sys.stderr)
        sys.exit(1)
