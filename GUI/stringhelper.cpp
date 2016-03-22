#include "stringhelper.h"

StringHelper::StringHelper()
{
}

void StringHelper::getPathAndName(QString fullPath, QString &name, QString &path){
    QStringList igsPathParsed = fullPath.split( "/" );
    path = "";
    for (int i = 0; i < igsPathParsed.length() - 1; i++){
        path.push_back(igsPathParsed.value(i) + "/");
    }

    name = igsPathParsed.value(igsPathParsed.length() - 1);
    name = name.split(".").first();
    //name = name.left(name.length() - 4);
}

QString StringHelper::cropText(QLabel* curLabel, QString toCropString){
    int width = curLabel->width();
    QFontMetrics metrics = curLabel->fontMetrics();
    QString croppedText = metrics.elidedText(toCropString, Qt::ElideLeft, width);
    return croppedText;
}
