# TIL
published by dockyum \
learn about deep learning

## Date
1. 5/11
2. 5/12
3. 5/13
3. 5/15

## Contents
### 5/11
- Inception 구현 예제 코드 읽기 \
    : [nevfiasco 블로그](https://nevfiasco.tistory.com/6)
    - inception module

- YOLO labeling \
    : m1에서 사용가능한 labeling tool
    [YOLO_label](https://github.com/developer0hye/Yolo_Label)
- [ROS wiki](http://wiki.ros.org/ROS/Tutorials)
    - 읽는 중

### 5/12
- ROS wiki 읽고 ROS_Basic.md 파일 작성
    - pinkwink 자료 포함

### 5/13
- 드론 프로젝트 방향 수정
- github repo 정리 수업 (4시간)

### 5/14
- colab에서 Yolo training 

### 5/15
- darknet object detecting 성능 평가
    - **현재의 cv2.dnn 모듈을 사용하는 코드는 fps가 느려서 개선이 필요**
    - input image frame을 낮추었는데, 이러면 학습을 더 시켜야함
    - 혹은 yolo5 사용.