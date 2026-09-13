print("Контроллер participant запущен")

#!/usr/bin/env python3
import math
import os
import sys

# путь к фиксированной локомоции (не трогай)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "common", "locomotion"))
from go2_api import Go2   # noqa: E402

def main():
    robot = Go2()
    checkpoints = [(2,0),(2,2),(0,2),(0,0)]  # пример координат
    cp = 0
    hold = 0
    state = "FORWARD"

    while robot.step():
        x,y,yaw = robot.pose()
        scan = robot.lidar_layer()

        tx,ty = checkpoints[cp]
        dist = math.hypot(tx-x, ty-y)

        if state == "FORWARD":
            if dist < 0.3:
                cp += 1
                if cp >= len(checkpoints):
                    state = "FINISH"
                    continue
            if min(scan[175:185]) < 0.5:  # впереди стена
                state = "TURN"
            else:
                robot.drive(0.4,0)

        elif state == "TURN":
            left = min(scan[90:120])
            right = min(scan[240:270])
            if left > right:
                robot.drive(0.2,0.8)
            else:
                robot.drive(0.2,-0.8)
            state = "FORWARD"

        elif state == "FINISH":
            robot.drive(0,0)
            hold += 1
            if hold > 120:  # 3 секунды при ~40 тиках/с
                break

if __name__ == "__main__":
    main()
