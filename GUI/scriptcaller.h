#ifndef SCRIPTCALLER_H
#define SCRIPTCALLER_H

#include <QObject>
#include <QDial>

class ScriptCaller// : public QObject
{
    //Q_OBJECT
public:
    ScriptCaller();

    //ScriptCaller(QDial* qDial);

   // ~ScriptCaller(){

    //}

//public slots:

    //void process();

    void callScript(std::string parameter);

//signals:
//    void finished();
//    void error(QString err);

//private:
//     QDial* curDial;
};

#endif // SCRIPTCALLER_H
