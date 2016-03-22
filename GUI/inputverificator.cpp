#include "inputverificator.h"
#include <QMessageBox>
#include <QString>
#include <sstream>
#include <QLineEdit>
#include <stdio.h>
#include <iostream>
//#include <QSpinBox>
InputVerificator::InputVerificator()
{

}


bool InputVerificator::isEmpty(QLineEdit*& qlineEdit, QLabel*& errorField, QString errorString){
    QString text = qlineEdit->text();
    errorField->hide();
    bool flag = true;

    if (text.isEmpty()){
        errorField->setText(errorString);
        errorField->setStyleSheet(styleSheet);
        errorField->show();
        flag = false;
    }

    return flag;
}

bool InputVerificator::isEmpty(QDoubleSpinBox*& qlineEdit, QLabel*& errorField, QString errorString){
    QString text = qlineEdit->text();
    errorField->hide();
    bool flag = true;

    if (text.isEmpty()){
        errorField->setText(errorString);
        errorField->setStyleSheet(styleSheet);
        errorField->show();
        flag = false;
    }

    return flag;
}

bool InputVerificator::isEmpty(QSpinBox*& qlineEdit, QLabel*& errorField, QString errorString){
    QString text = qlineEdit->text();
    errorField->hide();
    bool flag = true;

    if (text.isEmpty()){
        errorField->setText(errorString);
        errorField->setStyleSheet(styleSheet);
        errorField->show();
        flag = false;
    }

    return flag;
}

bool InputVerificator::areSame(QString stpName, QString igsName, QLabel*& STEPFileInput, QLabel*& IGSFileInput)
{
    QMessageBox messageBox;
    bool flag = true;

    if(stpName.compare(igsName)!=0){
        STEPFileInput->setStyleSheet(styleSheet);
        IGSFileInput->setStyleSheet(styleSheet);
        messageBox.critical(0, "Error", "Filenames are not equal");
        messageBox.setFixedSize(500,200);
        flag = false;
    }
    return flag;
}

bool InputVerificator::checkFileName(QString file, QString name, QString type, QLabel*& errorField)
{
    bool flag = true;

    if (!file.endsWith(type)){
        errorField->setText("Please choose the " + type + " file");
        errorField->setStyleSheet(styleSheet);
        flag = false;
    } else {
        if (name.contains(".")){
            errorField->setText("Filename can not contain a dot");
            errorField->setStyleSheet(styleSheet);
            flag = false;
        }
    }
    return flag;

}

bool InputVerificator::checkRange(const QString& input_string, QLabel*& errorField, double min, double max)
{
   // QString input_string = input->text();
    double value = input_string.toDouble();
    std::cout << value << std::endl;

    bool flag = 1;
    if ((value >= max) || (value <= min))
    {
        std::cout << "here!" << std::endl;
        std::ostringstream error_message_stream;
        error_message_stream << "The value should be between " << min << " and " << max;
        std::string error_message = error_message_stream.str();
        std::cout << error_message << std::endl;
        errorField->setText("!!!");//setText(QString::fromUtf8(error_message.c_str()));
        errorField->setStyleSheet(styleSheet);
        errorField->update();
        flag = 0;
    }
    return flag;
}
