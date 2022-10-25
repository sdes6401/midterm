package designpattern_3;

public class StaticInnerClass {
    private StaticInnerClass(){}

    public static StaticInnerClass getInstance(){
        return StaticInnerClassHolder.instance;
    }

    private static class StaticInnerClassHolder{
        private static StaticInnerClass instance = new StaticInnerClass();
    }
}
