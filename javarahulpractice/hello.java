import java.util.Scanner;
class hello {
    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);
    
        int num1 = scan.nextInt();
        int num2 = scan.nextInt();

        if(num1==num2)
        {
            System.out.println("Yes it's true");
        }else
        {
            System.out.println("No it's false");
        }
}        
}
