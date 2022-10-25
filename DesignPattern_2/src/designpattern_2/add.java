package designpattern_2;

public class add implements IStrategy{
    @Override
    public int calcuate(int a, int b) {
        return a + b;
    }
}
