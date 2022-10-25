package designpattern_2;

public class multyply implements IStrategy{
    @Override
    public int calcuate(int a, int b) {
        return a * b;
    }
}
