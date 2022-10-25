package designpattern_1;

public class FrenchFries implements Product{
    String state;
    
    protected FrenchFries()
    {
        this.state = "有鹽巴";
    }
    
    protected FrenchFries(String state)
    {
        this.state = state;
    }
    
    @Override
    public void describe() {
        System.out.println("我是"+ state +"薯條");
    }
}
