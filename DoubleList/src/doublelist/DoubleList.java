package doublelist;

/**
 *
 * @author Liang
 */             

import java.io.*;
import java.util.Scanner;
import java.util.InputMismatchException;

// 定義一個 Node 的資料結構(Class)，其資料包含左、右子鏈結，姓名及分數
class student { 
	public String name="";   // 姓名
	public int score=0;      // 分數   
	public student llink;    // 節點左鏈結 
	public student rlink;    // 節點右鏈結 
}

class DoubleList {
    static student prev, ptr, head, current;
    static Scanner keyboard = new Scanner(System.in);

    DoubleList() { 
            ptr = new student();		   
            ptr.name = "0";
            ptr.llink = ptr;
            ptr.rlink = ptr;		   
            head = ptr;
    }
	
    //加入函數，依分數的高低排序
 	public static void insert_f() 
 	{   
 		ptr = new student();		            
		System.out.printf("\n   Please enter student name  : ");
 		ptr.name = keyboard.next();       			
		System.out.printf("   Please enter student score : ");
  		ptr.score = keyboard.nextInt();
        
		System.out.println("");
		prev = head;
		current = head.rlink;
		while((current != head) && (current.score >= ptr.score)) {
                    prev = current;
                    current = current.rlink;
		}
		ptr.rlink = current;
		ptr.llink = prev;
		prev.rlink = ptr;
		current.llink = ptr;
	}
	
    //刪除函數
	public static void delete_f() 
	{ 
            String del_name="";
            int count = 0;
            student clear;

            if(head.rlink == head) // 無資料顯示錯誤 
                System.out.printf("\n        No student record !!\n\n"); 
            else {
                System.out.printf("\n       Delete student name: ");
                del_name = keyboard.next();

                prev = head;    			
                current = head.rlink;
                while((current!= head) && (!del_name.equals(current.name))) {              
                    prev = current;
                    current = current.rlink;
                }
            }
 
            if(head != current) { 
                prev.rlink = current.rlink;
                current.rlink.llink = prev;
                current = null;
                System.out.printf("Student %s has been deleted!!\n\n", del_name);
            }
            else{			 
                System.out.printf("Student %s not found!!\n\n", del_name);
            }
	}
	
    // 輸出函數
    public static void display_f() 
    { 
		int count = 0;

		if(head.rlink == head) // 無資料顯示錯誤
                    System.out.printf("\n        No student record !!\n");  
		else {
                    System.out.printf("\n%-15s %-10s\n", "NAME", "SCORE");
                    System.out.printf("---------------------------\n");
                    current = head.rlink;
                    while(current != head) {
                        System.out.printf("%-15s %-3d\n", current.name, current.score);
                        count++;
                        current = current.rlink;
                    }
                    System.out.println("---------------------------");
                    System.out.println("There is(are) " + count + " record(s) found !!\n");
		}
	}
	
    // 主函數
	public static void main (String args[]) 
	{  
 		int option=0; 
		DoubleList DBLink = new DoubleList();
 
		do {
                    System.out.println();			 
                    System.out.println("********  Double linked list  *********");
                    System.out.println("           <1> Insert                  ");
                    System.out.println("           <2> Delete                  ");
                    System.out.println("           <3> List                    ");
                    System.out.println("           <4> Exit                    ");
                    System.out.println("***************************************");
                    System.out.print("             Choice : ");

                    try {
                        option = keyboard.nextInt();
                    } catch(InputMismatchException e) {
                        keyboard.nextLine();
                        System.out.printf("Not a correctly number.\n");
                        System.out.printf("Try again\n\n");
                    }

                    switch(option) {			   
                        case 1 :
                                insert_f();  //新增函數
                                break;
                        case 2 :
                                delete_f();  //刪除函數
                                break;
                        case 3 :
                                display_f();  //輸出函數
                                break;
                        case 4 :
                                System.exit(0);	
                    }
		} while (true);
	}
}
