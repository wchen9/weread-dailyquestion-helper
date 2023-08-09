# -*- coding: utf-8 -*-
from aip import AipOcr
import io


class OCR:
    def __init__(self, appId, apiKey, secretKey):
        self.client = AipOcr(appId, apiKey, secretKey)

    def _pil2bin(self, pilObj):
        bin = io.BytesIO()
        pilObj.save(bin, format="JPEG")
        return bin.getvalue()

    def _ocr(self, img):
        imgBin = self._pil2bin(img)
        return self.client.basicGeneral(imgBin)

    def run(self, quesImg, optionImg):
        ques = self._ocr(quesImg)
        option = self._ocr(optionImg)
        ques = "".join([item["words"] for item in ques["words_result"]])
        try:
            option = [item["words"] for item in option["words_result"]]
        except:
            option = []
        return ques, option
