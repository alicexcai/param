#ifndef PARAMETERS_H
#define PARAMETERS_H

#include <QDialog>

namespace Ui {
class Parameters;
}

class Parameters : public QDialog
{
    Q_OBJECT

public:
    explicit Parameters(QWidget *parent = nullptr);
    ~Parameters();

private:
    Ui::Parameters *ui;
};

#endif // PARAMETERS_H
