package designpattern_2;

public class divide implements IStrategy{
    @Override
    public int calcuate(int a, int b) {
        return a / b;
    }
}
