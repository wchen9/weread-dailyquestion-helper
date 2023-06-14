# -*- coding: utf-8 -*-
import json
import time

from PIL import ImageChops

from process.OCR import OCR
from process.OpenAIHelper import OpenAIHelper
from process.ScreenCapture import ScreenCapture


def isSame(imgA, imgB):
    if imgA is None or imgB is None:
        return False
    diff = ImageChops.difference(imgA, imgB)
    if diff.getbbox():
        return False
    return True


def getOCRConfig():
    with open("./config.json", "r", encoding="utf-8") as fp:
        return json.load(fp)


if __name__ == "__main__":
    config = getOCRConfig()

    sc = ScreenCapture()
    ocr = OCR(config["APP_ID"], config["API_KEY"], config["SECRET_KEY"])

    quesImg, optionImg = None, None
    helper = OpenAIHelper(config["OPENAI_KEY"])
    currQues = ""
    currOptions = []
    while True:
        tmpQuesImg, tmpOptionImg = sc.run()
        if not isSame(quesImg, tmpQuesImg):
            quesImg, optionImg = tmpQuesImg, tmpOptionImg
            ques, option = ocr.run(quesImg, optionImg)
            if ques == currQues:
                continue
            if option == currOptions:
                continue
            currQues = ques
            currOptions = option
            if not ques.strip():
                continue
            print("问题: {}".format(ques))
            print("选项: {}".format(option))
            answer = helper.answer(ques, option)
            print("正确答案: {}".format(answer))
            print("-----------------")
        time.sleep(0.8)
