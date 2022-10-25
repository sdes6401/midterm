package designpattern_2;

public class minus implements IStrategy{
    @Override
    public int calcuate(int a, int b) {
        return a - b;
    }
}
