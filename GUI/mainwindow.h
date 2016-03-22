#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QLabel>
#include <QString>
#include <QFutureWatcher>

#include <QMainWindow>

#include <QImage>
#include <QPixmap>
#include <QGraphicsPixmapItem>
#include <QGraphicsScene>


#include "scriptcaller.h"

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = 0);
    ~MainWindow();

private slots:
    void on_STEPFileSelector_clicked();

    //void on_IGSFileSelector_clicked();

    void on_runButton_clicked();

    bool checkInput(QString igsName, QString stpName);

    void on_Output_selector_clicked();

    void hide_ErrorFields();

    void setValueOfToPyDial(int value);

    void on_startFreeCadButton_clicked();

    void rotateDial(QDial* dial,const QFuture<void>& future);

    void resetDials();

    void on_checkBox_stateChanged(int arg1);

    void on_checkBox_2_stateChanged(int arg1);

    void disableAllElements();

    void enableAllElements();
    void showEvent(QShowEvent *);

  //  void on_VolumeFractionEdit_textEdited(const QString &arg1);

private:
    Ui::MainWindow *ui;

    QFutureWatcher<void> futureWatcher;
    QString stpFile;
    QString igsFile;
    QString stepOutputFile;
    bool isFixtureFileSupplied = 0;
    bool isOptimizationDomainSupplied = 0;

    ScriptCaller scriptCaller;

    QGraphicsScene logoScene;
    QPixmap* logoPicture = new QPixmap("GUI/images/LOGO.png");
    QGraphicsPixmapItem logoItem;
};

#endif // MAINWINDOW_H
