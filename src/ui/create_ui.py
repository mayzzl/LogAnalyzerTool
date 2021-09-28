import os
import shutil
import sys
import pandas as pd
from PySide2.QtCore import QFile, QIODevice, QTextStream
from PySide2.QtGui import QIcon
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QWidget, QFileDialog, QMessageBox


class LogTool(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = QUiLoader().load('../../config/ui/lat.ui')
        self.module_ui = [self.ui.Common, self.ui.Video, self.ui.Audio,
                          self.ui.Display]
        self.set_icon()
        self.filename = None
        self.file_path = None
        self.module_keywords = []
        self.input_keywords = []
        self.outputs_log = []
        self.conclusion = []
        self.set_menu()
        self.open()
        self.signal()
        self.ui.show()

    def open(self):
        self.ui.OPEN.clicked.connect(self.open_file)

    def signal(self):
        self.ui.Submit.clicked.connect(self.generate)

    def set_icon(self):
        appIcon = QIcon('../../config/ui/logo.png')
        self.ui.setWindowIcon(appIcon)

    def set_menu(self):
        self.ui.Open.triggered.connect(self.open_file)
        self.ui.Save.triggered.connect(self.save_as_file)
        self.ui.Quit.triggered.connect(self.exit_app)
        self.ui.Contact.triggered.connect(self.contact_us)

    def contact_us(self):
        QMessageBox.information(
            self.ui,
            'Please Contact Us:',
            'Ben.Liu1@unisoc.com\n'
            'Jubo.Wang@unisoc.com\n'
            'Lei.Zhang1@unisoc.com\n')

    def creat_log(self, filename):
        father_path = os.path.abspath(os.path.dirname(filename)
                                      + os.path.sep + '.')
        shutil.copy2('analyzer.py', father_path)
        os.system('python ' + father_path + '\\analyzer.py')
        self.file_path = filename[:-5]

    def open_file(self):
        """
        仅支持匹配打开.ylog文件
        :return:
        """
        self.filename, _ = QFileDialog.getOpenFileName(self,
                                                       '选取Log文件',
                                                       '',
                                                       'Log Files (*.ylog)')
        self.ui.YlogName.setPlainText(self.filename)
        self.creat_log(self.filename)
        # self.open_file_flag(self.filename)

    def open_all_type_file(self):
        """
        可匹配所有文件并打开，可调整盘符
        :return:
        """
        self.filename, _ = QFileDialog.getOpenFileName(self,
                                                       '选取Log文件',
                                                       'C:/',
                                                       'All Files (*);;Log Files (*.ylog)')
        self.creat_log(self.filename)
        # self.open_file_flag(self.filename)

    def open_file_flag(self, path):
        if path:
            f = QFile(path)
            if not f.open(QIODevice.ReadOnly | QIODevice.Text):
                self.msgCritical('打开文件失败')
                return False
            self.path = path
            self.ui.LogOutput.setPlainText(QTextStream(f).readAll())
            f.close()  # 关闭文件

    def save_file(self):
        if self.path is None:
            return self.save_as_file()
        self._saveToPath(self.path)

    def _saveToPath(self, path):
        f = QFile(path)
        if not f.open(QIODevice.WriteOnly):
            self.msgCritical('打开文件失败')
            return False

        self.path = path
        outText = QTextStream(f)
        outText << self.ui.LogOutput.toPlainText()
        f.close()

    def save_as_file(self):
        path, _ = QFileDialog.getSaveFileName(self, '保存文件', '',
                                              '文本文件 (*.txt)')
        if not path:
            return
        self._saveToPath(path)

    def exit_app(self):
        self.ui.close()

    def tip(self):
        if (
                self.ui.Common.isChecked() == False and self.ui.Video.isChecked() == False
                and self.ui.Audio.isChecked() == False and self.ui.Display.isChecked() == False):
            QMessageBox.information(
                self.ui,
                'Warning',
                'Please Select Modules！')
            return False
        return True

    def generate(self):
        self.module_keywords.clear()
        while self.tip():
            for check_box in self.module_ui:
                if check_box.isChecked():
                    self.module_keywords.append(check_box.text())

            self.analyzer(self.file_path)
            break

    def analyzer(self, filename):
        modules, types, keywords, reason = self.load_file()
        print(self.module_keywords)
        for index in range(len(keywords)):
            with open(filename + '/0-android.log', 'r', errors='ignore') as fi:
                for line in fi:
                    if modules[index] in self.module_keywords:
                        if keywords[index] in line:
                            self.outputs_log.append(line)
                            self.conclusion.append("**************************")
                            self.conclusion.append(
                                "KeyWord: " + keywords[index])
                            self.conclusion.append("Reason: " + reason[index])
                            self.conclusion.append('\n')

        # 输出
        self.ui.LogOutput.setPlainText('\n'.join(self.outputs_log))
        self.ui.Conclusion.setPlainText('\n'.join(self.conclusion))

    def load_file(self):
        modules = []
        types = []
        keywords = []
        reason = []
        df0 = pd.read_excel('../../docs/keywords.xlsx', usecols=[0],
                            names=None)
        df1 = pd.read_excel("../../docs/keywords.xlsx", usecols=[1],
                            names=None)
        df2 = pd.read_excel("../../docs/keywords.xlsx", usecols=[2],
                            names=None)
        df3 = pd.read_excel("../../docs/keywords.xlsx", usecols=[3],
                            names=None)
        df_li0 = df0.values.tolist()
        df_li1 = df1.values.tolist()
        df_li2 = df2.values.tolist()
        df_li3 = df3.values.tolist()

        for s_li0 in df_li0:
            modules.append(s_li0[0])
        for s_li1 in df_li1:
            types.append(s_li1[0])
        for s_li2 in df_li2:
            keywords.append(s_li2[0])
        for s_li3 in df_li3:
            reason.append(s_li3[0])
        return modules, types, keywords, reason


if __name__ == '__main__':
    app = QApplication(sys.argv)
    LAT = LogTool()
    sys.exit(app.exec_())
