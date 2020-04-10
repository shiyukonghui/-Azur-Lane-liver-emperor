import pyautogui as Auto
from PIL import Image
from PIL import ImageGrab
import imagehash
import cv2
import time
import numpy as np
import os

# 颜色控制
B = (255, 0, 0)
G = (0, 255, 0)
R = (0, 0, 255)

"""
章节对应坐标
"""
map_sign_pt = {"2-1": (1090, 620), "2-2": (1038, 406), "2-3": (670, 475), "2-4": (750, 690),
               "3-1": (760, 430), "3-2": (622, 654), "3-3": (1070, 360), "3-4": (930, 546),
               "4-1": (630, 500), "4-2": (773, 633), "4-3": (1100, 690), "4-4": (1060, 490),
               "5-1": (632, 548), "5-2": (1125, 684), "5-3": (1030, 550), "5-4": (913, 427),
               "6-1": (1170, 655), "6-2": (1000, 530), "6-3": (780, 430), "6-4": (680, 600),
               "7-1": (604, 641), "7-2": (810, 400), "7-3": (1100, 484), "7-4": (1200, 614),
               "8-1": (878, 408), "8-2": (660, 542), "8-3": (708, 711), "8-4": (1067, 622),
               "9-1": (632, 444), "9-2": (743, 646), "9-3": (1070, 467), "9-4": (1172, 670),
               "10-1": (660, 448), "10-2": (748, 650), "10-3": (1080, 470), "10-4": (1180, 675)}
"""
页面切换按钮，左，右
"""
page_change = {"left": (485, 523), "right": (1430, 525)}
"""
困难按钮
"""

hard_made = {"hard": (514, 764)}
"""
活动档案
"""
operation_file = {"file": (686, 766)}
ex1 = {"a1": (787, 400), "a2": (1030, 673), "a3": (1155, 455), "b1": (724, 674), "b2": (1140, 654),
       "b3": (1002, 436)}
ex_files = {"ex1": (690, 430), "ex2": (1206, 434), "ex3": (703, 668)}

sp_button = {"sp_button": (1288, 270)}
sp_files = {"sp1": (701, 428), "sp2": (1230, 430)}
"""
特别活动
"""
special_events = {"event": (1410, 380)}
special_files = {"a1": (705, 439), "a2": (840, 700), "a3": (1128, 476), "b1": (686, 568), "b2": (1000, 700),
                 "b3": (1135, 445), "c1": (705, 439), "c2": (840, 700), "c3": (1128, 476), "d1": (686, 568),
                 "d2": (1000, 700),
                 "d3": (1135, 445)}


def key_down(key, time0, num):
    """
    函数功能：按下按键停留一定时间在弹起
    参    数：key:按键值     || time0 :具体时间
    """
    if num - 1 > 0:
        for i in range(num - 1):
            Auto.keyDown(key)
            time.sleep(time0)
            Auto.keyUp(key)
            time.sleep(0.2)
    else:
        Auto.keyDown(key)
        time.sleep(time0)
        Auto.keyUp(key)
        time.sleep(0.2)


def mouse_to_click(x, y, t):
    """
    鼠标移动，并且点击
    t 单位是s
    """
    Auto.moveTo(x, y, duration=0.4)
    Auto.click()
    time.sleep(t)


def list_bj(position):
    """
    进行坐标数组比较，以去重
    如果x,y之和与所有的已有坐标x,y和的绝对值的差大于一定值，
    即距离太近的，保留一个就可
    如果zlist是空的，就不比较，直接加入
    """
    zlist = []
    if len(position) > 0:
        for blist in position:
            n = 0
            zlen = len(zlist)
            if zlen > 0:
                for item in zlist:
                    key1 = max(blist[0], item[0])
                    key2 = min(blist[0], item[0])
                    key3 = max(blist[1], item[1])
                    key4 = min(blist[1], item[1])
                    if max(key1 - key2, key3 - key4) > 75:
                        n += 1
            else:
                pass
            if n == zlen:
                zlist.append(blist)
            else:
                pass

    return zlist


def draw(imglist, target, name, S):
    """
    在图中画框，
    imglist 是要画的点的坐标
    target 是图
    name 是框标明的名称
    S 输入B, G, R 改变颜色
    """
    if imglist is None:
        pass
    else:
        for x, y in imglist:
            # 框的高度，宽度
            w, h = (50, 50)
            # 画框,x,y左上角,
            cv2.rectangle(target, (x, y), (x + w, y + h), S, 2, 1)
            # 显示图片
            # 使用默认字体
            font = cv2.FONT_HERSHEY_SIMPLEX
            # 在坐标x,y处写字，不能中文
            cv2.putText(target, name, (x, y), font, 0.5, S, 2)


def dict_out(list_zb, center_sign):
    """
    接收一个坐标列表
    比较坐标相对图中心的距离
    返回距离由近到远的列表
    """
    sun_zb = []
    sum_zb1 = []
    w, h = center_sign
    long = len(list_zb)
    if long > 0:
        for n in range(long):
            name, sign = list_zb[n]
            if "BOSS" in name:
                sum_zb1.append((name, sign))
            else:
                x, y = sign
                sum_bj = max(w, x) + max(h, y) - min(w, x) - min(h, y)
                sun_zb.append((sum_bj, n))

        sun_zb.sort(reverse=True)
        for m in sun_zb:
            n = m[1]
            sum_zb1.append(list_zb[n])
    else:
        pass
    return sum_zb1


def Picture(pic, px, py, px1, py1):
    """
    (px,py) 是左上角
    (px1,py1) 是右下角
    """
    bbox = (px, py, px1, py1)
    picture0 = ImageGrab.grab(bbox)
    picture0.save(pic)


def moving_map(num, move_num):
    key_num = ['s', 's', 'a', 'a', 'd', 'd', 'd', 'd', 'w', 'w', 'a', 'a']
    key_down(key_num[num], 0.7, 3 * move_num)
    num += 1
    if num == len(key_num):
        num = 0
    return num


class Bule_Ai:
    def __init__(self):
        self.px = 550
        self.py = 350
        self.px1 = 1410
        self.py1 = 725
        self.dict_img = {}
        self.value = 10  # 二次匹配时 hash匹配的阈值
        self.threshold = 0.02  # 一次匹配时的匹配度  ，1-threshold 为实际阈值
        self.center_sign = (430, 187)  # 图中心坐标，决定相对距离
        self.pic = "D:\\BL\\Break\\picture.jpg"
        self.map_ambush_rf = "D:\\BL\\ZT\\map_ambush.JPG"
        self.map_ambush_gf = "D:\\BL\\ZT\\map_ambush_gf.JPG"
        self.monster_ordinary = "D:\\BL\\Project\\PTImg\\"
        self.monster_special = "D:\\BL\\Project\\HDImg\\"
        self.fight_num = 0
        self.play_state_dt = "D:\\BL\\ZT\\ZT_DT.JPG"
        self.play_state_fb = "D:\\BL\\ZT\\ZT_FB.JPG"
        self.play_state_rf_dt = "D:\\BL\\ZT\\RFZT_DT.JPG"
        self.play_state_rf_fb = "D:\\BL\\ZT\\RFZT_FB.JPG"
        self.play_state_dt_hd = "D:\\BL\\ZT\\HDZT_DT.JPG"
        self.play_state_fb_hd = "D:\\BL\\ZT\\HDZT_FB.JPG"
        self.play_state_rf_dt_hd = "D:\\BL\\ZT\\RF_HDZT_DT.JPG"
        self.play_state_rf_fb_hd = "D:\\BL\\ZT\\RF_HDZT_FB.JPG"

    def open_img(self, path):
        """
        path 是小模版的文件夹地址
        将文件名及其地址加入到字典
        """
        if os.path.exists(path):
            list_name = os.listdir(path)
            for item in list_name:
                name = item.split(".")
                path_pic = path + item
                self.dict_img.update({name[0]: path_pic})

    def found_pic(self, small_name, small_pic, big_pic):
        # 坐标数组
        # 输入为图片名
        zb1 = []
        '''
        small_pic 是小图片的地址
        big_pic 是大图片的地址
        '''
        big_img = cv2.imread(big_pic)
        limit_img = cv2.imread(small_pic)

        big_img = cv2.cvtColor(big_img, cv2.COLOR_BGR2GRAY)
        limit_img = cv2.cvtColor(limit_img, cv2.COLOR_BGR2GRAY)
        # 执行模板匹配，采用的匹配方式cv2.TM_SQDIFF_NORMED
        result = cv2.matchTemplate(limit_img, big_img, cv2.TM_SQDIFF_NORMED)
        # 归一化处理
        cv2.normalize(result, result, 0, 1, cv2.NORM_MINMAX, -1)
        # min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        # 寻找矩阵（一维数组当做向量，用Mat定义）中的最大值和最小值的匹配结果及其位置
        # 对于cv2.TM_SQDIFF及cv2.TM_SQDIFF_NORMED方法min_val越趋近与0匹配度越好，
        # 对于其他方法max_val越趋近于1匹配度越好，
        # target原始图片
        # px,py 起始坐标
        # w,h 返回的宽长
        # 调整匹配度
        # 匹配程度大于90%的坐标y,x
        loc = np.where(result <= self.threshold)
        zb_list = zip(*loc[::-1])

        if loc is None:
            pass
        else:
            zb = list_bj(zb_list)
            for op in zb:
                zb1.append((small_name, op))

        """
        zb1.append((small_name, (min_loc[0], min_loc[1])))
        t2 = time.time()
        print("[-]" + small_name + "扫描耗时：" + str(t2 - t1) + "s")
        """
        pic_list, list_screen = self.pic_hash(small_pic, big_pic, zb1)
        return pic_list, list_screen

    def pic_hash(self, small_pic, big_pic, place):
        # 打开大,小图片
        # place为坐标数组
        list_true = []
        list0 = []
        limit_img = Image.open(small_pic)
        big_img = Image.open(big_pic)
        # 小图片的宽，高
        x0, y0 = limit_img.size
        # 获取hash
        lim_hash = imagehash.average_hash(limit_img)
        # 以相同像素点为起点，剪切图片,并获得hash，在对比hash差
        for name, sign in place:
            x, y = sign
            box = (x, y, x + x0, y + y0)
            img_bj = big_img.crop(box)
            big_hash = imagehash.average_hash(img_bj)
            key = lim_hash - big_hash
            # value 为阈值,大于阈值的为不匹配
            if key > self.value:
                pass
            else:
                print("[-]发现 :" + str(name) + " | " + "匹配值 :" + str(100 - key))
                list0.append((x, y))
                x = self.px + x + round(x0 / 2)
                y = self.py + y + round(y0 / 2)
                list_true.append((name, (x, y)))

        return list0, list_true

    def obtain_coordinates(self):
        """
        输出各怪坐标
        """
        list_screen1 = []
        t1 = time.time()
        Picture(self.pic, self.px, self.py, self.px1, self.py1)
        # target = cv2.imread(self.pic)
        for small_name in self.dict_img:
            small_path = self.dict_img[small_name]
            # small_path 是模板地址，pic是截图
            # pic_list 是进行二次（hash）验证后的图坐标,准确度更高，list_screen 结构(名称，屏幕坐标)，控制鼠标用
            pic_list, list_screen = self.found_pic(small_name, small_path, self.pic)
            # draw(pic_list, target, small_name, R)
            list_screen1 = list_screen1 + list_screen

        """
        cv2.imshow("233", target)
        cv2.waitKey(3)
        """
        list_h = list_bj(list_screen1)
        # 坐标排序,center_sign 图中心坐标
        list_h = dict_out(list_h, self.center_sign)
        # t2 = time.time()
        # print("[o]坐标分析耗时：" + str(t2 - t1) + "s")
        return list_h

    def play_state(self, state_button):
        bbox = (1190, 744, 1300, 785)
        img_break = ImageGrab.grab(bbox)
        """
        判断是在地图里，还是地图外，或者战斗中
        普通地图
        """
        if state_button[0] == "GF":
            if state_button[1] == "PT":
                img_dt = Image.open(self.play_state_dt)
                img_fb = Image.open(self.play_state_fb)
            else:
                img_dt = Image.open(self.play_state_dt_hd)
                img_fb = Image.open(self.play_state_fb_hd)

        elif state_button[0] == "RF":
            if state_button[1] == "PT":
                img_dt = Image.open(self.play_state_rf_dt)
                img_fb = Image.open(self.play_state_rf_fb)
            else:
                img_dt = Image.open(self.play_state_rf_dt_hd)
                img_fb = Image.open(self.play_state_rf_fb_hd)

        hash_fb = imagehash.average_hash(img_fb)
        hash_dt = imagehash.average_hash(img_dt)
        hash_break = imagehash.average_hash(img_break)
        if hash_dt - hash_break < 8:
            return "d"
        elif hash_fb - hash_break < 8:
            return "f"
        else:
            return "z"

    def play_map_ambush(self, state_button):
        """
        1.截图,2.读取,3.识别是否遇到伏击
        """
        state = state_button[0]
        if state == "GF":
            ambush_serve = self.map_ambush_gf
        else:
            ambush_serve = self.map_ambush_rf
        bbox = (1234, 580, 1344, 620)
        picture = ImageGrab.grab(bbox)
        ambush = Image.open(ambush_serve)
        ambush_hash = imagehash.average_hash(ambush)
        hash_bj = imagehash.average_hash(picture)
        """
        遇到伏击，返回True ,反之 False
        """
        if ambush_hash - hash_bj < 5:
            return True
        else:
            return False

    def return_coordinates(self, num):
        """
        输入一个整数，返回一个坐标
        resoluton 步进多少像素
        n1, n2 确定坐标中点
        """
        num1 = num % 4
        num2 = num // 4
        resolution = 100
        n1 = (self.px + self.px1) // 2
        n2 = (self.py + self.py1) // 2
        if num1 == 0:
            px = n1 - resolution * num2
            py = n2 - resolution * num2
        elif num1 == 1:
            px = n1 + resolution * num2
            py = n2 - resolution * num2
        elif num1 == 2:
            px = n1 + resolution * num2
            py = n2 + resolution * num2
        else:
            px = n1 - resolution * num2
            py = n2 + resolution * num2
        """
        防止坐标超出界面
        """
        if px < self.px:
            px = self.px + 200
        elif px > self.px1:
            px = self.px1 - 200
        if py < self.py:
            py = self.py + 200
        elif py > self.py1:
            py = self.py1 - 200
        print("[-]使用遍历坐标中")
        return px, py

    def playing(self, fb_x, fb_y, number, state_button):
        """
        输入副本坐标，点击确定，选择舰队，确定选择，三步后进图
        """
        time.sleep(3)
        mouse_to_click(fb_x, fb_y, 0.8)

        mouse_to_click(1200, 640, 0.8)

        mouse_to_click(1310, 710, 4)

        # Auto.moveTo(980, 540, duration=0.3)
        """
        活动地图，把地图移动到左上角
        """
        if state_button[1] == "HD":
            pass
        else:
            pass

        map_move_num = 0
        map_move_really = 0
        map_move = 0
        map_fire = 0
        FB_NUM = 1
        t0 = time.time()
        while True:
            """
            先判断状态
            """
            state = self.play_state(state_button)
            if state == "z":
                print("[p1]战斗中...")
                mouse_to_click(1380, 740, 1.8)
                mouse_to_click(1080, 640, 1.8)
            elif state == "f":
                FB_NUM += 1
                if FB_NUM > int(number):
                    break
                else:
                    t0 = time.time()
                    print("[+]第" + str(FB_NUM) + "次")
                    mouse_to_click(fb_x, fb_y, 0.8)

                    mouse_to_click(1200, 640, 0.8)

                    mouse_to_click(1310, 710, 0.8)
                    """
                    如果是档案，点确定消耗钥匙
                    """
                    mouse_to_click(1080, 640, 0.8)
                    time.sleep(3)
                    map_move_really = 0
                    # Auto.moveTo(980, 540, duration=0.3)
            else:
                """
                截图获取坐标
                """
                if state_button[1] == "HD":
                    pass

                print("[p2]寻找目标...")
                """
                移动地图, map_move_really 记录一次刷本过程中的所有地图移动次数
                """
                if map_move > 3:
                    map_move = 0
                    map_move_really += 1
                    if map_move_really > 3:
                        map_move_really = 3
                    map_move_num = moving_map(map_move_num, map_move_really)
                else:
                    pass
                """
                切换舰队
                """
                if map_fire > 2:
                    mouse_to_click(1320, 770, 0.8)
                    time.sleep(1.2)
                    map_fire = 0
                else:
                    pass

                """
                判断是否遇到伏击
                """
                ambush = self.play_map_ambush(state_button)
                if ambush:
                    print("[p4]遇到伏击，尝试规避")
                    mouse_to_click(1320, 600, 0.8)
                else:
                    pass

                coordinates = self.obtain_coordinates()
                if len(coordinates) == 0:
                    print("[p2]未能发现目标,移动地图")
                    map_move_really += 1
                    map_move_num = moving_map(map_move_num, map_move_really)
                    if map_move_really > 3:
                        map_move_really = 3

                else:
                    boss_pass = 0
                    for name, zb in coordinates:
                        x, y = zb
                        print("[p3]选择目标:" + name + str((x, y)))
                        """
                        活动本的坐标分两步走，防止无法到达
                        """
                        if state_button[1] == "HD":
                            key1 = max(980, x)
                            key2 = min(980, x)
                            key3 = max(540, y)
                            key4 = min(540, y)
                            tx = key1 - (key1 - key2) // 2
                            ty = key3 - (key3 - key4) // 2
                            time.sleep(0.5)
                            mouse_to_click(tx, ty, 0.8)
                            time.sleep(1.5)
                            mouse_to_click(x, y, 0.8)
                            time.sleep(1.5)
                        else:
                            time.sleep(0.6)
                            mouse_to_click(x, y, 0.8)
                            time.sleep(3.6)
                        """
                        判断是否遇到伏击
                        """
                        ambush = self.play_map_ambush(state_button)
                        if ambush:
                            print("[p4]遇到伏击，尝试规避")
                            mouse_to_click(1320, 600, 0.8)
                            state = self.play_state(state_button)
                            if state == "f":
                                break

                            elif state == "d":
                                """
                                规避成功，继续之前坐标                            
                                """
                                print("[p4.1]规避成功..")
                                time.sleep(0.6)
                                mouse_to_click(x, y, 0.8)
                                time.sleep(3.6)

                            else:
                                print("[p5]规避失败,战斗中..." + name + str((x, y)))
                                while True:
                                    state = self.play_state(state_button)
                                    if state == "d":
                                        print("[p5.1]战斗结束:" + name)
                                        map_fire += 1
                                        map_move = 0
                                        break
                                    elif state == "f":
                                        print("[p5.1]战斗结束:" + name)
                                        break
                                    else:
                                        """
                                        上下不断点击，位置是捞出货时确定键，及结束时的确定键
                                        """
                                        mouse_to_click(1380, 740, 1.8)
                                        mouse_to_click(1080, 640, 1.8)
                                if state == "f":
                                    break
                        else:
                            state = self.play_state(state_button)
                            if state == "f":
                                FB_NUM += 1
                                if FB_NUM > int(number):
                                    break
                                else:
                                    t0 = time.time()
                                    print("[+]第" + str(FB_NUM) + "次")
                                    mouse_to_click(fb_x, fb_y, 0.8)

                                    mouse_to_click(1200, 640, 0.8)

                                    mouse_to_click(1310, 710, 4)
                                    map_move_really = 0
                                    # Auto.moveTo(980, 540, duration=0.3)
                                    break

                            elif state == "d":
                                """
                                可能因为各种原因中断                           
                                一次周期2次无效行动，切换舰队                            
                                """
                                print("[6]地图中...")
                                map_move += 1
                                if name == "BOSS":
                                    if boss_pass is 0:
                                        coordinates.append((name, zb))
                                        boss_pass += 1
                                    else:
                                        pass

                            else:
                                t1 = time.time()
                                print("[p5]战斗中..." + name + str((x, y)))
                                while True:
                                    state = self.play_state(state_button)
                                    if state == "d":
                                        t2 = time.time()
                                        print("[p5.1]与:" + name + "战斗结束，用时:" + str(t2 - t1) + "s")
                                        map_fire += 1
                                        map_move = 0
                                        break
                                    elif state == "f":
                                        t3 = time.time()
                                        print("[p5.1]任务结束,用时:" + str(t3 - t0) + "s")
                                        break
                                    else:
                                        mouse_to_click(1380, 740, 1.8)
                                        mouse_to_click(1080, 640, 1.8)
                                if state == "f":
                                    map_move_really = 0
                                    break

        print("[OK]任务目标完成")

    def start(self):
        """
        3-4 是 930,540
        """
        fb_x = 930
        fb_y = 540
        state_button = []
        state_b = input("[0]服务器国服 y/n \r\n")
        """
        服务器状态选择
        """
        if state_b == "y":
            state_button.append("GF")
        else:
            state_button.append("RF")

        res0 = input("[1]是否选择目标 y/n \r\n")
        if res0 == "y":

            fb = input("[2]普通章节，活动档案，特别活动，输入：1 || 2 || 3 \r\n")
            if fb == "1":
                """
                首先选择打开普通怪标签，状态标签选择普通
                """
                self.open_img(self.monster_ordinary)
                state_button.append("PT")
                map_default = input("[2.1.1]输入默认章节（出击按钮后的章节），如4，6 \r\n")
                map_target = input("[2.1.2]目标具体章节及任务次数,如 3-3-4 ，4-1-2 \r\n")
                map_big_target, map_small_target, number = map_target.split("-")
                map_target = map_big_target + "-" + map_small_target
                hard_choose = input("[2.1.3]是否困难模式 y/n \r\n")
                print("[!]准备开始，请切换 \r\n")
                time.sleep(3)
                if hard_choose == "y":
                    x, y = hard_made["hard"]
                    mouse_to_click(x, y, 1)
                else:
                    pass
                """
                如果大，则点击向右，大几就点击几次
                """
                if int(map_big_target) > int(map_default):
                    map_num = int(map_big_target) - int(map_default)
                    x, y = page_change["right"]
                    for i in range(map_num):
                        mouse_to_click(x, y, 0.8)
                    """
                        从字典中获得坐标
                        """
                    fb_x, fb_y = map_sign_pt[map_target]
                    self.playing(fb_x, fb_y, number, state_button)

                else:
                    map_num = int(map_default) - int(map_big_target)
                    if map_num == 0:
                        x1, y1 = map_sign_pt[map_target]
                        self.playing(x1, y1, number, state_button)
                    else:
                        x, y = page_change["left"]
                        for i in range(map_num):
                            mouse_to_click(x, y, 0.8)
                        fb_x, fb_y = map_sign_pt[map_target]
                        self.playing(fb_x, fb_y, number, state_button)

            elif fb == "2":
                """
                首先选择打开普通怪标签,档案中船模与普通本一样
                点击活动档案按钮
                """
                self.open_img(self.monster_ordinary)
                state_button.append("PT")
                x1, y1 = operation_file["file"]
                operation = input("[2.2.1]目标ex or sp \r\n")
                if operation == "ex":
                    ex = input("[2.2.2] 目标ex几 \r\n")
                    if ex == "ex1":
                        x, y = ex_files["ex1"]
                        limit = input("[2.2.3] 具体小节及任务次数，如a1-3,b1-2 \r\n")
                        limit, number = limit.split("-")
                        limit_big, limit_small = limit
                        print("[!]准备开始，请切换\r\n")
                        time.sleep(3)
                        mouse_to_click(x1, y1, 0.8)
                        mouse_to_click(x, y, 0.8)
                        if limit_big == "a":
                            try:
                                fb_x, fb_y = ex1[limit]
                                self.playing(fb_x, fb_y, number, state_button)
                            except:
                                print("[!][2.2.2]参数错误 \r\n")

                        elif limit_big == "c":
                            x, y = page_change["right"]
                            mouse_to_click(x, y, 0.8)
                            try:
                                fb_x, fb_y = ex1[limit]
                                self.playing(fb_x, fb_y, number, state_button)
                            except:
                                print("[!][2.2.2]参数错误 \r\n")
                        else:
                            """
                                c1-3,d1-3要点击困难模式按钮
                                """
                            x, y = hard_made["hard"]
                            mouse_to_click(x, y, 0.8)
                            if limit_big == "d":
                                x, y = page_change["right"]
                                mouse_to_click(x, y, 0.8)
                                try:
                                    fb_x, fb_y = ex1[limit]
                                    self.playing(fb_x, fb_y, number, state_button)
                                except:
                                    print("[!][2.2.2]参数错误 \r\n")
                            else:
                                try:
                                    fb_x, fb_y = ex1[limit]
                                    self.playing(fb_x, fb_y, number, state_button)
                                except:
                                    print("[!][2.3.3]参数错误\r\n")
                    else:
                        print("[!]暂时没有坐标\r\n")

            elif fb == "3":
                """
                点击活动按钮,船模选择活动,加载活动时的怪对比模板
                """
                self.open_img(self.monster_special)
                state_button.append("HD")
                limit = input("[2.3.1] 输入具备小节及任务次数，如a1-2,a3-4,b3-3 \r\n")
                try:
                    limit, number = limit.split("-")
                    limit_big, limit_small = limit
                except:
                    print("[2.3.1]参数错误")
                print("[!]准备切换，即将开始\r\n")
                time.sleep(3)
                x1, y1 = special_events["event"]
                mouse_to_click(x1, y1, 0.8)
                if limit_big == "a":
                    try:
                        fb_x, fb_y = special_files[limit]
                        self.playing(fb_x, fb_y, number, state_button)
                    except:
                        print("[!][2.3.2]参数错误\r\n")
                elif limit_big == "b":
                    x, y = page_change["right"]
                    mouse_to_click(x, y, 0.8)
                    try:
                        fb_x, fb_y = special_files[limit]
                        self.playing(fb_x, fb_y, number, state_button)
                    except:
                        print("[!][2.3.2]参数错误\r\n")
                else:
                    """
                    c1-3,d1-3要点击困难模式按钮
                    """
                    x, y = hard_made["hard"]
                    mouse_to_click(x, y, 0.8)
                    if limit_big == "d":
                        x, y = page_change["right"]
                        mouse_to_click(x, y, 0.8)
                        try:
                            fb_x, fb_y = special_files[limit]
                            self.playing(fb_x, fb_y, number, state_button)
                        except:
                            print("[!][2.3.2]参数错误\r\n")
                    else:
                        try:
                            fb_x, fb_y = special_files[limit]
                            self.playing(fb_x, fb_y, number, state_button)
                        except:
                            print("[!][2.3.3]参数错误\r\n")

            else:
                print("[!]参数错误 \r\n")

        else:
            self.playing(fb_x, fb_y, 10, state_button)


if __name__ == "__main__":
    blan = Bule_Ai()
    blan.start()
