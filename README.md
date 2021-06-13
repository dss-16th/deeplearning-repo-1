# 드론 길들이기 (How to Train Your Drone)

- 딥러닝을 활용하여 손동작으로 드론을 조종한다.
- 기간 : 2021. 05. 03. ~ 2021. 06. 03.
- [김도겸](https://github.com/dockyum) : 드론 동작 프로그래밍, 모듈화
- [장혜임](https://github.com/mieyhgnaj) : 레퍼런스 조사(object tracking, gesture control, face recognition), 드론에 적용 테스트
- 👉🏼 [발표자료](https://www.icloud.com/keynote/0KOTU2vOxqReZHmUsTAo-_5cg#How_to_Train_Your_Drone)


</br>

```
☝🏻 핵심 내용

  - 드론에 딥러닝을 활용하는 방법
  - computer vision 관련 라이브러리 활용 방법
  - 실시간 서비스에서 딥러닝 사용 시 고려해야 할 점
```

</br>

&emsp; <img src="https://user-images.githubusercontent.com/73205057/121772913-7b1cc680-cbb3-11eb-96a7-4de7741c8658.gif" width="500">

&emsp; (얼굴 인식으로 드론을 이륙시키고, 제스처로 조종하는 중)


</br>

## 프로젝트 개요

### 전체 프로젝트 기획
</br>

<img src="https://user-images.githubusercontent.com/73205057/121645407-20aa3a00-cacf-11eb-9434-1f7ea2c51c5c.png" width="700">

</br>

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
- 약 19만원 (추가 배터리 포함)

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

<img src="https://user-images.githubusercontent.com/73205057/121772841-0d709a80-cbb3-11eb-9282-c72dedfb99ff.gif" width="500">

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

<img src="https://user-images.githubusercontent.com/73205057/121773042-4b21f300-cbb4-11eb-9ea7-4ef1970c5d1d.gif" height="70">
<img src="https://user-images.githubusercontent.com/73205057/121773044-4c532000-cbb4-11eb-924b-cd840baaf003.gif" height="70">

</br>

```
🤦🏻‍♂️ 근데 mask detecting & tracking mode의 속도가 keyboard control mode와 비교해서 굉장히 느리다..
   그래서인지 사람이 빠르게 지나가면 드론은 잡지 못한다..
```

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

<div align="left">
  <a href="https://youtu.be/EpHT2bJ2jco"><img src="https://user-images.githubusercontent.com/73205057/121773389-a2c15e00-cbb6-11eb-8a7d-cd2a78ec35ae.png" width="700" alt="IMAGE ALT TEXT"></a>
</div>

</br>

### MediaPipe

<img align="right" src="https://user-images.githubusercontent.com/73205057/121664322-53116280-cae2-11eb-8ae7-e925de413c3a.gif" width="500">

- 머신러닝 파이프 라인 구축을 위한 프레임 워크
- 비디오, 오디오, 시계열 데이터 등의 다양한 모드와
Android, iOS, 웹 등의 플랫폼에 적용 가능
- pip install mediapipe

</br>
</br>
</br>
</br>
</br>
</br>
</br>
</br>
</br>
</br>
</br>
</br>
</br>

### hand gesture

```
👏🏻 총 7가지의 제스처를 사용했다!
```

<img src="https://user-images.githubusercontent.com/73205057/121664654-a97ea100-cae2-11eb-8766-122a6811c347.png" width="270">

</br>

### 제스처 학습

```
✌🏻 거리 상관없이 인식이 잘 되게 하기 위한 노력
```

<img src="https://user-images.githubusercontent.com/73205057/121665763-7e488180-cae3-11eb-93db-1fc425feff52.gif" width="700">
&emsp; &emsp; &emsp; &emsp; &emsp; &emsp; 가까운 거리 &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; 먼 거리

</br>
</br>

### 학습의 중요성

```
🥺 뒤로 가라고 했는데.. 난데없이 착지를 한다..
```

<img src="https://user-images.githubusercontent.com/73205057/121666601-69202280-cae4-11eb-8396-022f0025d423.gif" width="700">

</br>

### 낮은 버퍼

```
😓 사진이 거의 1초 단위로 찍힌다.. ⇒ buffer_len=20 으로 수정
```

<img src="https://user-images.githubusercontent.com/73205057/121666886-b4d2cc00-cae4-11eb-8812-538956ffe238.png" width="700">

## 03 얼굴 인식으로 주인 확인

<img src="https://user-images.githubusercontent.com/73205057/121667409-34609b00-cae5-11eb-90a6-3960c44f2740.gif" width="450">

</br>

### face_recognition
- 딥러닝 기반으로 제작된 dlib의 최첨단 얼굴 인식 기능을 사용하여 구축
- 13,000개 이상의 얼굴 이미지가 포함된 Labeled Faces in the Wild 기준으로
정확도가 무려 99.38%
- 단 한장의 사진으로 얼굴 인식 가능!.!
- wow 😲
- pip install face_recognition

</br>

## 프로젝트 회고

### 시도해 본 "face recognition" 관련 github repo 리스트..

- [https://github.com/davidsandberg/facenet](https://github.com/davidsandberg/facenet)
- [https://github.com/cmusatyalab/openface](https://github.com/cmusatyalab/openface)
- [https://github.com/Skuldur/facenet-face-recognition](https://github.com/Skuldur/facenet-face-recognition)
- [https://github.com/Linzaer/Ultra-Light-Fast-Generic-Face-Detector-1MB](https://github.com/Linzaer/Ultra-Light-Fast-Generic-Face-Detector-1MB)
- [https://github.com/fyr91/face_recognition](https://github.com/fyr91/face_recognition)
- [https://github.com/ageitgey/face_recognition](https://github.com/ageitgey/face_recognition)

</br>

## REFERENCE

- F. Schroff, D. Kalenichenko and J. Philbin, "FaceNet: A unified embedding for face recognition and clustering," 2015 IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2015, pp. 815-823, doi: 10.1109/CVPR.2015.7298682. ([https://arxiv.org/abs/1503.03832](https://arxiv.org/abs/1503.03832))
