#ifndef STRINGHELPER_H
#define STRINGHELPER_H

#include <QString>
#include <QLabel>

class StringHelper
{
public:
    StringHelper();

    static void getPathAndName(QString fullPath, QString &name, QString &path);

    static QString cropText(QLabel* curLabel, QString toCropString);
};

#endif // STRINGHELPER_H
