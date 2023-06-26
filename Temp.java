public class Temp {
    public static void main(String args[]) {
        Subtemp sub = new Subtemp();
        int subx = sub.get_x();
        System.out.println(subx);
        // System.out.println(subx);
        // System.out.println("coucou Martin");
        int a = 1;
        int b = 2;
        float c = 3;
        float d = 4;
        int e = a + b;
        float f = c + d;
        System.out.println(e);
        System.out.println(f);
        
    }
}

interface interfaceSubTemp {
    public int get_x();
}

class Subtemp implements interfaceSubTemp{
    int x;

    public Subtemp() {
        this.x = 10;
    }

    public int get_x() {
        return x;
    }

    public int inutile(String temp) {
        int a = 1;
        int b = 2;
        return a + b;
    }
}