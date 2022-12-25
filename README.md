# **키슈 (Kiosk is you)**
배리어프리 키오스크 프로그램


## **Install requirements**

```bash
pip install -r requirements.txt
```


## **SSLServer 설정 및 구동**  


- **Key 파일 생성**

```bash
openssl genrsa 1024 > django.key
```

- **CRT 파일 생성**

```bash
openssl req -new -x509 -nodes -sha256 -days 365 -key django.key > django.crt
```

- **runsslserver**  

```bash
python manange.py runsslserver 0.0.0.0:80 --certificate django.crt --key django.key
```

