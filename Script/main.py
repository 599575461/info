# -*- coding: UTF-8 -*-
# @Time : 2023/2/10 16:06
# @Author : Installation
# @Email : 599575461@qq.com
# @File : main.py
# @Project : info


import json
import os
import os.path
import shutil
import subprocess
import sys
import webbrowser
from ast import literal_eval
from typing import Union
import Mainwindow
import urllib3
import winsound
from PyQt5.QtCore import (
    Qt,
    QCoreApplication,
    QPoint,
    QThread,
    QObject,
    QSize,
    QUrl,
    pyqtSignal,
    QRect,
    QPropertyAnimation,
    pyqtProperty,
    QTranslator,
    QTimer,
    QModelIndex,
)
from PyQt5.QtGui import (
    QMouseEvent,
    QPixmap,
    QIcon,
    QCloseEvent,
    QShowEvent
)
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtWidgets import (
    QApplication,
    QFrame,
    QFileDialog,
    QDialog,
    QLabel,
    QGraphicsPixmapItem,
    QGraphicsScene,
    QLineEdit,
    QFileSystemModel,
)
from playsound import playsound
from requests import get

import File_Search
import MUSIC
import Video
import info
import more_info_
import setting
from API.EDN import EDNCrypto, English
from MQMessageBox import Ui_Dialog
from losder import Losder


def right(num, self):
    return QPoint(main_window.x() + main_window.width(), main_window.y() + num)


def left(num, self):
    return QPoint(main_window.x() - self.width(), main_window.y() + num)


def bottom(num, self):
    return QPoint(main_window.x() + num, main_window.y() - main_window.height())


def topmost(num, self):
    return QPoint(main_window.x() + num, main_window.y() - self.height())


class Searchs(QFrame, File_Search.Ui_Form):
    def __init__(self) -> None:
        super().__init__()
        self._isTracking = None
        self._startPos = None
        self._startPos = None
        self._endPos = None
        self.setupUi(self)
        self.model = QFileSystemModel()
        self.model.setRootPath(cwd)
        self.treeView.setModel(self.model)

        self.setWindowFlags(Qt.WindowMaximizeButtonHint | Qt.WindowCloseButtonHint)
        self.setFixedSize(self.width(), self.height())

        self.treeView.clicked.connect(self.play_mps)

    def play_mps(self, index: QModelIndex) -> None:
        data = self.model.filePath(index)
        if os.path.isfile(data):
            new_name = get_splits(data)
            if new_name in audio_type:
                mm.play(data)
            if new_name in video_type:
                videos.ffmpeg_play(data)
            if new_name == "exe":
                os.system(f"start {data}")
            if new_name == "txt":
                os.system(f"notepad.exe {data}")


class Conver(QThread):
    def __init__(self, file_source_text, finish_source_text, is_del_log=False, is_save=False, is_open_now=False,
                 parent=None) -> None:
        super(Conver, self).__init__(parent)

        self.finish_source_text = finish_source_text
        self.file_source_text = file_source_text
        self.is_del_log = is_del_log
        self.is_save = is_save
        self.is_open_now = is_open_now

    def run(self) -> None:
        subprocess.Popen(
            f"""ffmpeg/ffmpeg.exe -report -i {self.file_source_text}  -threads 5 {self.finish_source_text} -y""",
            shell=False).wait()
        if self.is_del_log:
            for files in os.listdir(cwd):
                if get_splits(files) == "log":
                    os.system(files)
                    os.unlink(files)
        if self.is_open_now:
            if self.finish_source_text in video_type:
                videos.ffmpeg_play(self.finish_source_text)
            elif self.finish_source_text in audio_type:
                mm.play(self.finish_source_text)
        if self.is_save:
            # 配置文件 保存配置文件
            fileName_choose = \
                get_file_search(['json'], fileCheckType=[self.tr('Configuration file')], mode=1,
                                title=self.tr("Save the configuration file"),
                                parent=main_window)[0]
            if fileName_choose != "":
                with open(fileName_choose, "w+") as w:
                    json.dump({
                        "file_source": self.file_source_text,
                        "finish_source": self.finish_source_text,
                        "is_open_now": self.is_open_now,
                        "is_del_log": self.is_del_log,
                        "is_save": self.is_save,
                    }, w)

        MessageBox.info("succeed", "The conversion was successful")


class MQLineEdit(QLineEdit):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, e) -> None:
        if e.mimeData().hasText():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e) -> None:
        self.setText(e.mimeData().text().split('\n')[0].replace('file:///', '', 1))


class MQLabel(QLabel):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, e) -> None:
        if e.mimeData().hasText():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e) -> None:
        filePath = e.mimeData().text().split('\n')[0].replace('file:///', '', 1)
        type_ = get_splits(filePath)
        if type_ in audio_type:
            mm.play(filePath)
        elif type_ in video_type:
            videos.ffmpeg_play(filePath)
        else:
            pass


# TODO

class MoreInfo(QDialog, more_info_.Ui_Dialog):

    def __init__(self) -> None:
        super(MoreInfo, self).__init__()
        self.window_point = None
        self.start_point = None
        self.is_moving = None
        self.setupUi(self)

        self.small.clicked.connect(self.showMinimized)
        self.exit.clicked.connect(self.close)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(self.width(), self.height())

    def mousePressEvent(self, e) -> None:
        if e.button() == Qt.LeftButton:
            self.is_moving = True
            self.start_point = e.globalPos()
            self.window_point = self.frameGeometry().topLeft()

    def mouseMoveEvent(self, e) -> None:
        if self.is_moving:
            repos = e.globalPos() - self.start_point
            self.move(self.window_point + repos)

    def mouseReleaseEvent(self, e) -> None:
        self.is_moving = False

    def start_(self, word) -> None:
        # 复数 现在分词 过去分词 三单 一过 比较级 最高级
        more_text = {"s": self.tr("plural"), "i": self.tr("present participle"), "d": self.tr("past participle"),
                     "3": self.tr("Three singles"), "p": self.tr("Once passed"), "t": self.tr("comparative"),
                     "r": self.tr("superlative")}
        new_exchange = {}
        self.textBrowser_ex.clear()
        self.english_tr.clear()

        for words in e_.main_idea(word):
            if len(word) > 4:
                for key, var in words[4].items():
                    new_exchange[more_text[key]] = var
                self.english_tr.setText(words[2])
        for key, var in new_exchange.items():
            self.textBrowser_ex.append(f"""
        <strong>
        <font size="4" family={config["font-family"]}>{key}</font></strong>:<strong><font size="3" family={config["font-family"]}>{var}</font></strong> """)


class playInfo(QThread):
    def __init__(self, text) -> None:
        super().__init__()
        self.text = text

    def run(self) -> None:
        winsound.PlaySound(self.text, winsound.SND_ALIAS)


class MQMessageBox(QDialog, Ui_Dialog):
    def __init__(self) -> None:
        super().__init__()
        self._startPos = None
        self._isTracking = None
        self._endPos = None

        self.is_OK = False

        self.setupUi(self)
        self.setWindowFlag(Qt.FramelessWindowHint)

        self.buttonBox.accepted.connect(self.OK)
        self.buttonBox.rejected.connect(self.NO)

        self.pushButton.clicked.connect(self.close)

        self.sound_ = None

    def OK(self):
        self.is_OK = True

    def NO(self):
        self.is_OK = False

    def mouseMoveEvent(self, a0: QMouseEvent) -> None:
        if self._startPos:
            self._endPos = a0.pos() - self._startPos
            self.move(self.pos() + self._endPos)

    def mousePressEvent(self, a0: QMouseEvent) -> None:
        if self.childAt(a0.pos().x(), a0.pos().y()).objectName() == "label":
            if a0.button() == Qt.LeftButton:
                self._isTracking = True
                self._startPos = QPoint(a0.x(), a0.y())

    def mouseReleaseEvent(self, a0: QMouseEvent) -> None:
        if a0.button() == Qt.LeftButton:
            self._isTracking = False
            self._startPos = None
            self._endPos = None

    def mouseDoubleClickEvent(self, a0: QMouseEvent) -> None:
        if self.childAt(a0.pos().x(), a0.pos().y()).objectName() == "label":
            if a0.button() == Qt.LeftButton:
                self.showNormal()

    def Play(self, title: str, text: str, type_sound: str, mark: bool = False) -> bool:
        self.close()
        self.setWindowTitle(title)
        if mark:
            infos.show()
            infos.textBrowser.setHtml(text)
        else:
            self.sound_ = playInfo(type_sound)
            self.sound_.start()
            self.textBrowser.setHtml(f"""<font size="10">{text}</font>""")
            self.show()
            self.exec_()
        return self.is_OK

    def info(self, title: str, text: str) -> bool:
        return self.Play(title, text, "SystemAsterisk")


class info_(QFrame, info.Ui_info):
    def __init__(self) -> None:
        super().__init__()
        self._startPos = None
        self._isTracking = None
        self._endPos = None

        self.setupUi(self)

        self.exit_2.clicked.connect(self.showNormal)
        self.exit.clicked.connect(self.close)

        self.setWindowFlag(Qt.FramelessWindowHint)

    def mouseMoveEvent(self, a0: QMouseEvent) -> None:
        if self._startPos:
            self._endPos = a0.pos() - self._startPos
            self.move(self.pos() + self._endPos)

    def mousePressEvent(self, a0: QMouseEvent) -> None:
        if self.childAt(a0.pos().x(), a0.pos().y()).objectName() == "widget":
            if a0.button() == Qt.LeftButton:
                self._isTracking = True
                self._startPos = QPoint(a0.x(), a0.y())

    def mouseReleaseEvent(self, a0: QMouseEvent) -> None:
        if a0.button() == Qt.LeftButton:
            self._isTracking = False
            self._startPos = None
            self._endPos = None

    def mouseDoubleClickEvent(self, a0: QMouseEvent) -> None:
        if self.childAt(a0.pos().x(), a0.pos().y()).objectName() == "widget":
            if a0.button() == Qt.LeftButton:
                self.showNormal()


def connects() -> bool:
    return True


class Many(QThread):
    def __init__(self, parent=None) -> None:
        super(Many, self).__init__(parent)
        self.t = dict()

    def run(self) -> None:
        if connects():
            req = get("https://v1.hitokoto.cn/", verify=False)
            req.encoding = "UTF-8"
            self.t = json.loads(req.text)
        else:
            MessageBox.info(self.tr("No connected to the Internet"), self.tr(
                "It has been detected that you are not connected to the Internet, please try again after connecting "
                "to the Internet"))


class revolve_MUSIC(QObject):
    def __init__(self) -> None:
        super().__init__()
        self.args = None
        self.anim = None

        pixmap_1 = QPixmap(':/English_tools/music.png')
        scaledPixmap_1 = pixmap_1.scaled(150, 150)
        self.animation()
        self.admin = QGraphicsPixmapItem(scaledPixmap_1)
        self.admin.setTransformOriginPoint(75, 75)
        self.admin.setPos(0, 30)

    def _set_rotation(self, degree) -> None:
        self.admin.setRotation(degree)

    def animation(self) -> None:
        self.args = {
            'duration': config["Rotation-speed"],
            'startValue': 0,
            'endValue': 360,
            'loopCount': -1
        }
        self.anim = QPropertyAnimation(self, b"rotation", **self.args)

    rotation = pyqtProperty(int, fset=_set_rotation)


class MUSIC_(QFrame, MUSIC.Ui_MUSIC_PL):
    def __init__(self) -> None:
        super().__init__()

        self._endPos = None
        self._startPos = None
        self._isTracking = None
        self.setupUi(self)
        self.block = revolve_MUSIC()

        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(-10, 0, 170, 210)
        self.scene.addItem(self.block.admin)

        self.setWindowFlag(Qt.FramelessWindowHint)

        self.graphicsView.setScene(self.scene)

        self.player = QMediaPlayer()

        self.icon2 = QIcon()
        self.icon2.addPixmap(QPixmap(":/windows/play.png"), QIcon.Normal, QIcon.Off)
        self.icon = QIcon()
        self.icon.addPixmap(QPixmap(":/windows/play_stop.png"), QIcon.Normal, QIcon.Off)

        self.listWidget.clicked.connect(lambda: self.play(self.listWidget.currentIndex().data()))

        self.stop.clicked.connect(self.stop_video)
        self.exit_2.clicked.connect(self.showNormal)
        self.exit.clicked.connect(self.close)

        self.player.stateChanged.connect(lambda: self.block.anim.stop())
        self.file.clicked.connect(self.file_)
        self.dir.clicked.connect(self.dir_)

    def file_(self) -> None:
        # 音频文件 选择音频文件
        file_choose = \
            get_file_search(audio_type, parent=self, fileCheckType=[self.tr('...')],
                            title=self.tr("Select the audio file"))[0]
        if file_choose != "":
            self.play(file_choose)

    def dir_(self) -> None:
        # 选择音频文件夹 选择音频文件夹
        file_choose = \
            get_file_search(audio_type, mode=3, parent=self, fileCheckType=[self.tr('Audio files')],
                            title=self.tr("Select the Audio folder"))
        self.dirs(file_choose)

    def dirs(self, file_choose) -> None:
        for file_path, dir_names, file_names in os.walk(file_choose):
            for filename in file_names:
                if get_splits(filename) in audio_type:
                    self.listWidget.addItem(os.path.join(file_path, filename))
        self.play(music_path + "lucky.mp3")

    def play(self, file_: str) -> None:
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(file_)))
        self.listWidget.addItem(file_)
        self.Deduplication()
        self.show()
        self.stop_video()

    def Deduplication(self) -> None:
        unique_items = []
        for i in range(self.listWidget.count()):
            item = self.listWidget.item(i)
            if item.text() not in unique_items:
                unique_items.append(item.text())
        self.listWidget.clear()
        for item_text in unique_items:
            self.listWidget.addItem(item_text)

    def stop_video(self) -> None:
        if self.player.state() == 1:
            self.stop.setIcon(self.icon)
            self.player.pause()
            self.block.anim.stop()
        else:
            self.stop.setIcon(self.icon2)
            self.player.play()
            self.block.anim.start()

    def closeEvent(self, a0: QCloseEvent) -> None:
        self.player.stop()
        a0.accept()

    def mouseMoveEvent(self, a0: QMouseEvent) -> None:
        if self._startPos:
            self._endPos = a0.pos() - self._startPos
            self.move(self.pos() + self._endPos)

    def mousePressEvent(self, a0: QMouseEvent) -> None:
        if self.childAt(a0.pos().x(), a0.pos().y()).objectName() == "background":
            if a0.button() == Qt.LeftButton:
                self._isTracking = True
                self._startPos = QPoint(a0.x(), a0.y())

    def mouseReleaseEvent(self, a0: QMouseEvent) -> None:
        if a0.button() == Qt.LeftButton:
            self._isTracking = False
            self._startPos = None
            self._endPos = None

    def mouseDoubleClickEvent(self, a0: QMouseEvent) -> None:
        if self.childAt(a0.pos().x(), a0.pos().y()).objectName() == "background":
            if a0.button() == Qt.LeftButton:
                self.showNormal()


class Video_play(QDialog, Video.Ui_Dialog):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)

        self._startPos = None
        self._isTracking = None
        self._endPos = None

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setFixedSize(self.width(), self.height())
        self.small.clicked.connect(self.showNormal)
        self.exit.clicked.connect(self.close)
        self.horizontalSlider.sliderMoved.connect(self.updatePosition)

        self.player = QMediaPlayer()
        self.player.durationChanged.connect(self.getDuration)
        self.player.positionChanged.connect(self.getPosition)
        self.stop.setIconSize(QSize(30, 30))
        self.stop.clicked.connect(self.stop_video)
        self.player.setVideoOutput(self.widget)

        self.icon2 = QIcon()
        self.icon2.addPixmap(QPixmap(":/windows/play.png"), QIcon.Normal, QIcon.Off)
        self.icon = QIcon()
        self.icon.addPixmap(QPixmap(":/windows/play_stop.png"), QIcon.Normal, QIcon.Off)

    def ffmpeg_play(self, file_) -> None:
        self.show()
        self.player.setMedia(QMediaContent(QUrl(file_)))
        self.exec_()

    def mouseMoveEvent(self, a0: QMouseEvent) -> None:
        if self._startPos:
            self._endPos = a0.pos() - self._startPos
            self.move(self.pos() + self._endPos)

    def mousePressEvent(self, a0: QMouseEvent) -> None:
        if self.childAt(a0.pos().x(), a0.pos().y()).objectName() == "background":
            if a0.button() == Qt.LeftButton:
                self._isTracking = True
                self._startPos = QPoint(a0.x(), a0.y())

    def mouseReleaseEvent(self, a0: QMouseEvent) -> None:
        if a0.button() == Qt.LeftButton:
            self._isTracking = False
            self._startPos = None
            self._endPos = None

    def mouseDoubleClickEvent(self, a0: QMouseEvent) -> None:
        if self.childAt(a0.pos().x(), a0.pos().y()).objectName() == "background":
            if a0.button() == Qt.LeftButton:
                self.showNormal()

    def closeEvent(self, a0: QCloseEvent) -> None:
        self.player.stop()
        a0.accept()

    def stop_video(self) -> None:
        if self.player.state() == 1:
            self.stop.setIcon(self.icon)
            self.player.pause()
        else:
            self.stop.setIcon(self.icon2)
            self.player.play()

    def getDuration(self, d) -> None:
        self.horizontalSlider.setRange(0, d)
        self.horizontalSlider.setEnabled(True)
        self.displayTime(d)

    def getPosition(self, p) -> None:
        self.horizontalSlider.setValue(p)
        self.displayTime(self.horizontalSlider.maximum() - p)

    def displayTime(self, ms) -> None:
        minutes = int(ms / 60000)
        seconds = int((ms - minutes * 60000) / 1000)
        self.lab_duration.setText(f'{minutes}:{seconds}')

    def updatePosition(self, v) -> None:
        self.player.setPosition(v)
        self.displayTime(self.horizontalSlider.maximum() - v)


class Main(QFrame, Mainwindow.Ui_Mainwindow):
    def __init__(self) -> None:
        super().__init__()
        # 无边框
        self._startPos_setting = None
        self._startPos_music = None
        self._startPos_file_sear = None
        self.is_img = None
        self.filePath = None
        self._startPos = None
        self._isTracking = None
        self._endPos = None
        self.word__number = 0
        self.word__ = None
        self.music_ = None
        self._word = None

        self.TEMP = None

        self.setupUi(self)

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.exit_2.clicked.connect(self.showNormal)
        self.exit.clicked.connect(self.queryExit)
        self.file_dir_search_start.clicked.connect(self.file_search_start_fun)

        self.start_mp = MQLineEdit(self.groupBox_4)
        self.start_mp.setGeometry(QRect(10, 36, 251, 21))
        self.start_mp.setObjectName("start_mp")
        self.setTabOrder(self.next, self.start_mp)
        self.setTabOrder(self.start_mp, self.set)

        self.file_tuo = MQLabel(self.groupBox)
        self.file_tuo.setGeometry(QRect(342, 10, 161, 81))
        self.file_tuo.setPixmap(QPixmap(":/windows/file_tuo_en.png"))
        self.file_tuo.setObjectName("file_tuo")
        self.file_tuo.setScaledContents(True)
        self.Inspirational_ = QTimer()
        self.Inspirational_.timeout.connect(self.play_Inspirational)

        self.start_work.clicked.connect(self.start_Conver)

        self.leaen_english.clicked.connect(lambda: self.functionality.setCurrentIndex(1))
        self.en_system.clicked.connect(lambda: self.functionality.setCurrentIndex(2))
        self.conver_.clicked.connect(lambda: self.functionality.setCurrentIndex(3))
        self.reili.clicked.connect(lambda: self.functionality.setCurrentIndex(0))
        self.File_search.clicked.connect(lambda: self.functionality.setCurrentIndex(4))

        self.next.clicked.connect(self.word_)
        self.next_.clicked.connect(self.word_)
        self.last.clicked.connect(lambda: self.word_(mode=True))
        self.last_.clicked.connect(lambda: self.word_(mode=True))
        self.sound.clicked.connect(self.music)

        copys = QApplication.clipboard()
        self.copy.clicked.connect(lambda: copys.setText(self.finish_text_2.toPlainText()))

        self.start_Custom_2.clicked.connect(self.start_word_)

        self.start_word.clicked.connect(lambda: self.play_worf())
        self.music_play_.clicked.connect(lambda: mm.dirs(music_path))
        self.start.clicked.connect(self.start_en)
        self.read_disposition.clicked.connect(self.read_configs)
        self.start_mp.textChanged.connect(self.check_long_name)
        self.finish_mpp.currentTextChanged.connect(self.search_finish_name)
        self.trans = QTranslator(app)
        self.change_language(language)
        self.File_search.clicked.connect(lambda: file_searchs.show())

        self.img_type = ["jpg", "jpeg", "png", "gif", "bmp", "tiff", "ai", "cdr", "eps"]
        self.text_type = ["txt", "log", "json", "xml", "py", "cpp", "c", "h", "cs"]
        # 文本类型 图像类型
        _, __ = self.tr("Text type"), self.tr("Image type")

        # 选择加密文件 选择解密文件
        self.file_search_en.clicked.connect(lambda: self.en_text.setText(
            get_file_search(self.text_type,
                            self.img_type, parent=self,
                            fileCheckType=[_, __], title=self.tr("Select Encrypt File"),
                            allType=True)[
                0]))
        self.file_search_dn.clicked.connect(lambda: self.dn_text.setText(
            get_file_search(self.text_type, self.img_type, parent=self,
                            fileCheckType=[_, __], title=self.tr("Select Decrypt File"),
                            allType=True)[
                0]))
        self.source_conver_type = None
        self.commandLinkButton.clicked.connect(lambda: webbrowser.open("https://599575461.github.io/"))
        self.information.clicked.connect(
            lambda: MessageBox.Play("", file.read_qss_file("README.html"), "SystemAsterisk", mark=True))

        self.en_text = MQLineEdit(self.layoutWidget)

        self.en_text.setObjectName("en_text")
        self.horizontalLayout_2.addWidget(self.en_text)

        self.dn_text = MQLineEdit(self.layoutWidget1)
        self.dn_text.setObjectName("dn_text")
        self.horizontalLayout_4.addWidget(self.dn_text)

        shutil.copyfile(f"..\\music\\lucky.mp3", music_path + "lucky.mp3")
        shutil.copyfile(f"..\\music\\So Cold.mp3", music_path + "So Cold.mp3")

        self.Inspirational_.start(int(config["up_time"]))

    # 英语选框输入
    def start_word_(self) -> None:
        self.word__ = self.Custom_words.text()
        self.word_(play=True)

    # 励志短语设置
    def play_Inspirational(self) -> None:
        many.start()
        if len(many.t) != 0:
            self.Inspirational.setMarkdown(f"""## "{many.t["hitokoto"][:-1]}"\n 
                    From {many.t["from"]}--{many.t["creator"]}
                    """)

    def search_finish_name(self) -> None:
        new_path = f"{os.path.split(self.start_mp.text())[0]}.{self.finish_mpp.currentText()}"
        self.finish_mp.setText(new_path)

    # 拖放文件时修改选框后缀
    def check_long_name(self) -> None:
        """

    :return: None
    """
        if os.path.isfile(self.start_mp.text()):
            if get_splits(self.start_mp.text()) in audio_type:
                for audio in audio_type:
                    self.finish_mpp.addItem(audio)
            else:
                for video in video_type:
                    self.finish_mpp.addItem(video)

    def read_configs(self) -> None:
        # 配置文件 读取配置文件
        fileName_choose = \
            get_file_search(['json'], parent=self, fileCheckType=[self.tr("Configuration file")],
                            title=self.tr("Read "
                                          "the "
                                          "configuration file"))[
                0]
        if fileName_choose != '':
            with open(fileName_choose, "r") as w:
                config_conver = json.load(w)
            self.start_mp.setText(config_conver["file_source"])
            self.finish_mp.setText(config_conver["finish_source"])
            self.save_disposition.setChecked(config_conver["is_save"])
            self.start_same_time.setChecked(config_conver["is_open_now"])
            self.del_log.setChecked(config_conver["is_del_log"])

    # 语言修改
    def change_language(self, text: str) -> None:
        _app = QApplication.instance()

        if text == 'English':
            _app.removeTranslator(self.trans)
            if language != text:
                sett.close()
            self.file_tuo.setPixmap(QPixmap(":/windows/file_tuo_en.png"))

        if text == '简体中文':
            self.trans.load("..\\QM\\Mainwindow_.qm")
            _app.installTranslator(self.trans)
            # 成功 重启以启动以更新界面
            if language != text:
                sett.close()
            self.file_tuo.setPixmap(QPixmap(":/windows/file_tuo.png"))

        self.update()
        self.retranslateUi(self)

    # 提示需要重启
    def succeed(self) -> None:
        if MessageBox.info(self.tr("succeed"), self.tr("The settings are saved successfully Reboot to launch to "
                                                       "update the interface")):
            rebot()

    # 开始工作
    def start_en(self) -> None:

        dn_text_finish = None
        # 获取要加密的信息
        en_text = self.en_text.text()
        # 获得要解密的信息
        dn_text = self.dn_text.text()

        # 如果说两个输入框都是空的
        if en_text == "" and dn_text == "":
            # 没有内容 您未输入任何字符\n您可以输入 /文件/文本/目录
            MessageBox.info(self.tr('There is no content'),
                            self.tr("You did not enter any characters\nYou can enter "
                                    "/file/text/directory"))
        elif en_text != "" and dn_text != "":
            # 不能同时进行 不能同时进行加密和解密
            MessageBox.info(self.tr('It cannot be done at the same time'),
                            self.tr("You cannot encrypt and decrypt at "
                                    "the same time"))
        elif len(en_text) >= 1000 or len(dn_text) >= 1000:
            # 太长 文本过于长\n建议写入txt文件
            MessageBox.info(self.tr('Too long'),
                            self.tr("Text is too long\nIt is recommended to write to a txt file"))
        else:
            # 实例化密码系统
            e = EDNCrypto()
            # 提示消息
            message = ''
            # 获得的文本信息
            text = ''
            # 如果加密的框不是空的
            if en_text != "":
                # 如果输入的是文件
                if os.path.isfile(en_text):
                    # 读取文件
                    try:
                        if get_splits(os.path.split(dn_text)[1]) in self.img_type:
                            e.encrypt_decrypt_image(dn_text)
                            self.is_img = True
                        else:
                            with open(en_text, 'r', encoding='UTF-8') as f:
                                # 将获得信息进行加密
                                text = f.read()
                                en_text_finish = str(e.en(text))
                    except FileNotFoundError:
                        # 未找到文件
                        message += self.tr('File not found\n')
                    else:
                        # 成功加密
                        message += self.tr('Successful encryption\n')
                        # 将浏览文本的窗口设置加密文本
                        if not self.is_img:
                            self.finish_text_2.setText(en_text_finish)
                            with open(en_text, 'w', encoding='UTF-8') as f:
                                # 写入加密的文本
                                f.write(en_text_finish)
                        else:
                            # message添加成功信息
                            # 成功替换文本
                            message += self.tr('Text replacement successfully\n')
                # 如果输入的是目录
                elif os.path.isdir(en_text):
                    # 遍历目录下所有文件
                    for filepath, dir_names, filenames in os.walk(en_text):
                        for filename in filenames:
                            # 拼接文件名和路径
                            _path = os.path.join(filepath, filename)

                            if get_splits(filename) in self.img_type:
                                e.encrypt_decrypt_image(_path)
                            else:
                                # 分别打开文件
                                with open(_path, 'w', encoding='UTF-8') as f:
                                    # 写入加密信息
                                    f.write(e.en(text))
                            # message添加成功信息
                            # 已将 加密
                            message += self.tr('Converted') + _path + self.tr('encrypt\n')

                # 如果是纯文本
                else:
                    # 设置已经加密好的信息
                    en_text_finish = str(e.en(en_text))
                    # 将浏览文本的窗口设置加密文本
                    self.finish_text_2.setText(en_text_finish)
                    # message添加成功信息
                    message += self.tr('The ciphertext succeeded\n')
            # 如果解密的框不是空的
            if dn_text != "":
                # 如果输入的是文件
                if os.path.isfile(dn_text):
                    try:
                        if get_splits(os.path.split(dn_text)[1]) in self.img_type:
                            e.encrypt_decrypt_image(dn_text)
                            self.is_img = True
                        else:
                            with open(dn_text, 'r', encoding='UTF-8') as f:
                                # 将获得信息进行解密
                                dn_text_finish = e.dn(f.read())
                    except ValueError:
                        # 输入格式不正确
                        message += self.tr('The input format is incorrect\n')
                    # 将浏览文本的窗口设置解密文本
                    else:
                        if not self.is_img:
                            self.finish_text_2.setText(dn_text_finish)
                            try:
                                with open(dn_text, 'w', encoding='UTF-8') as f:
                                    # 写入解密的文本
                                    f.write(dn_text_finish)
                            except ValueError:
                                # 输入格式不正确
                                message += self.tr('The input format is incorrect\n')
                            # message添加成功信息
                        # 成功替换文本
                        message += self.tr('Text replacement successfully\n')
                # 如果输入的是目录
                elif os.path.isdir(dn_text):
                    for filepath, dir_names, filenames in os.walk(dn_text):
                        for filename in filenames:
                            # 拼接文件名和路径
                            _path = os.path.join(filepath, filename)
                            if get_splits(filename) in self.img_type:
                                e.encrypt_decrypt_image(_path)
                            else:
                                # 分别打开文件
                                with open(_path, 'w', encoding='UTF-8') as f:
                                    # 写入解密信息
                                    f.write(e.dn(literal_eval(text)))
                                # message添加成功信息
                            # 已将 解密
                            message += self.tr('Converted') + _path + self.tr('decrypt\n')
                # 如果是纯文本
                else:
                    # 设置已经解密好的信息
                    try:
                        dn_text_finish = e.dn(dn_text)
                    except ValueError:
                        # 输入格式不正确
                        message += self.tr('The input format is incorrect\n')
                    except TypeError:
                        # 输入格式不正确
                        message += self.tr('The input format is incorrect\n')
                    else:
                        # 将浏览文本的窗口设置解密文本
                        self.finish_text_2.setText(dn_text_finish)
                        # 解密文本成功
                        message += self.tr('Decrypting the text successfully')
            # 弹出窗口提示
            MessageBox.info('信息', message)

    def play_worf(self) -> None:
        update_thread.start()
        update_thread.text.connect(self.bar__)
        self.start_word.setVisible(False)

    def bar__(self, word) -> None:
        MessageBox.info(self.tr("Succeed!"), self.tr("Initialization dictionary successful!"))
        main_window.word_(word___=word, first=True)

    def word_(self, word___=None, mode=False, first=False, play=False) -> None:
        if mode:
            self.word__number -= 2
        if first:
            self.word__ = 'object'
            self._word = word___
        elif not play:
            self.word__ = self._word[self.word__number]
        try:
            try:
                self.textBrowser.clear()
                for i in e_.main_idea(self.word__):
                    # <strong>单词:</strong>
                    # <strong>音标:</strong>
                    # <strong>解释:</strong>
                    self.textBrowser.append(self.tr("<strong>Word:</strong>") + i[0])
                    self.textBrowser.append(self.tr("<strong>Phonetic transcription:</strong>") + i[1])
                    self.textBrowser.append(self.tr("<strong>Explanation:</strong>") + i[3])
                    break
                self.english_words.setText(self.word__)
                self.more_info()
                self.word__number += 1
            except TypeError:
                # 出现错误 词库损失
                MessageBox.info(self.tr('An error occurred'), self.tr('Thesaurus loss') + self.word__)
                self.word__number += 1
        except AttributeError:
            self.__play()
        except TypeError:
            self.__play()
        except IndexError:
            self.word__number = 0

    def __play(self) -> None:
        # 请稍等 正在初始化词库
        MessageBox.info(self.tr("Please wait"), self.tr("Initializing thesaurus"))

    def more_info(self) -> None:
        more_inf.start_(self.word__)
        more_inf.show()

    def music(self) -> None:
        _path = os.path.join(f"{english_path + self.word__}.mp3")

        self.music_ = Music(_path)
        self.music_.start()

    def start_Conver(self) -> None:
        Conver_ = Conver(self.start_mp.text(), self.finish_mp.text(), is_save=self.save_disposition.isChecked(),
                         is_open_now=self.start_same_time.isChecked(), is_del_log=self.del_log.isChecked())
        Conver_.run()

    def file_search_start_fun(self) -> None:
        # 音频文件 视频文件 选择文件
        fileName_choose = get_file_search(audio_type, video_type, parent=self,
                                          fileCheckType=[self.tr("Audio files"), self.tr("Video files")],
                                          title=self.tr("Select the file"))
        self.start_mp.setText(fileName_choose[0])

    # 退出
    def queryExit(self, mode=False):
        # 退出? 你确认退出?
        _ = MessageBox.info(self.tr("Quit?"), self.tr("Do you confirm your exit?"))
        if _ and not mode:
            sett.exit_()
            QCoreApplication.instance().exit()
        if _ and mode:
            sett.exit_()
            return True

    def closeEvent(self, a0: QCloseEvent) -> None:
        if self.queryExit(mode=False):
            a0.accept()

    # 鼠标移动事件
    def mouseMoveEvent(self, a0: QMouseEvent) -> None:
        if self._startPos:
            if config["Stitching-window"]:

                if mm.isVisible():
                    mm.move(eval(config["music_window"][0])(config["music_window"][1], mm))
                if file_searchs.isVisible():
                    file_searchs.move(eval(config["file_window"][0])(config["file_window"][1], file_searchs))
                if sett.isVisible():
                    sett.move(eval(config["set_window"][0])(config["set_window"][1], sett))

            self.move(self.pos() + (a0.pos() - self._startPos))

    # 鼠标按下事件
    def mousePressEvent(self, a0: QMouseEvent) -> None:
        if self.childAt(a0.pos().x(), a0.pos().y()).objectName() == "label_12":
            if a0.button() == Qt.LeftButton:
                self._isTracking = True
                self._startPos = QPoint(a0.x(), a0.y())

    # 松开
    def mouseReleaseEvent(self, a0: QMouseEvent) -> None:
        if a0.button() == Qt.LeftButton:
            self._isTracking = False
            self._startPos = None
            self._endPos = None

    def mouseDoubleClickEvent(self, a0: QMouseEvent) -> None:
        if self.childAt(a0.pos().x(), a0.pos().y()).objectName() == "label":
            if a0.button() == Qt.LeftButton:
                self.showNormal()
                file_searchs.showNormal()
                sett.showNormal()
                mm.showNormal()

    def dragEnterEvent(self, e) -> None:
        self.file_tuo.setVisible(True)
        if e.mimeData().hasText():
            e.accept()
        else:
            e.ignore()

    def dragLeaveEvent(self, a0) -> None:
        self.file_tuo.setVisible(False)

    def dropEvent(self, e) -> None:
        self.file_tuo.setVisible(False)
        self.filePath = e.mimeData().text().split('\n')[0].replace(
            'file:///', '', 1)

    @property
    def startPos_setting(self):
        return self._startPos_setting


class BarThread(QThread):
    text = pyqtSignal(list)

    def run(self) -> None:
        # 开一个线程解压ecdict.7z
        with open("words_alpha.txt", 'r', encoding='UTF-8') as w:
            a = w.read()
        if not os.path.isfile(English_dict):
            os.system(f"7z.exe x info/Box/English/ecdict.7z -p599575461 -o{english_path} -y")
        e_.start()
        self.text.emit(a.split('\n'))


class Music(QThread):

    def __init__(self, path__) -> None:
        QThread.__init__(self)
        self.path = path__

    def run(self) -> None:
        playsound(self.path)


class setting_(QFrame, setting.Ui_Settings):
    def __init__(self) -> None:
        super().__init__()
        self.trans = None
        self._endPos = None
        self._startPos = None
        self._isTracking = None

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setupUi(self)

        for i in ['English', '简体中文']:
            self.comboBox.addItem(i)
        self.side = [self.tr('topmost'), self.tr('below'), self.tr("left"), self.tr('right')]

        # 上面 下面 左面 右面
        for i in self.side:
            self.comboBox_2.addItem(i)
            self.comboBox_3.addItem(i)
            self.comboBox_4.addItem(i)

        self.pushButton.clicked.connect(self.re_config)
        self.init()

    # 设置初始化
    def init(self) -> None:
        self.exits.clicked.connect(self.close)
        self.comboBox.currentTextChanged.connect(lambda: main_window.change_language(self.comboBox.currentText()))
        self.trans = QTranslator(self)
        self.comboBox.setCurrentText(language)
        self.lineEdit.setText(english_path)
        self.lineEdit_2.setText(music_path)
        self.textEdit.setText(" ".join(audio_type).upper())
        self.textEdit_2.setText(" ".join(video_type).upper())
        self.spinBox.setValue(int(mm.block.args["duration"]))
        self.fontComboBox.setCurrentText(config["font-family"])
        self.checkBox.setChecked(config["Stitching-window"])
        self.spinBox_2.setValue(config["up_time"])

        self.comboBox_2.setCurrentText(config["set_window"][0])
        self.set_coor.setValue(config["set_window"][1])
        self.comboBox_3.setCurrentText(config["file_window"][0])
        self.File_coor.setValue(config["file_window"][1])
        self.comboBox_4.setCurrentText(config["music_window"][0])
        self.spinBox_3.setValue(config["music_window"][1])

    def re_config(self) -> None:
        file.write_json_file("json/config.json", file.read_json_file("json/config_re.json"))

        global config
        config = file.read_json_file("json/config.json")

        self.init()

        main_window.succeed()

    def exit_(self) -> None:
        languages = self.comboBox.currentText()
        if self.lineEdit.text()[-1] == "\\":
            self.lineEdit.setText(self.lineEdit.text()[:-1])
        file.write_json_file("..\\json\\config.json", {
            "Language": f"{languages}",
            "English_path": f"{self.lineEdit.text()}",
            "MUSIC": f"{self.lineEdit_2.text()}",
            "English_dict": self.lineEdit.text() + "\\ecdict.csv",
            "audio_type": self.textEdit.toPlainText().lower().split(" "),
            "video_type": self.textEdit_2.toPlainText().lower().split(" "),
            "font-family": self.fontComboBox.currentText(),
            "Rotation-speed": int(self.spinBox.text()),
            "Stitching-window": self.checkBox.isChecked(),
            "up_time": int(self.spinBox_2.text()),
            "set_window": [self.comboBox_2.currentText(), int(self.set_coor.text())],
            "file_window": [self.comboBox_3.currentText(), int(self.File_coor.text())],
            "music_window": [self.comboBox_4.currentText(), int(self.spinBox_3.text())],
        })

    def closeEvent(self, a0: QCloseEvent, main=False) -> None:
        self.exit_()
        main_window.succeed()

    def mouseMoveEvent(self, a0: QMouseEvent) -> None:
        if self._startPos:
            self._endPos = a0.pos() - self._startPos
            self.move(self.pos() + self._endPos)

    def mousePressEvent(self, a0: QMouseEvent) -> None:
        if self.childAt(a0.pos().x(), a0.pos().y()).objectName() == "label_2":
            if a0.button() == Qt.LeftButton:
                self._isTracking = True
                self._startPos = QPoint(a0.x(), a0.y())

    def mouseReleaseEvent(self, a0: QMouseEvent) -> None:
        if a0.button() == Qt.LeftButton:
            self._isTracking = False
            self._startPos = None
            self._endPos = None

    def mouseDoubleClickEvent(self, a0: QMouseEvent) -> None:
        if self.childAt(a0.pos().x(), a0.pos().y()).objectName() == "label_2":
            if a0.button() == Qt.LeftButton:
                self.showNormal()


def get_splits(filename: str) -> str:
    """
    返回文件后缀
    :param filename: 文件名
    :return: 后缀
    """
    return os.path.splitext(filename)[1].replace(".", "")


def get_file_search(*args: list, fileCheckType: list = None, title: str = "文件", mode: int = 2,
                    allType: bool = False, parent=None) -> Union[tuple[str, str], str]:
    """
    :param parent:
    :param args: 更多文件后缀 类型与fileCheckType对应
    :param fileCheckType: 对应后缀类型
    :param title: 对话框标题
    :param mode: 对话框模式
    :param allType: 是否用全后缀
    :return:
    """
    GET_types = ""
    if fileCheckType and len(args) > 0:
        for introduce, arg in zip(fileCheckType, args):
            for i in arg:
                GET_types += f"{introduce}(*.{i});;"
    if allType:
        GET_types += "All File(*.)"
    else:
        GET_types = GET_types[:-2]

    if mode == 1:
        fileName_choose, filetype = QFileDialog.getSaveFileName(parent, title, cwd,
                                                                GET_types)
        if fileName_choose != "" or fileName_choose is not None:
            return fileName_choose, filetype

    if mode == 2:
        fileName_choose, filetype = QFileDialog.getOpenFileName(parent, title, cwd,
                                                                GET_types)
        if fileName_choose != "" or fileName_choose is not None:
            return fileName_choose, filetype

    if mode == 3:
        fileName_choose = QFileDialog.getExistingDirectory(parent, title, cwd, )
        if fileName_choose != "" or fileName_choose is not None:
            return fileName_choose


def rebot() -> None:
    """
    重启
    :return: None
    """
    pass
    # app_path = QCoreApplication.applicationFilePath()
    # process = QProcess()
    # process.startDetached(app_path)
    # QCoreApplication.quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    cwd = os.getcwd()
    file = Losder.Losder()
    config = file.read_json_file(f"..\\json\\config.json")

    language = config["Language"]
    english_path = config["English_path"]
    music_path = config["MUSIC"]
    English_dict = config["English_dict"]
    audio_type = config["audio_type"]
    video_type = config["video_type"]

    # 设置QSS
    main_qss = file.read_qss_file(f"..\\QSS\\Mainwindow.qss") % config["font-family"]
    app.setStyleSheet(main_qss)

    # 检测目录
    if english_path[-1] != "\\":
        english_path += "\\"
    if not os.path.isdir(english_path):
        os.mkdir(english_path)
    if not os.path.isdir(english_path + "MUSIC\\"):
        os.mkdir(english_path + "MUSIC\\")

    MessageBox = MQMessageBox()
    mm = MUSIC_()
    infos = info_()
    many = Many()
    update_thread = BarThread()
    more_inf = MoreInfo()
    e_ = English(english_path, English_dict)
    videos = Video_play()
    main_window = Main()
    sett = setting_()
    file_searchs = Searchs()

    main_window.set.clicked.connect(sett.show)
    main_window.show()

    urllib3.disable_warnings()
    sys.exit(app.exec_())
