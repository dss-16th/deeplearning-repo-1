# ROS tutorial
흐름 파악을 위해 명령어만 모았습니다
## 목차

## Rosbag
```shell
roscore
rosrun turtlesim turtlesim_node
```
```shell
rosrun turtlesim turtle_teleop_key
rosnode info /teleop_turtle
# > cmd_vel 토픽을 publish 함
```
현재 토픽 확인
```shell
rostopic list
```
1. 전체 토픽 저장
```shell
rosbag record -a
```
2. 액션
```shell
rosrun turtlesim turtle_teleop_key
```
3. 실행 종료하면 파일이 하나 생성됨.
```shell
rosbag info 2021....bag
```
4. reset을 call
```shell
rosservice call /reset
```
5. rosbag play
```shell
rosbag play 2021 ... bag
```