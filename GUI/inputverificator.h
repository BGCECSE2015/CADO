#ifndef INPUTVERIFICATOR_H
#define INPUTVERIFICATOR_H

#include <QMainWindow>
#include <QString>
#include <QLineEdit>
#include <QLabel>
#include <QSpinBox>
class InputVerificator
{
private:
    QString styleSheet = "QLabel {color : red}";

public:
    InputVerificator();
    bool isEmpty(QLineEdit*& qlineEdit, QLabel*& errorField, QString errorString);
    bool isEmpty(QDoubleSpinBox *&qlineEdit, QLabel*& qlabel, QString errorMessage);
    bool checkFileName(QString file, QString name, QString type, QLabel*& errorField);
    bool areSame(QString stpName, QString igsName, QLabel*& STEPFileInput, QLabel*& IGSFileInput);
    bool checkRange(const QString& input, QLabel*& errorField, double min, double max);
    bool isEmpty(QSpinBox*& qlineEdit, QLabel*& errorField, QString errorString);

};

#endif // INPUTVERIFICATOR_H
