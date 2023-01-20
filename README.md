<br>

# 📌 키슈(Kiosk IS YOU) : 모두를 위한 키오스크
> 2022.11.28 ~ 2023.01.05 KT AIVLE 충남/충북 15조 빅프로젝트<br>
>  *'키슈(Kiosk IS YOU)'는 키오스크에 익숙치 않은 노년층이나 장애가 있어 사용에 어려움을 겪는 사람 등을 위해 개발되었습니다.
고령층을 위한 간단 UI, 장애인용 모바일 어플리케이션을 통해 모든 사람이 이용할 수 있는 키오스크 서비스입니다.
또한 인공지능 모델을 통해 사용자의 연령대를 추측하여 그에 따른 추천 메뉴를 제공하는 등 다양한 기능을 구현하였습니다.*
<img src="https://user-images.githubusercontent.com/68288862/210302860-bebdfbc4-a493-4a37-9281-f7ce4697ff10.png" width="600" height="600">

# 로고
![image](https://user-images.githubusercontent.com/68462676/210313547-fd45db49-9596-4f88-b4a5-21fe213eec12.png)

## 조원 소개
- `AI충남/충북1반 2조[15조]`
> 최재혁(조장), 김수빈, 김유민, 이시영, 이지호, 조진호, 황재윤


## 목차
1. 개발 배경 및 목적

2. 기능 및 UI/UX

3. 서비스 FLOW

4. Service Architecture

5. DB 설계

6. 개발 환경

7. 설정 및 구동

***

## 1. 개발 배경 및 목적
> 🍀 **'키오스크로부터 소외당하는 구성원이 없는 사회를 위하여'**\
우리는 패스트푸드점, 은행 등 각종 서비스 업체를 중심으로 무인 주문 시스템인 '키오스크(Kiosk)'를 자주 접할 수 있다. 키오스크가 어떤 이들에게는 편리와 경제적 이익을 가져다주지만, 또 다른 사람들에게는 쓸모 없는 고철 덩어리에 불과할지도 모른다.
높은 연령대 고객의 경우 키오스크의 **복잡한 UI**로 인해 사용에 어려움을 겪고 있다는 사실이 각종 매체를 통해 끊임없이 보도된다. 또한 **시각장애인** 고객은 키오스크의 UI를 인식할 수 없으며, **휠체어**를 탄 고객도 높낮이 조절이 안되어 터치 주문이 어렵다는 문제점도 꾸준히 제기되고 있다.\
따라서 본 프로젝트는 이러한 문제점들을 인식하고 다양한 특성을 가진 고객들이 주문을 원활히 할 수 있는 키오스크 서비스를 개발하는 것에 목적을 둔다.

<br>
<br>

- `나이가 많아도 👵👴`
    - AI 모델이 사용자의 안면 인식을 통한 연령대 추측 수행
    - 40대 이상일 경우 **간편 UI**로 화면 전환
 
<br>
<br>

- `장애가 있어도 👨‍🦽👩‍🦯`
  - 장애인용 모바일 어플리케이션 제작
  - 시각 장애인: 스마트폰 내 **스크린리더** 기능을 활용해 청각적 요소 추가
  - 휠체어 이용자: 키오스크의 높이와 관계 없이 스마트폰을 이용해 주문 가능

<br>
<br>

- `점주를 위해서도 🙏`
    - **장애인차별금지법 개정안**: 공공기관은 1년 이내 민간 기관은 최대 2년 이내에 **배리어프리 키오스크**를 의무적 도입
    - 하지만 배리어프리 키오스크의 가격은 일반 제품의 6~7배이므로 소상공인 점주의 부담이 증가
    - 기기 교체 없이 기존 키오스크의 문제점을 해결하기 위한 소프트웨어를 제작

<br>
<br>

## 2-1. 키오스크🖥: 기능 및 UI/UX

<details>
<summary> 서비스 주요 기능 보기 🍽 </summary>

#### 📌 홈 화면
![image](https://user-images.githubusercontent.com/68462676/210805079-e8fc7a0c-e4f1-4eb3-ab7f-f450688882be.png)
<br>
<br>

#### 📌 연령대 추측
![image](https://user-images.githubusercontent.com/68462676/210909402-f577d780-ce70-4f16-ba25-09160eb66b92.png)

  - 인공지능 모델을 통해 사용자의 연령대를 추측 
<br>
<br>

#### 📌 추천 메뉴 화면
<table>
  <tr>
    <td><img alt="" src="https://user-images.githubusercontent.com/68462676/210818356-4fd83fb0-f725-417d-a044-7fce08732f7c.png" /></td><td><img alt="" src="https://user-images.githubusercontent.com/68462676/210909290-1408d30d-ae7f-4738-b4e9-b59f3579f9e4.png" /></td>
  <tr>
</table>

  - 앞에서 예측한 **연령대에 따른 추천 메뉴** 탭
  
<br>
<br>


#### 📌 일반 메뉴 UI
<table>
  <tr>
    <td><img alt="" src="https://user-images.githubusercontent.com/68462676/210818356-4fd83fb0-f725-417d-a044-7fce08732f7c.png" /></td><td><img alt="" src="https://user-images.githubusercontent.com/68462676/210910718-50f201e3-41ec-4ec2-b3ab-7e26259f9b45.png" /></td><td><img alt="" src="https://user-images.githubusercontent.com/68462676/210910363-9affce6f-c705-43e7-af68-be78d5ec9512.png" /></td>
  <tr>
</table>

<br>
<br>

#### 📌 고령자를 위한 간편 UI
<table>
  <tr>
    <td><img alt="" src="https://user-images.githubusercontent.com/68462676/210805534-a14822ca-f5a0-48cd-b8e3-e3ba58ef87ad.png" /></td><td><img alt="" src="https://user-images.githubusercontent.com/68462676/210909765-4877968f-ee86-4863-95aa-6fcb5e63eead.png" /></td><td><img alt="" src="https://user-images.githubusercontent.com/68462676/210909802-09da7ab6-1e97-440f-8f07-99dcaa3aa5e5.png" /></td>
  <tr>
</table>

<br>
<br>

#### 📌 주문 내역 확인 페이지
![image](https://user-images.githubusercontent.com/68462676/210911221-13bfe49a-44d6-457f-b55a-e14e97f65a83.png)

#### 📌 신용카드 결제중
![image](https://user-images.githubusercontent.com/68462676/210911255-11c1b7ee-42a9-4cc5-a152-c615354b6e01.png)

#### 📌 주문 완료 페이지
![image](https://user-images.githubusercontent.com/68462676/210806573-a5ff32d1-f888-41e2-b572-44c51d4e75d7.png)

<br>
<br>
</details>

## 2-2. 장애인 전용 어플📱: 기능 및 UI/UX
<details>
<summary> 서비스 주요 기능 보기 😎 </summary>

#### 📌 홈 화면
![image](https://user-images.githubusercontent.com/68288862/210070370-0e0e75c4-081c-41d2-b641-e50c3dbb66e1.png)
<br>
<br>

#### 📌 연령대 추측
![image](https://user-images.githubusercontent.com/68288862/210199856-1577acfc-1b65-4043-bf03-6c92336c0187.png)

  - 인공지능 모델을 통해 사용자의 연령대를 추측 
<br>
<br>

#### 📌 메뉴 화면
<table>
  <tr>
    <td><img alt="" src="https://user-images.githubusercontent.com/68288862/210200283-edecca72-1054-4b80-ad8c-f2fcd77f310e.png" /></td><td><img alt="" src="https://user-images.githubusercontent.com/68288862/210200812-a5f3f2ca-9c0a-4f9a-ad95-54ceb262488c.png" /></td><td><img alt="" src="https://user-images.githubusercontent.com/68288862/210200908-dac32fb7-7e63-4c96-9abb-87af5ef7421a.png" /></td>
  <tr>
</table>

  - 앞에서 예측한 **연령대에 따른 추천 메뉴** 탭

<br>
<br>

#### 📌 메뉴 상세 화면 
<table>
  <tr>
    <td><img alt="" src="https://user-images.githubusercontent.com/68288862/210203044-b388eb84-f3cc-443a-a812-73fd0c8e5985.png" /></td><td><img alt="" src="https://user-images.githubusercontent.com/68288862/210203443-eeabeff1-d3e8-49f5-865d-2b962b670e29.png" /></td>
  <tr>
</table>

<br>
<br>


#### 📌 장바구니
<table>
  <tr>
    <td><img alt="" src="https://user-images.githubusercontent.com/68288862/210203178-eda2fe4a-6689-4e8c-ae54-1b2f2554e3f2.png" /></td><td><img alt="" src="https://user-images.githubusercontent.com/68288862/210203469-ad7e0cec-e930-4332-b26f-80680f6d331f.png" /></td>
  <tr>
</table>

  - 좌: 장바구니에 아무것도 없을 때 
  - 우: 장바구니에 메뉴를 담은 모습

<br>
<br>

#### 📌 결제 화면

![image](https://user-images.githubusercontent.com/68288862/210203705-7d9cd8e1-8349-44bd-801d-d57b92894acc.png)

  - 결제 API 사용해 여러 결제 수단 구현

#### 📌 결제 완료!
![image](https://user-images.githubusercontent.com/68462676/210907925-8bc43f5c-a22f-4550-9bf0-7f41ba7bb8cd.png)

</details>

<br>


## 3. 서비스 FLOW
  - `주요 기능 Flow`
  
  ![image](https://user-images.githubusercontent.com/68462676/210824324-b17231ae-f53d-43c2-a96c-4428c72a302f.png)
<br>

## 4. Service Architecture
 
 ![아키텍쳐](https://drive.google.com/uc?id=19eIfhFXB7WlEDym1mnbYTzNw-Gu9jcVn)
<br>

## 5. DB 설계
  - `ERD`
![Kiosk Is U ERD](https://drive.google.com/uc?id=19wp7yki7WcyHFpJXGmRFD0rnGRUygxec)

<br>

## 6. 개발 환경

- `Front-End`

  |HTML|CSS|JS|Bootstrap|
  |:---:|:---:|:---:|:---:|
  |![html](https://user-images.githubusercontent.com/68097036/151471705-99458ff8-186c-435b-ac5c-f348fd836e40.png)|![css](https://user-images.githubusercontent.com/68097036/151471805-14e89a94-59e8-468f-8192-c10746b93896.png)|![js](https://user-images.githubusercontent.com/68097036/151471854-e0134a79-b7ef-4a0f-99fd-53e8ee5baf50.png)|![bootstrap](https://user-images.githubusercontent.com/68097036/151480381-2b23a8af-c6b4-43a6-96a6-ea69e0b953e0.png)|


- `Back-End and Cloud`

  |Python|Django|SQLite|
  |:---:|:---:|:---:|
  |![pngwing com](https://user-images.githubusercontent.com/68097036/151479684-a85d26d4-e79e-47c9-9023-bf6d92f57536.png)|![pngwing com (1)](https://user-images.githubusercontent.com/68097036/151466729-9cad0405-85ad-454e-815a-1a4fd065f8b7.png)|<img src="https://drive.google.com/uc?id=1ESaa-EooyQ5TJg26BRG0FZUNl3IedkOo" width="140" height="100">|
- `Application`

  |Flutter|Dart|Firebase|
  |:---:|:---:|:---:|
  |<img src="https://drive.google.com/uc?id=18mVvE6-_EuX5OugcAwPYkARZ3fBymDXh" width="100" height="90">|<img src="https://drive.google.com/uc?id=1p0gY6azaaEPejcktNGE-piNVRK1pT3dE" width="100" height="60">|<img src="https://drive.google.com/uc?id=18Jr9vTGdlkiAVBHnuwNkBs1sUV1D43R1" width="100" height="70">|

- `Etc`

  |VS Code|Microsoft Teams|GitLab|Redmine|
  |:---:|:---:|:---:|:---:|
  |<img src="https://user-images.githubusercontent.com/68097036/151479933-01785e34-1283-4fca-a407-9fe284b50fa8.png" width="160" height="100">|![pngwing com (4)](https://user-images.githubusercontent.com/68097036/151467837-2cd89acd-2a92-45dd-b06b-e08e316b7695.png)|<img src="https://iridge.jp/wp-content/uploads/stacked_wm_no_bg.png" width="130" height="100">|<img src="https://drive.google.com/uc?id=1JqJjJ5uVi-KgsCv0ZOHF8_SvHPzOjRvn" width="160" height="80">|


<br>
<br>

## 7. 설정 및 구동

#### **Install requirements**

```bash
pip install -r requirements.txt
```

#### **SSLServer 설정 및 구동**  


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
python manage.py runsslserver 0.0.0.0:8443 --certificate django.crt --key django.key
```
