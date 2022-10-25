package designpattern_2;

public class Calculator{

    private int now = 0 ;

    private IStrategy strategy ;

//    策略模式
    public int execute(int a , int b){
        return strategy.calcuate(a, b);
    }

    public void reset(){
        this.now = 0 ;
    }

//    簡單工廠模式
    public void setStrategy(DoType doType) {
        switch (doType){
            case ADD:
                this.strategy = new add();
                break;
            case MINUS:
               this.strategy = new minus();
                break;
            case DIVIDE:
                this.strategy = new divide();
                break;
            case MULTYPLY:
               this.strategy = new multyply();
                break;
        }
    }

    enum DoType{
        ADD , MINUS , DIVIDE , MULTYPLY
    }

}
