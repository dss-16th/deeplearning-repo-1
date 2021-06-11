# 드론 길들이기 (How to Train Your Drone)

- 딥러닝을 활용하여 손동작으로 드론을 조종한다.
- 기간 : 2021. 05. 03. ~ 2021. 06. 03.
- [김도겸](https://github.com/dockyum) : 드론 동작 프로그래밍, 모듈화
- [장혜임](https://github.com/mieyhgnaj) : 레퍼런스 조사(object tracking, face recognition)
- 발표자료

</br>

왜 드론이었나

</br>

(고민중)

</br>

```
☝🏻 핵심 내용

  - 드론에 딥러닝을 활용하는 방법
  - computer vision 관련 라이브러리 활용 방법
  - 실시간 서비스에서 딥러닝 사용 시 고려해야 할 점
```

</br>

(다은찡 영상)

</br>

## 프로젝트 개요

### 전체 프로젝트 기획
</br>

<img src="https://user-images.githubusercontent.com/73205057/121645407-20aa3a00-cacf-11eb-9434-1f7ea2c51c5c.png" width="700">

### 프로젝트 구조
</br>

<img src="https://user-images.githubusercontent.com/73205057/121645461-30298300-cacf-11eb-89f6-1e422f09071a.png" width="700">

### 폴더 구조
</br>

<img src="https://user-images.githubusercontent.com/73205057/121645468-33247380-cacf-11eb-9f68-b1880ebe8e5c.png" width="700">

</br>

## 간단한 드론 소개 및 활용법

### DJI TELLO EDU

<img src="https://user-images.githubusercontent.com/73205057/121645480-3586cd80-cacf-11eb-9ae4-6e0634616dbb.png" width="300">

- 중량 : 87g
- 최대속도 : 8m/s
- 영상 : 720p
- 2.4GHz Wi-Fi 지원
- 19만원 (추가 배터리 포함)

</br>

### DJI TELLO EDU를 사용한 이유

- DJI에서 제공하는 python 모듈이 있다.
- 모듈을 참조하여 만든 패키지도 있다.
- 패키지를 활용한 사용 예제가 많다.

</br>

### 프로젝트에 사용한 드론 활용법

<img src="https://user-images.githubusercontent.com/73205057/121645490-3881be00-cacf-11eb-82f8-851908b44e92.png" width="700">

</br>

### 드론 사용법

<img src="https://user-images.githubusercontent.com/73205057/121645498-3a4b8180-cacf-11eb-87a3-1e1b4c9909bd.png" width="700">

</br>

### 딥러닝 및 여러 모델 적용법

<img src="https://user-images.githubusercontent.com/73205057/121645505-3c154500-cacf-11eb-9c01-75cb239e87da.png" width="700">

</br>

## 01 마스크 미착용자 트래킹

(용하 영상)

</br>

### mask detecting

- classes = [ with-mask, without-mask ]
- 드론 카메라로 영상 수집
- 실시간으로 랩탑에서 detecting

</br>

### YOLOv3

<img src="https://user-images.githubusercontent.com/73205057/121645520-3fa8cc00-cacf-11eb-8ba6-483e1e549203.png" width="700">

</br>

### 마스크 미착용자를 발견하면 드론 이륙

<img src="https://user-images.githubusercontent.com/73205057/121645525-41728f80-cacf-11eb-8e6d-3ac5ba0b5b84.png" width="600">

</br>

근데 속도가....

(영상 두개)

</br>

### 가장 오래 걸리는 코드는?

<img src="https://user-images.githubusercontent.com/73205057/121645536-43d4e980-cacf-11eb-9feb-75b0fa1b3b59.png" width="600">

</br>

### 결국 정확도와 속도 선택

<img src="https://user-images.githubusercontent.com/73205057/121645543-46374380-cacf-11eb-8994-2824af3a7560.png" width="600">

</br>

### 연산량을 줄이고자 하는 작은 노력..

<img src="https://user-images.githubusercontent.com/73205057/121645549-48999d80-cacf-11eb-9f71-086bdf3ab605.png" width="600">

</br>

### 트래킹 방법

<img align="left" src="https://user-images.githubusercontent.com/73205057/121645561-4afbf780-cacf-11eb-90ef-255c3cc960b3.png" width="350">

### - 방향 조절

&ensp; 1. 드론 영상의 중심을 구한다</br>
&ensp; 2. 바운딩 박스의 중심을 구한다</br>
&ensp; 3. 차이 나는 방향으로 이동! (방향 조절)

### - 거리 조절

&ensp; 1. 얼굴 크기 박스의 크기를 정해둔다</br>
&ensp; 2. 바운딩 박스의 면적을 구한다</br>
&ensp; 3. 1번이 크면 전진, 2번이 크면 후진
  
</br>
</br>

## 02 제스처 컨트롤

</br>

## 03 얼굴 인식으로 주인 확인

</br>

## 프로젝트 회고

</br>

## REFERENCE

</br>
