# ROS_Basic
for r1_mini Robot project \
프로젝트를 위한 가장 최소한의 ROS 정리합니다 \
만약 수정이 필요하다면 PR 남겨주세요! \
\
더 자세한 내용이 궁금하다면? [ROS wiki](http://wiki.ros.org/)

## 1. ROS 란
오픈소스 robot OS. 기본적인 OS 기능을 제공하며, robot을 다루기위한 여러 기능(심지어 package management)까지 제공.

## 2. 왜 ROS
ROS의 주된 목적이 로봇 연구 개발에서 코드 재사용을 쉽게 하자 였음. 따라서 일관적이며, 쓰기 쉬운 장점. 등등.

## 3. 용어

### 3-1. ROS 구조 관련
원본 : [ROS Concept](http://wiki.ros.org/ROS/Concepts)

- Master : ROS의 시작점 \
    -> 다른 모든 ROS 노드들이 연결되어 있다 \
    -> 여러 노드를 서로 연결하고, 통신을 할 수 있게한다 \
    -> 되돌아보면, `$ vi ~/.bashrc`에서 `ROS_MASTER_URI` 값을 데스크탑 URI로 설정했다.

- Node : 하나의 실행 가능한 프로그램 \
    -> 명령어를 통해 파일 하나를 실행하면 한 개 이상의 노드가 실행됨 \
    (4-2. rosnode에서 확인)

- Messages : 토픽에서 주고받는 데이터 (구조) \
    -> 표준 타입(int, floating point, boolean, etc.)을 지원

- Topic : 노드 간 통신 채널- 단방향 \
    -> 하나의 노드는 여러개 토픽을 만들어냄 \
    -> 메시지를 구분하기 위한 이름 
    - publish : 데이터를 만들어 보내는 쪽 (노드)
    - subscribe : 데이터를 받는 쪽 (노드)

- Service : 양방향 통신 채널 \
    -> Topic과 다르게 request/reply 형태의 통신 \
    -> srv 로 저장

- Bag : ROS 메시지를 저장하는 포맷

### 3-2. 그 외
- catkin : ROS의 빌드 시스템. \
    -> 되돌아보면, ROS 설치 과정에서 우리는 `$ catkin build `라는 명령어를 `~/catkin_ws` 디렉토리에서 실행했다 \
    -> 빌드와 관련한 여러 catkin 명령도 있다 (궁금하면 찾아보기) \
    -> `~/catkin_ws/src/omo_r1mini ` 디렉토리에 들어가면 r1 mini 관련 패키지를 볼 수 있음 \
    -> 새로운 패키지를 설치하고 싶다면 
    1. `:~/catkin_ws/src$` 에서 패키지를 clone 
    2. `$ cd .. ` (상위 폴더로 이동)
    3. `$ catkin build [package name]`

- rqt : gui 관련 서브패키지. \
    -> ROS 설치 시 같이 설치 \
    -> `$ rqt_image_view` , `$ rqt_bag` 등으로 실행

- rviz : (ros visualization tool) 영상 관련 서브패키지 \
    -> ROS 설치 시 같이 설치 \
    -> `$ rviz` 로 실행

## 4. ros 명령어
`ros core => roscore` 와 같은 패턴으로 명령어 구성

### 4-1. ros core : 
ROS를 사용하기 위해 가장 먼저 실행. \
Master + rosout + parameter server 동작
```shell
$ roscore
```
### 4-2. ros node : 
- 현재 실행된 node 보기
    ```shell
    $ rosnode list
    ```
    roscore 실행 중이면
    ```shell
    /rosout
    ```
    만 보인다

- 노드 상세 내용 보기
    ```shell
    $ rosnode info /rosout
    ```

### 4-3. ros run : 
패키지 이름으로 노드를 실행
```shell
$ rosrun [package_name] [node_name]
```
### 4-3-1 turtle sim 패키지의 노드 실행 (예제)
1. 노드 실행
    ```shell
    $ rosrun turtlesim turtlesim_node
    ```

2. 노드 확인
    ```shell
    $ rosnode list
    ```

3. rqt graph 보기
    ```shell
    $ 
    ```
- slam을 통해 만들어진 맵 저장
    ```shell
    $ rosrun map_server map_saver -f map
    ```

### 4-4. ros launch : 
`.launch` 파일로 정의된 node 실행
```shell
$ roslaunch [package] [filename.launch]
```
### 4-4-1 omo r1mini - 로봇의 node
로봇에 설치된 ROS에는 다양한 omo_r1mini package가 설치되어있음 (있는걸로 추측)


- bringup 패키지 \
bringup + lidar 실행
    ```shell
    $ roslaunch omo_r1mini_bringup omo_r1mini_robot.launch
    ```

- bringup 패키지의 lidar 
    ```shell
    $ roslaunch omo_r1mini_bringup omo_r1mini_lidar.launch
    ```

- slam 패키지 
    ```shell
    $ roslaunch omo_r1mini_slam omo_r1mini_slam.launch
    ```

- jetson camera 패키지 
    ```shell
    $ roslaunch jetson_camera jetson_camera.launch
    ```


### 4-4-2 omo r1mini - PC node
- slam 패키지의 rviz 노드 
    ```shell
    $ roslaunch omo_r1mini_slam omo_r1mini_slam_rviz.launch
    ```

- teleop 패키지 \
    *teleoperation : 원격 조정
    ```shell
    $ roslaunch omo_r1mini_teleop omo_r1mini_teleop_key.launch
    ```

### 4-5. ros topic :
토픽 관련 명령어
- 현재 발행 토픽, 구독 토픽 동시 보기
    ```shell
    $ rostopic list -v
    ```

- 토픽 내용 보기
    ```shell
    $ rostopic info rosout
    ```
    결과
    ```shell
    Type: rosgraph_msgs/Log

    Publishers: None

    Subscribers:
    * /rosout (http://192.168.8.23:35339/)
    ```
- 토픽에서 발행되는 내용 보기 \
odometry = 주행 거리 측정, echo = 실시간으로 발행되는 메시지 보기
    ```shell
    # robot
    $ rostopic echo /odom
    ```

### 4-6. ros service :
서비스 관련 명령어
- 현재 서비스 확인 
    ```shell
    $ rosservice list
    ```
    
- led 색상 바꾸는 명령
    ```shell
    $ rosservice call /set_led_color "red : 250 green: 50 blue: 50"
    ```

- battery 확인
    ```shell
    $ rosservice call /battery_status "{}"
    ```

- reset
    ```shell
    $ rosservice call /reset
    ```

- service 정보 보기
    ```shell
    $ rosservice info /turtle1/teleport_absolute
    ```

- service 요청하기
    ```shell
    $ rosservice call /turtle1/teleport_absolute 1 1 0
    ```

### 4-7. ros bag :
ros message 기록, 재생
- 전부 저장
    ```shell
    $ rosbag record -a
    ```

### 4-8. ros ed :
package 내부에 있는 파일을 edit 가능

```shell
$ rosed [package_name] [filename]
```

- ex) bringup package의 node.py 파일 수정
    ```shell
    $ rosed omo_r1mini_bringup omo_r1mini_node.py
    ```