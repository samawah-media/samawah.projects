import pandas as pd
from datetime import datetime

def create_real_data():
    # 1. Projects
    projects = pd.DataFrame([
        {
            "Project_ID": "P_REPORTS",
            "Name": "منصة التقارير",
            "Manager": "عوض",
            "Project_Path": "Tech/Media",
            "Current_Stage": "Execution",
            "Start_Date": "2026-01-06",
            "End_Date": "2026-02-15",
            "Total_Budget": 23000,
            "Description": "مشروع حصر وبرمجة وتنظيم منصة التقارير الكبرى",
            "Logo_URL": "https://cdn-icons-png.flaticon.com/512/2645/2645853.png"
        }
    ])

    # 2. Tasks (Full Transcription from Image)
    # [Task_ID, Project_ID, Task_Name, Sub_Task, Task_Category, Owner, Start, End, Cost, Qty_Total, Qty_Done, Status]
    tasks_data = [
        # البحث
        ["T1", "P_REPORTS", "مراجعة ال 12 ألف تقرير المتبقي", "البحث", "Content/Writing", "فريق البحث", "2026-01-06", "2026-01-12", 15000, 12000, 12000, "Completed"],
        ["T2", "P_REPORTS", "البحث عن 18 ألف تقرير جديد", "البحث", "Content/Writing", "فريق البحث", "2026-01-06", "2026-01-12", 0, 18000, 7200, "In Progress"],
        
        # معالجة البيانات
        ["T3", "P_REPORTS", "فرز التقارير والتأكد من شمولها", "معالجة البيانات", "General", "فريق البحث", "2026-01-08", "2026-01-18", 0, 100, 0, "Not Started"],
        ["T4", "P_REPORTS", "التأكد من صحة البيانات وإتاحتها", "معالجة البيانات", "General", "فريق البحث", "2026-01-08", "2026-01-18", 0, 100, 0, "Not Started"],
        
        # المحتوى
        ["T5", "P_REPORTS", "كتابة محتوى تسويقي للمنصة", "المحتوى", "Content/Writing", "أثير", "2026-01-11", "2026-01-13", 0, 100, 50, "In Progress"],
        ["T6", "P_REPORTS", "كتابة تجربة المستخدم للمنصة", "المحتوى", "Content/Writing", "أثير", "2026-01-11", "2026-01-13", 0, 100, 70, "In Progress"],
        
        # التصاميم
        ["T7", "P_REPORTS", "تصميم المحتوى التسويقي للمنصة", "التصاميم", "Design/Execution", "يوسف", "2026-01-13", "2026-01-17", 0, 100, 0, "Not Started"],
        ["T8", "P_REPORTS", "تصميم تجربة المستخدم للمنصة", "التصاميم", "Design/Execution", "يوسف", "2026-01-13", "2026-01-17", 0, 100, 0, "Not Started"],
        
        # القانون
        ["T9", "P_REPORTS", "التواصل مع الجهة القانونية", "القانون", "General", "محمد الجديعي", "2026-01-11", "2026-01-20", 0, 100, 0, "Not Started"],
        ["T10", "P_REPORTS", "جلب والاتفاق", "القانون", "General", "محمد الجديعي", "2026-01-11", "2026-01-20", 0, 100, 0, "Not Started"],
        ["T11", "P_REPORTS", "دراسة المبرمجين وتوقيع الاتفاقية", "القانون", "General", "محمد الجديعي", "2026-01-11", "2026-01-20", 0, 100, 0, "Not Started"],
        ["T12", "P_REPORTS", "الدراسة الفنية والتوقيع والاتفاقية", "القانون", "General", "محمد الجديعي", "2026-01-11", "2026-01-20", 0, 100, 0, "Not Started"],
        ["T13", "P_REPORTS", "الاتفاقية الدولية للممول والشريك", "القانون", "General", "محمد الجديعي", "2026-01-11", "2026-01-20", 0, 100, 0, "Not Started"],
        
        # البرمجة
        ["T14", "P_REPORTS", "UX للمنصة", "البرمجة", "Design/Execution", "عبدالرحمن الأردني", "2026-01-08", "2026-01-17", 5000, 100, 50, "In Progress"],
        ["T15", "P_REPORTS", "تصميم واجهة الموقع بالتطبيقات", "البرمجة", "Design/Execution", "عبدالرحمن الأردني", "2026-01-15", "2026-01-29", 0, 100, 0, "Not Started"],
        ["T16", "P_REPORTS", "برمجة كود نظيف", "البرمجة", "Design/Execution", "عبدالرحمن الأردني", "2026-01-06", "2026-01-12", 0, 100, 100, "Completed"],
        ["T17", "P_REPORTS", "تضمين SEO من المبرمج", "البرمجة", "Design/Execution", "عبدالرحمن الأردني", "2026-01-11", "2026-01-20", 0, 100, 0, "Not Started"],
        
        # الشراكات (أ- محمد بارحمة)
        ["T18", "P_REPORTS", "التواصل مع قطاع التعليم", "الشراكات", "General", "أ- محمد بارحمة", "2026-01-11", "2026-01-22", 0, 100, 0, "Not Started"],
        ["T19", "P_REPORTS", "التواصل مع قطاع المال", "الشراكات", "General", "أ- محمد بارحمة", "2026-01-11", "2026-01-22", 0, 100, 0, "Not Started"],
        ["T20", "P_REPORTS", "التواصل مع قطاع الصحة", "الشراكات", "General", "أ- محمد بارحمة", "2026-01-11", "2026-01-22", 0, 100, 0, "Not Started"],
        ["T21", "P_REPORTS", "التواصل مع قطاع البنوك", "الشراكات", "General", "أ- محمد بارحمة", "2026-01-11", "2026-01-22", 0, 100, 0, "Not Started"],
        ["T22", "P_REPORTS", "الشركات مع الحكومة العربي", "الشراكات", "General", "أ- محمد بارحمة", "2026-01-11", "2026-01-22", 0, 100, 0, "Not Started"],
        ["T23", "P_REPORTS", "التواصل مع المجتمع المدني", "الشراكات", "General", "أ- محمد بارحمة", "2026-01-11", "2026-01-22", 0, 100, 0, "Not Started"],
        ["T24", "P_REPORTS", "توقيع الشراكة مع قطاع التعدين", "الشراكات", "General", "أ- محمد بارحمة", "2026-01-11", "2026-01-22", 0, 100, 0, "Not Started"],
        ["T25", "P_REPORTS", "توقيع الشراكة مع الصحة العالمية", "الشراكات", "General", "أ- محمد بارحمة", "2026-01-11", "2026-01-22", 0, 100, 0, "Not Started"],
        ["T26", "P_REPORTS", "مراجعة وتجهيز وثائق المشروع", "الشراكات", "General", "أ- محمد بارحمة", "2026-01-11", "2026-01-22", 0, 100, 0, "Not Started"],
        
        # إدارة المستخدمين
        ["T27", "P_REPORTS", "خطة إدارة المستخدمين", "إدارة المستخدمين", "General", "بشائر", "2026-01-10", "2026-01-12", 3000, 100, 0, "Not Started"],
        ["T28", "P_REPORTS", "تفعيل ميزات بروفايل المستخدمين", "إدارة المستخدمين", "General", "بشائر", "2026-01-10", "2026-01-12", 0, 100, 0, "Not Started"],
        ["T29", "P_REPORTS", "استقطاب الكادرات الفنية للمنصة", "إدارة المستخدمين", "General", "بشائر", "2026-01-12", "2026-01-16", 0, 100, 0, "Not Started"],
        
        # مراجعة ما قبل الإطلاق
        ["T30", "P_REPORTS", "مراجعة الهوية", "ما قبل الإطلاق", "General", "الهوية", "2026-01-21", "2026-01-21", 0, 100, 0, "Not Started"],
        ["T31", "P_REPORTS", "مراجعة المحتوى", "ما قبل الإطلاق", "General", "المحتوى", "2026-01-22", "2026-01-23", 0, 100, 0, "Not Started"],
        ["T32", "P_REPORTS", "مراجعة الأمان", "ما قبل الإطلاق", "General", "الأمان", "2026-01-26", "2026-01-27", 0, 100, 0, "Not Started"],
    ]
    
    tasks = pd.DataFrame(tasks_data, columns=[
        "Task_ID", "Project_ID", "Task", "Sub_Task", "Task_Category", 
        "Owner", "Start_Date", "End_Date", "Cost", "Quantity_Total", "Quantity_Done", "Status"
    ])

    # 3. Config (Dropdowns)
    config_data = [
        ["Team_Member", "عوض"], ["Team_Member", "فريق البحث"], ["Team_Member", "أثير"],
        ["Team_Member", "يوسف"], ["Team_Member", "محمد الجديعي"], ["Team_Member", "عبدالرحمن الأردني"],
        ["Team_Member", "أ- محمد بارحمة"], ["Team_Member", "بشائر"], ["Team_Member", "الهوية"],
        ["Team_Member", "المحتوى"], ["Team_Member", "الأمان"],
        ["Task_Category", "Content/Writing"], ["Task_Category", "Design/Execution"], ["Task_Category", "General"]
    ]
    config = pd.DataFrame(config_data, columns=["Type", "Value"])

    # 4. Others
    challenges = pd.DataFrame([{"Challenge_ID": "C1", "Project_ID": "P_REPORTS", "Description": "تأخر الاتفاقيات الدولية", "Status": "Open", "Owner": "محمد الجديعي", "Resolution_Plan": "تصعيد للادارة", "Risk_Impact": "Medium", "Risk_Type": "Legal"}])
    users = pd.DataFrame([{"Username": "admin", "Name": "Awad", "Role": "Admin"}])
    docs = pd.DataFrame([{"Doc_ID": "D1", "Project_ID": "P_REPORTS", "Name": "Design Doc", "Link_URL": "#"}])

    with pd.ExcelWriter("mock_data.xlsx") as writer:
        projects.to_excel(writer, sheet_name="Projects", index=False)
        tasks.to_excel(writer, sheet_name="Tasks", index=False)
        config.to_excel(writer, sheet_name="Config", index=False)
        challenges.to_excel(writer, sheet_name="Challenges", index=False)
        users.to_excel(writer, sheet_name="App_Users", index=False)
        docs.to_excel(writer, sheet_name="Documents", index=False)

    print("Successfully updated with Arabic Reporting Platform data!")

if __name__ == "__main__":
    create_real_data()
