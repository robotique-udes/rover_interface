
import os
import rospkg
import rospy
from rospkg import RosPack
from python_qt_binding import loadUi
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QShortcut, QSlider, QAbstractSlider, QSpinBox
# from rover_control.msg import CamCommand

class RoverCamControlWidget(QtWidgets.QWidget):

    def __init__(self):
        super(RoverCamControlWidget, self).__init__()

        ui_file = os.path.join(rospkg.RosPack().get_path('rover_cam_control'), 'resource', 'cam_control.ui')
        loadUi(ui_file, self)
        self.setObjectName('RoverCamControlWidget')

        self.is_active = False

        self.cam_horizontal_pos = 0
        self.cam_vertical_pos = 0

        self.cam_horizontal_pos_signal = 0
        self.cam_vertical_pos_signal = 0

        self.init_fields()

        self.cam_left_btn.clicked.connect(self.cam_left_btn_callback)
        self.cam_right_btn.clicked.connect(self.cam_right_btn_callback)
        self.cam_up_btn.clicked.connect(self.cam_up_btn_callback)
        self.cam_down_btn.clicked.connect(self.cam_down_btn_callback)
        self.cam_update_btn.clicked.connect(self.update_command)
        self.cam_reset_btn.clicked.connect(self.init_fields)

        self.cam_keyboard_check_box.clicked[bool].connect(self.cam_keyboard_check_box_callback)
        
        self.cam_left_shortcut = QShortcut(QKeySequence(self.tr("G", "File|Open")), self)
        self.cam_right_shortcut = QShortcut(QKeySequence(self.tr("J", "File|Open")), self)
        self.cam_up_shortcut = QShortcut(QKeySequence(self.tr("Y", "File|Open")), self)
        self.cam_down_shortcut = QShortcut(QKeySequence(self.tr("H", "File|Open")), self)
        self.cam_update_shortcut = QShortcut(QKeySequence(self.tr("B", "File|Open")), self)

        self.cam_left_shortcut.activated.connect(self.cam_left_btn.animateClick)
        self.cam_right_shortcut.activated.connect(self.cam_right_btn.animateClick)
        self.cam_up_shortcut.activated.connect(self.cam_up_btn.animateClick)
        self.cam_down_shortcut.activated.connect(self.cam_down_btn.animateClick)
        self.cam_update_shortcut.activated.connect(self.cam_update_btn.animateClick)

        self.cam_horizontal_slider.valueChanged.connect(self.update_fields)
        self.cam_vertical_slider.valueChanged.connect(self.update_fields)
        self.cam_horizontal_field.valueChanged.connect(self.update_sliders)
        self.cam_vertical_field.valueChanged.connect(self.update_sliders)

        # self.cam_cmd_pub = rospy.Publisher('cam_cmd', Command, queue_size=10)
        # rospy.Timer(rospy.Duration(1.0/10.0), self.publish_command)

    def init_fields(self):
        self.cam_horizontal_field.setValue(0)
        self.cam_horizontal_slider.setValue(0)
        self.cam_horizontal_pos_info.setValue(0)
        self.cam_vertical_field.setValue(0)
        self.cam_vertical_slider.setValue(0)
        self.cam_vertical_pos_info.setValue(0)
        self.cam_keyboard_check_box.setChecked(False)

        self.cam_horizontal_pos = 0
        self.cam_vertical_pos = 0

        self.cam_horizontal_pos_signal = 0
        self.cam_vertical_pos_signal = 0

        self.update_command()

    def cam_left_btn_callback(self):
        self.cam_horizontal_slider.triggerAction(2)
        self.update_fields()
        self.update_command()

    def cam_right_btn_callback(self):
        self.cam_horizontal_slider.triggerAction(1)
        self.update_fields()
        self.update_command()

    def cam_up_btn_callback(self):
        self.cam_vertical_slider.triggerAction(1)
        self.update_fields()
        self.update_command()

    def cam_down_btn_callback(self):
        self.cam_vertical_slider.triggerAction(2)
        self.update_fields()
        self.update_command()

    def cam_keyboard_check_box_callback(self):
        self.update_command()

    def update_sliders(self):
        self.cam_horizontal_pos = self.cam_horizontal_field.value()
        self.cam_vertical_pos = self.cam_vertical_field.value()
        self.cam_horizontal_slider.setValue(self.cam_horizontal_pos)
        self.cam_vertical_slider.setValue(self.cam_vertical_pos)

    def update_fields(self):
        self.cam_horizontal_pos = self.cam_horizontal_slider.value()
        self.cam_vertical_pos = self.cam_vertical_slider.value()
        self.cam_horizontal_field.setValue(self.cam_horizontal_pos)
        self.cam_vertical_field.setValue(self.cam_vertical_pos)

    def update_command(self):
        self.cam_horizontal_pos_signal = self.cam_horizontal_pos
        self.cam_vertical_pos_signal = self.cam_vertical_pos
        self.cam_horizontal_pos_info.setValue(self.cam_horizontal_pos_signal)
        self.cam_vertical_pos_info.setValue(self.cam_vertical_pos_signal)

        self.is_active = self.cam_keyboard_check_box.isChecked()

    # def publish_command(self, event):
    #     command = CamCommand()
    #     command.cam_horizontal = self.cam_horizontal_pos_signal
    #     command.cam_vertical = self.cam_vertical_pos_signal
    #     command.is_active = self.is_active
    #     self.cam_cmd_pub.publish(command)