import time
from io import BytesIO

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from PIL import Image

EMAIL = 'test@test.com'
PASSWORD = '123456'


class CrackGeetest():
    def __init__(self):
        self.url = 'https://account.geeetest.com/login'
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, 20)
        self.email = EMAIL
        self.password = PASSWORD

    def get_geetest_button(self):
        """
        获取初始验证按钮
        :return:
        """
        button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_radar_tip')))
        return button

    def get_screenshot(self):
        """
        获取网页截图
        :return:
        """
        screenshot = self.browser.get_screenshot_as_png()
        screenshot = Image.open(BytesIO(screenshot))
        return screenshot

    def get_position(self):
        """
        获取验证码位置坐标
        :return:
        """
        img = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_canvas_img')))
        time.sleep(2)
        location = img.location
        size = img.size
        top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size['width']
        return top, bottom, left, right

    def get_geetest_image(self, name='captcha.png'):
        """
        获取验证码图片
        :param name:
        :return:
        """
        top, bottom, left, right = self.get_position()
        print('验证码位置:', top, bottom, left, right)
        screenshot = self.get_screenshot()
        captcha = screenshot.crop((left, top, right, bottom))       # 把图片裁剪出来
        return captcha

    def get_slider(self):
        """
        获取滑块
        :return:
        """
        slider = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_slider_button')))
        return slider

    def exec(self):
        button = self.get_geetest_button()
        button.click()
        # 点按呼出缺口
        slider = self.get_slider()
        slider.click()

    def is_pixel_equal(self, image1, image2, x, y):
        """
        判断两张图片的某个像素点是否相同
        :param image1:
        :param image2:
        :param x:
        :param y:
        :return:
        """
        pixel1 = image1.load()[x, y]
        pixel2 = image2.load()[x, y]
        threshold = 60
        if abs(pixel1[0] - pixel2[0]) < threshold and abs(pixel1[1] - pixel2[1]) < threshold and \
                abs(pixel1[2] - pixel2[2]) < threshold:
            return True
        else:
            return False

    def get_gap(self, image1, image2):
        """
        遍历图片像素点，获取滑块缺口偏移量
        :param image1:
        :param image2:
        :return:
        """
        left = 60
        for i in range(left, image1.size[0]):
            for j in range(image1.size[1]):
                if not self.is_pixel_equal(image1, image2, i, j):   # 像素点不同
                    left = i
                    return left
        return left

    def get_track(self, distance):
        """
        根据偏移量计算移动轨迹
        :param distance: 运动总距离
        :return:
        """
        track = []                      # 移动轨迹
        current = 0                     # 当前位移
        mid = distance * 4 / 5          # 减速阈值
        t = 0.2                         # 计算间隔
        v = 0                           # 初速度

        while current < distance:
            if current < mid:           # a：加速度
                a = 2
            else:
                a = -3
            v0 = v                      # 初始速度
            v = v0 + a * t              # 当前速度
            move = v0 * t + 1 / 2 * a * t * t   # 移动距离
            current += move             # 当前位移
            track.append(round(move))
        return track

    def move_to_gap(self, slider, tracks):
        """
        移动滑块到缺口处
        :param slider: 滑块对象
        :param tracks: 运动轨迹
        :return:
        """
        ActionChains(self.browser).click_and_hold(slider).perform()
        for x in tracks:
            ActionChains(self.browser).move_by_offset(xoffset=x, yoffset=0).perform()
        time.sleep(0.5)
        ActionChains(self.browser).release().perform()
