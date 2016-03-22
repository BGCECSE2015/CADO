#include "mainwindow.h"
#include "ui_mainwindow.h"
#include "inputverificator.h"

#include <QFileDialog>
#include <QMessageBox>
#include <QFuture>
#include <QtConcurrent/QtConcurrent>
#include <QtGui>
#include <QFont>
#include <QThreadPool>

#include "stringhelper.h"

#include <iostream>

#include <stdlib.h>     //for using the function sleep
#include <stdio.h>
#include <time.h>
#include <unistd.h>

#include <chrono>


MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    QLocale dotSeperator(QLocale::C);

    ui->ForceDoubleSpinBox->setMinimum(0);
    ui->ForceDoubleSpinBox->setMaximum(1000000);
    ui->ForceDoubleSpinBox->setSingleStep(0.5);
    ui->ForceDoubleSpinBox->setValue(1.5);
    ui->ForceDoubleSpinBox->setLocale(dotSeperator);

    ui->SmoothnessDoubleSpinBox->setMinimum(0);
    ui->SmoothnessDoubleSpinBox->setMaximum(10000);
    ui->SmoothnessDoubleSpinBox->setSingleStep(0.1);
    ui->SmoothnessDoubleSpinBox->setValue(0.5);
    ui->SmoothnessDoubleSpinBox->setLocale(dotSeperator);

    ui->ResolutionSpinBox->setMinimum(1);
    ui->ResolutionSpinBox->setMaximum(10);
    ui->ResolutionSpinBox->setLocale(dotSeperator);

    ui->CoarseningSpinBox->setMinimum(1);
    ui->CoarseningSpinBox->setMaximum(50);
    ui->CoarseningSpinBox->setLocale(dotSeperator);

    ui->VolumeFractionDoubleSpinBox->setMinimum(0);
    ui->VolumeFractionDoubleSpinBox->setMaximum(1);
    ui->VolumeFractionDoubleSpinBox->setSingleStep(0.05);
    ui->VolumeFractionDoubleSpinBox->setValue(0.2);
    ui->VolumeFractionDoubleSpinBox->setLocale(dotSeperator);

    this->hide_ErrorFields();
    this->ui->startFreeCadButton->hide();

    this->ui->VoxelizerDial->setValue(0);
    this->ui->VoxelizerDial->setDisabled(true);
    this->ui->ToPyDial->setValue(0);
    this->ui->ToPyDial->setDisabled(true);
    this->ui->NurbsDial->setValue(0);
    this->ui->NurbsDial->setDisabled(true);

    //logoScene->setSceneRect(ui->logoView->Rect());
    this->ui->logoView->setScene(&logoScene);
    logoItem.setPixmap(*logoPicture);
    logoScene.addItem(&logoItem);
  //  ui->logoView->fitInView(logoScene.sceneRect(),Qt::KeepAspectRatioByExpanding);
   // ui->logoView->fitInView();
    this->ui->logoView->show();

    isFixtureFileSupplied = 0;

    /*ui->IGSFileInput->setText("/home/friedrich/Documents/Studium/Master_CSE/BGCE/BGCEGit/Prototypes/OpenCascade/TestGeometry/CantileverColoredNew/CantiLeverWithLoadAtEndSmallerMovedLoad.igs");
    ui->STEPFileInput->setText("/home/friedrich/Documents/Studium/Master_CSE/BGCE/BGCEGit/Prototypes/OpenCascade/TestGeometry/CantileverColoredNew/CantiLeverWithLoadAtEndSmallerMovedLoad.stp");
    ui->BooleanFileInput->setText("/home/friedrich/Documents/Studium/Master_CSE/BGCE/BGCEGit/Prototypes/PYTHON/Back2CAD/Cone.step");
    ui->STEPOutput->setText("/home/friedrich/Documents/Studium/Master_CSE/BGCE/BGCEGit/Prototypes/GUI/build-testGui-Desktop-Debug/testBitch.step");
    igsFile = ui->IGSFileInput->text();
    stpFile = ui->STEPFileInput->text();
    booleanFile = ui->BooleanFileInput->text();
    stepOutputFile = ui->STEPFileInput->text();
    ui->RefinementEdit->setText("0");
    ui->ForceEdit->setText("1");
    ui->Coarsening->setText("2");
    ui->FairnessWeight->setText("0.5");*/
}

MainWindow::~MainWindow()
{
    delete this->logoPicture;
    delete ui;
}

void MainWindow::on_STEPFileSelector_clicked()
{
    QStringList fileNames;

    fileNames = QFileDialog::getOpenFileNames(this, tr("Open File"),"/path/to/file/",tr("STEP File (*.step)"));

    if(fileNames.size()==1){
        stpFile = fileNames.first();
        ui->STEPFileInput->setText(StringHelper::cropText(ui->STEPFileInput, stpFile));
        ui->STEPFileInput->setStyleSheet("QLabel { Color : black }");
        QString stpPath, stpName;
        StringHelper::getPathAndName(stpFile, stpName, stpPath);
        igsFile = stpPath+stpName+".iges";
    }else{
        ui->STEPFileInput->setText("Select ONE step input file!");
        ui->STEPFileInput->setStyleSheet("QLabel { Color : red }");
    }
}

//void MainWindow::on_IGSFileSelector_clicked()
//{
//    QStringList fileNames;

//    fileNames = QFileDialog::getOpenFileNames(this, tr("Open File"),"/path/to/file/",tr("IGES File (*.iges)"));
//    if(fileNames.size()==1){
//        igsFile = fileNames.first();
//        ui->IGSFileInput->setText(StringHelper::cropText(ui->IGSFileInput, igsFile));
//        ui->IGSFileInput->setStyleSheet("QLabel { Color : black }");
//    }else{
//        ui->IGSFileInput->setText("Select ONE iges input file!");
//        ui->IGSFileInput->setStyleSheet("QLabel { Color : red }");
//    }
//}

void MainWindow::showEvent(QShowEvent *) {
    ui->logoView->fitInView(logoScene.sceneRect(),Qt::KeepAspectRatio);
}
void MainWindow::on_runButton_clicked()
{
    this->disableAllElements();
    //ui->IGSFileInput->setStyleSheet("QLabel { Color : black }");
    ui->STEPFileInput->setStyleSheet("QLabel { Color : black }");
    this->hide_ErrorFields();
    this->resetDials();

    QString igsPath, igsName;
    QString stpPath, stpName;
    QString stpOutputPath, stpOutputName;

    StringHelper::getPathAndName(stpFile, stpName, stpPath);
    StringHelper::getPathAndName(stepOutputFile, stpOutputName, stpOutputPath);
    StringHelper::getPathAndName(igsFile, igsName, igsPath);

    std::chrono::time_point<std::chrono::system_clock> start;
    std::chrono::time_point<std::chrono::system_clock> end;
    std::chrono::duration<double> elapsedSeconds;

    //if (this->checkInput(igsName, stpName)){

    //std::cout << "CHECK STILL DISABLED" << std::endl;
    //this->checkInput(igsName, stpName)
    if (this->checkInput(igsName, stpName)){
        QString forceScaling = ui->ForceDoubleSpinBox->text();
        int refinementLevelValue = ui->ResolutionSpinBox->text().toInt() - 1;
        std::string refinementLevelString = std::to_string(refinementLevelValue);
        QString volFraction = ui->VolumeFractionDoubleSpinBox->text();

        QFont boldFont("Cantarell", 11, QFont::Bold);
        QFont normalFont("Cantarell", 11, QFont::Normal);
        QThreadPool qpool;
        QFuture<void> future;


        start = std::chrono::system_clock::now();
        /** Start the Voxelization Script **/
        std::string parameterString = stpPath.toStdString() + " " +
                                      stpName.toStdString() + " " +
                                      forceScaling.toStdString() + " " +
                                      refinementLevelString + " " +
                                      volFraction.toStdString() + " " +
                                      (isFixtureFileSupplied ? "1" : "0");
        std::string scriptCADToVoxel = "./CPP/CADTopOp.sh " + parameterString;
        std::cout << scriptCADToVoxel << std::endl;

        future = QtConcurrent::run(&qpool, &this->scriptCaller, &ScriptCaller::callScript, scriptCADToVoxel);

        this->ui->voxelizationLabel->setFont( boldFont );
        this->rotateDial(this->ui->VoxelizerDial, future);
        this->ui->voxelizationLabel->setFont( normalFont );
        /**                                 **/
        end = std::chrono::system_clock::now();
        elapsedSeconds = end - start;
        double voxelizerTime = elapsedSeconds.count();

        /*std::string vtkPath = "./../../OpenCascade/Code/";
        parameterString = "python ./../../OpenCascade/Code/vtkToPngPrototype.py " + vtkPath + " " + stpName.toStdString();
        std::cout << parameterString << std::endl;
        scriptCaller.callScript(parameterString);*/

        start = std::chrono::system_clock::now();
        /** Start ToPy **/
        parameterString = stpName.toStdString();
        std::string scriptToPy = "./CPP/ToPyRunner.sh " + parameterString;

        future = QtConcurrent::run(&qpool, &this->scriptCaller, &ScriptCaller::callScript, scriptToPy);

        this->ui->topologyOptimizationLabel->setFont( boldFont );
        this->rotateDial(this->ui->ToPyDial, future);
        this->ui->topologyOptimizationLabel->setFont( normalFont );
        /**                                 **/
        end = std::chrono::system_clock::now();
        elapsedSeconds = end - start;
        double topyTime = elapsedSeconds.count();

        start = std::chrono::system_clock::now();
        /** Start the Surface Fitting, Extraction and Back2CAD **/
        std::string cellsAndDimensionsPath = "./PYTHON/NURBSReconstruction";
       // std::string outputFileString = stepOutputFile.toStdString();
        std::string fairnessWeight = ui->SmoothnessDoubleSpinBox->text().toStdString();
        int coarseningFactor = ui->CoarseningSpinBox->text().toInt();
        coarseningFactor = pow(2, coarseningFactor);
        std::string coarseningFactorString = std::to_string(coarseningFactor);
        std::string outputFile = stpOutputPath.toStdString()+stpOutputName.toStdString();
        std::string fixedFileFullPathNameString = this->isFixtureFileSupplied ? stpPath.toStdString() + stpName.toStdString() + "_Fixed.step" : "\"\"";
        std::string booleanFileString = this->isOptimizationDomainSupplied ? stpPath.toStdString() + stpName.toStdString() + "_ToOptimize.step" : "\"\"";
        parameterString = cellsAndDimensionsPath + " " + stpFile.toStdString() + " " + outputFile + " " + fairnessWeight + " " + coarseningFactorString + " "
                + refinementLevelString + " " + fixedFileFullPathNameString + " " + booleanFileString;
        std::string scriptPython = "python ./PYTHON/NURBSReconstruction/runningScript.py " + parameterString;

        std::cout << scriptPython << std::endl;
        //system(scriptPython.c_str());

        future = QtConcurrent::run(&qpool, &this->scriptCaller, &ScriptCaller::callScript, scriptPython);

        this->ui->surfaceFittingLabel->setFont( boldFont );
        this->rotateDial(this->ui->NurbsDial, future);
        this->ui->surfaceFittingLabel->setFont( normalFont );
        /**                                 **/
        end = std::chrono::system_clock::now();
        elapsedSeconds = end-start;
        double surfaceFittingTime = elapsedSeconds.count();

        std::cout << "###Voxelizer: Elapsed Time: " << voxelizerTime << std::endl;
        std::cout << "###Topology Optimization: Elapsed Time: " << topyTime << std::endl;
        std::cout << "###SURFACE-Fitting: Elapsed Time: " << surfaceFittingTime << std::endl;

        this->ui->startFreeCadButton->show();
    }
    this->enableAllElements();
}

void MainWindow::resetDials(){
    this->ui->VoxelizerDial->setStyleSheet( "QDial {background:transparent }" );
    this->ui->ToPyDial->setStyleSheet( "QDial {background:transparent }" );
    this->ui->NurbsDial->setStyleSheet( "QDial {background:transparent }" );
}


void MainWindow::rotateDial(QDial* dial, const QFuture<void>& future){
     int rotationDirection = 1;
     dial->setStyleSheet( "QDial {background-color : orange }" );
     while(future.isRunning()){
         if( dial->value() == dial->maximum()){
             rotationDirection = -1;
         }else if( dial->value() == dial->minimum()){
             rotationDirection = 1;
         }
         dial->setValue(dial->value()+rotationDirection );
         QCoreApplication::processEvents();
         usleep(70000);
     }
     while(dial->value() < dial->maximum()){
         dial->setValue( dial->value()+1 );
         QCoreApplication::processEvents();
         usleep(7000);
     }
     dial->setStyleSheet( "QDial {background-color : green }" );
     dial->setValue(dial->maximum());
     QCoreApplication::processEvents();
}

void MainWindow::setValueOfToPyDial(int value){
    std::cout << "We are actually using this function with value: " << value << std::endl;
    this->ui->ToPyDial->setValue(value % (this->ui->ToPyDial->maximum()+1));
}

bool MainWindow::checkInput(QString igsName, QString stpName){
    InputVerificator verificator;
    QString outputName, outputPath;
    StringHelper::getPathAndName(stepOutputFile, outputName, outputPath);


    bool flag = true;

    flag = flag && verificator.isEmpty(ui->CoarseningSpinBox, ui->ErrorField_coarsening, "Please enter the coarsening");
    flag = verificator.isEmpty(ui->SmoothnessDoubleSpinBox, ui->ErrorField_fairness, "Please enter the fairness weight") && flag;
    flag = verificator.isEmpty(ui->ForceDoubleSpinBox, ui->ErrorField_force, "Please enter the force") && flag;
    flag = verificator.isEmpty(ui->ResolutionSpinBox, ui->ErrorField_refinement, "Please enter the refinement") && flag;
    flag = verificator.isEmpty(ui->VolumeFractionDoubleSpinBox, ui->ErrorField_volumefraction, "Please enter the volume fraction") && flag;

    //flag = verificator.areSame(stpName, igsName, ui->STEPFileInput, ui->IGSFileInput) && flag;

    flag = verificator.checkFileName(this->stpFile, stpName, ".step", ui->STEPFileInput) && flag;
    //flag = verificator.checkFileName(this->igsFile, igsName, ".iges", ui->IGSFileInput) && flag;
    flag = verificator.checkFileName(this->stepOutputFile, outputName, ".step", ui->STEPOutput) && flag;
    return flag;
}

void MainWindow::on_Output_selector_clicked()
{
    QString fileName;
    fileName = QFileDialog::getSaveFileName(this, tr("Save File"), QDir::currentPath(),tr("STEP File (*.step)"));
    if(fileName.size()>=1){
        if(!(fileName.endsWith(".step"))){
            fileName = fileName + tr(".step");
        }
        stepOutputFile = fileName;
        ui->STEPOutput->setText(StringHelper::cropText(ui->STEPOutput, stepOutputFile));
        ui->STEPOutput->setStyleSheet("QLabel { Color : black }");
    } else {
        ui->STEPOutput->setText("Select ONE step output file!");
        ui->STEPOutput->setStyleSheet("QLabel { Color : red }");
    }
}

void MainWindow::hide_ErrorFields(){
    ui->ErrorField_force->hide();
    ui->ErrorField_refinement->hide();
    ui->ErrorField_coarsening->hide();
    ui->ErrorField_fairness->hide();
    ui->ErrorField_volumefraction->hide();
}

void MainWindow::on_startFreeCadButton_clicked()
{
    QString outputFile;
    QString outputPath;
    StringHelper::getPathAndName(stepOutputFile, outputFile, outputPath);
    std::string freeCADCommand = "freecad " + stepOutputFile.toStdString() + " " +
            (isFixtureFileSupplied ? outputPath.toStdString() + outputFile.toStdString() + "_BOOLEANED.step " : " ") + "&"; //+
          //  (isOptimizationDomainSupplied ? outputFile.toStdString() + "_ALLOWED.step" : "");
    system(freeCADCommand.c_str());
}

void MainWindow::on_checkBox_stateChanged(int newState)
{
    if(newState){
        this->ui->checkBoxWarningLabel->setText("Specify as \'StepFileName\'_Fixed.step");
        this->ui->checkBoxWarningLabel->setStyleSheet("QLabel { Color : red }");
        this->isFixtureFileSupplied = 1;
    }else{
        this->ui->checkBoxWarningLabel->setText("");
        this->isFixtureFileSupplied = 0;
    }
}

void MainWindow::on_checkBox_2_stateChanged(int newState)
{
    if(newState){
        this->ui->checkBoxWarningLabel_2->setText("Specify as \'StepFileName\'_ToOptimize.step");
        this->ui->checkBoxWarningLabel_2->setStyleSheet("QLabel { Color : red }");
        this->isOptimizationDomainSupplied = 1;
    }else{
        this->ui->checkBoxWarningLabel_2->setText("");
        this->isOptimizationDomainSupplied = 0;
    }
}

void MainWindow::disableAllElements(){
    this->ui->STEPFileSelector->setDisabled(true);
    //this->ui->IGSFileSelector->setDisabled(true);
    this->ui->checkBox->setDisabled(true);
    this->ui->checkBox_2->setDisabled(true);
    this->ui->ForceDoubleSpinBox->setDisabled(true);
    this->ui->ResolutionSpinBox->setDisabled(true);
    this->ui->VolumeFractionDoubleSpinBox->setDisabled(true);
    this->ui->SmoothnessDoubleSpinBox->setDisabled(true);
    this->ui->CoarseningSpinBox->setDisabled(true);
    this->ui->Output_selector->setDisabled(true);
    this->ui->runButton->setDisabled(true);
}

void MainWindow::enableAllElements(){
    this->ui->STEPFileSelector->setEnabled(true);
    //this->ui->IGSFileSelector->setEnabled(true);
    this->ui->checkBox->setEnabled(true);
    this->ui->checkBox_2->setEnabled(true);
    this->ui->ForceDoubleSpinBox->setEnabled(true);
    this->ui->ResolutionSpinBox->setEnabled(true);
    this->ui->VolumeFractionDoubleSpinBox->setEnabled(true);
    this->ui->SmoothnessDoubleSpinBox->setEnabled(true);
    this->ui->CoarseningSpinBox->setEnabled(true);
    this->ui->Output_selector->setEnabled(true);
    this->ui->runButton->setEnabled(true);
}


