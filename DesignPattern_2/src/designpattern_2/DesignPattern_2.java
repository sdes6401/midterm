package designpattern_2;

public class DesignPattern_2 {

    public static void main(String[] args) {
        Calculator aa = new Calculator();
        Calculator bb = new Calculator();
        Calculator cc = new Calculator();
        Calculator dd = new Calculator();
        // ADD
        aa.setStrategy(Calculator.DoType.ADD);
        System.out.println(aa.execute(12, 3));
        
        // MINUS
        bb.setStrategy(Calculator.DoType.MINUS);
        System.out.println(bb.execute(12, 3));
        
        // DIVIDE
        cc.setStrategy(Calculator.DoType.DIVIDE);
        System.out.println(cc.execute(12, 3));
        
        // MULTYPLY
        dd.setStrategy(Calculator.DoType.MULTYPLY);
        System.out.println(dd.execute(12, 3));
    }
    
}
