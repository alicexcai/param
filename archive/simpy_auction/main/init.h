#ifndef INIT_H
#define INIT_H

#include <QMainWindow>

namespace Ui {
class Init;
}

class Init : public QMainWindow
{
    Q_OBJECT

public:
    explicit Init(QWidget *parent = nullptr);
    ~Init();

private:
    Ui::Init *ui;
};

#endif // INIT_H
