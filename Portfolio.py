# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 15:32:50 2026

@author: Hir Shah
"""


import time

def loading1():
    print("\n\nLoading portfolio", end="", flush=True)
    for i in range(3):
        time.sleep(1.0)
        print(".", end="", flush=True)
    print("\n\n")

def loading2():
    print("\033[0m" + "\n\nLoading", end="", flush=True)
    for i in range(3):
        time.sleep(0.5)
        print(".", end="", flush=True)
    print("\n")


def about_me():
        loading2() 
        print("\033[96m" + "\n                        ABOUT THE DEVELOPER! ")
        print("\033[93m" + " -" * 34)

        print("\033[0m" + """\n                           Name: Hir Shah
           Major: Finance & Management Information Systems
                 University: Rutgers Business School
                      Graduation: December 2026
   Skills: Python, SQL, Excel, JavaScript, Financial Analysis""")
    

def background():
        loading2()
        print("\033[96m" + "\n                            Background!")
        print("\033[93m" + " -" * 34)

        print("\033[0m" + """\n        I'm based in Jersey City, NJ. I am trilingual in 
               Gujarati, Hindi, and English. 
              
       I grew up in a family of entrepreneurs, which 
       sparked my interset in business from a young 
       age. I was introduced to coding in elementary 
       school, I started with block coding which made 
            interested in how technology works.
               
          I participated in Girls Who Code Summer 
          Immersion Program in the summer of 2020, 
        throughout the program I learned how to code 
       using JavaScript. Through GWC I participated in 
          DTCC Rising Stars Program, which was from 
         September 2020 to May 2022, where I learned 
        Python. My interest for coding grew even more 
           as I decided I wanted it to be part of my 
           career, so I took AP Computer Science in 
         high school, and have continued to build my 
               coding skills now in college.
                        
        I bridge the gap between financial strategy and 
         technical execution, whether that's building 
         relational databases, modeling cash flows in 
         Excel, or writing Python tools that automate 
            portfolio analysis. I bring that same 
         cross-functional perspective to every team I 
                           work with.""")
        
def why_finance_mis():
    loading2()
    print("\033[96m" + "\n                          Why Finance + MIS?")
    print("\033[93m" + " -" * 34)

    print("\033[0m" + """\n     I double majored in Finance and Management Information Systems
       because I want to understand the numbers and the systems 
                             behind them.

   Finance teaches me how to analyze, forecast, and make decisions
      with data. MIS teaches me how that data is actually built,
    stored, and moved. Together, they let me see the full picture:
     not just what a company's numbers say, but how those numbers
          get to a decision maker's desk in the first place.""")
    
    
def achievements():
        loading2()
        print("\033[96m" + "\n                             Achievements!")
        print("\033[93m" + " -" * 34)

        print("\033[0m" + """\n          I was listed on the Dean's List for Spring 2026, 
           reflecting my academic commitment alongside my 
                         leadership roles.\n
                                
           I was particitated in the DTCC Rising Stars Program 
            through in Girls Who Code, and completed the Girls 
                        Who Code Summer Immersion 
                            Program in 2020.\n""") 

        print("\033[96m" + "\n          Co-Vice President of Corporate Relations | RUWIB")
        print("\033[0m" + """\n         Throught both my Girls Who Code organization experiences 
             I made a commitment that I still carry today, 
            is to always keep learning and always inspire 
            and empower others. I carried those values as 
             the Co-VP of Corporate Relations at Rutgers
             Undergraduate Women in Business, where I led
               corporate partnerships and professional 
                   development for our members.\n""")
        
        print("\033[96m" + "\n                 Treasurer | Ascend Pan-Asian Leaders")
        print("\033[0m" + """\n            Manage chapter finances, budgeting, and funding
                  allocation for events and initiatives.
                  Being part of this community has been 
                   incredibly rewarding and educational.\n""")

        print("\033[96m" + "\n        Logistics & Events Manager | Girls Who Code @ Rutgers")
        print("\033[0m" + """\n             From a participant in the national 
                 organization to a leader, I planed and ran
                  coding workshops and events for students
                              at my university.""")
    
    
def projects():
        loading2()
        print("\033[96m" + "\n                            Projects!")
        print("\033[93m" + " -" * 34)
    
        print("\033[96m" + "\n         Hotel Management Database | DBMS Course Project")  
        print("\033[0m" + """\n         Worked with SQL databases using Microsoft Access. 
          Built a full relational database from scratch, 
         designed the ERD, normalized tables to 3NF, and 
        wrote SQL queries to pull meaningful data. Utalized 
         something I'd never touched - Microsoft Access - 
               and created a project I was proud of.\n""")
          
        print("\033[96m" + "        Jaguar Land Rover Case Study | Fixed Income Class")
        print("\033[0m" + """\n         Analyzed JLR financials to assess profitability, 
         leverage, liquidity, and credit risk. Built an 
         Excel scenario model evaluating cash flow and 
                  investment recommendations.\n""")
 
        print("\033[96m" + "             J&J Case Competition @ Rutgers University") 
        print("\033[0m" + """\n         Took the inititive to sign up and to be part 
         a case competition stepping outside of my comfort 
           zone. Met new people, learned new skills, and 
             gained a new perspective on teamwork and 
             collaboration. Worked with students from 
              different years and majors to analyze a 
                    real-world business problem.
              
         Analyzed Johnson & Johnson's financials as part 
         of a case competition and presented our findings 
         in front of company executives. Built the Excel 
          model, led the financial analysis, and helped 
             craft the presentation. One of the most 
           real-world experiences I have had in school.""")
   
    
def interests():
        loading2()
        print("\033[96m" + "\n                            Interests")
        print("\033[93m" + " -" * 34)
    
        print("\033[0m" + """\n          Outside of finance and coding, I like to 
        I play tennis, paint, and, have a deep love for 
         animals. I'm also an avid gardener - currently 
        propagating snake plants, roses, and a mulberry 
                    tree from cuttings.
             
       I grew up speaking Gujarati, Hindi, and English 
       and have a huge passion for Indian and Western 
         music. My top favorites from India include 
          Bollywood, Gujarati, and Rajastani beats. 
          
         I'm also a Nintendo Switch player when I need 
                         to decompress.""")
    
   
def intro():
    loading1()
    print("\033[93m" + " *" * 34)
    print("\033[96m" + "                    Welcome to Hir's Portfolio")
    print("\033[93m" + " *" * 34)
    print("\033[92m" +  "                Built For Finance. Wired For Data.\n")    
        
    
def main_menu():
    options = { 
        "1": about_me,
        "2": background,
        "3": why_finance_mis,
        "4": achievements,
        "5": projects,
        "6": interests
        }
    
    while True:
        loading2()
        print("\033[96m" + "\n                           NAVIGATION MENU")
        print("\033[93m" + " -" * 34)
        print("\033[0m" + """\n                               0 - Exit
                             1 - About Me
                            2 - Background
                         3 - Why Finance + MIS
                           4 - Achievements
                             5 - Projects
                             6 - Interests""")

        choice = input("\033[92m" + "\n                        Enter a number (0-6): ").strip()
        if choice == "0":
            loading2()
            print("\033[92m" + """\n                   Thanks for visiting my portfolio!
                              Love ~ Hir :)""")
            input("\n             Press Enter to return to the navigation menu") 
        
        elif choice in options:
            options[choice]()
            input("\n             Press Enter to return to the navigation menu")

        else: 
            loading2()
            print("\033[92m" +  "\n           Invalid input. Enter a number between 0 and 6.\n")


intro()
main_menu()