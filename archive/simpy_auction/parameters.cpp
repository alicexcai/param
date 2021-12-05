#include "parameters.h"
#include "ui_parameters.h"

Parameters::Parameters(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::Parameters)
{
    ui->setupUi(this);
}

Parameters::~Parameters()
{
    delete ui;
}
