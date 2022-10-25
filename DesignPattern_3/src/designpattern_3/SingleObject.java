package designpattern_3;

public class SingleObject {
    private static SingleObject instance = new SingleObject();
 
    private SingleObject(){}
 
    public static SingleObject getInstance(){
       return instance;
    }
}
