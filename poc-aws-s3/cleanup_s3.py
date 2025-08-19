#!/usr/bin/env python3
"""
Cleanup – remove objetos e o bucket S3 criado no POC.

Uso:
  python cleanup_s3.py --bucket <nome-do-bucket> [--region <regiao>]
"""
import argparse, sys
import boto3
from botocore.exceptions import ClientError

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--bucket', required=True)
    parser.add_argument('--region', default=None)
    args = parser.parse_args()

    session = boto3.Session(region_name=args.region)
    s3 = session.resource('s3')
    bucket = s3.Bucket(args.bucket)

    # Remove todos os objetos e versões (se versionado)
    try:
        bucket.object_versions.delete()
    except Exception:
        # Se não houver versionamento, tenta apagar objetos simples
        bucket.objects.delete()

    try:
        bucket.delete()
        print(f"[OK] Bucket removido: {args.bucket}")
    except ClientError as e:
        print(f"[AWS ERROR] {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
