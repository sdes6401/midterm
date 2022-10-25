package designpattern_3;

public class DesignPattern_3 {

    public static void main(String[] args) {
        Cola cola = (Cola) SingletonFactory.getColaFactory().getProduct();
        Humburger humberger =(Humburger) SingletonFactory.getHumbergerFactory().getProduct();
        
        System.out.println(cola.getName());
        System.out.println(humberger.getName());
    }
    
}
