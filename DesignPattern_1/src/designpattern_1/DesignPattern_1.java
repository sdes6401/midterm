package designpattern_1;

public class DesignPattern_1 {

    public static void main(String[] args) {
        // Factory Method Pattern
        Factory friesFac = new FrenchFriesFactory();
        Product fries = friesFac.getProduct();
        Product myfries = ((FrenchFriesFactory)friesFac).getProduct("無鹽的");

        fries.describe();//我是有鹽巴薯條
        myfries.describe();//我是無鹽的薯條
    }
    
}
