"""
직원(Employee) DocType 정의
ERPNext의 Employee와 동일한 구조
"""
from sqlalchemy import Column, String, Integer, Float, Text, Boolean, DateTime, Date
from core.doctype.base import DocTypeBase, Base, DocTypeMeta, register_doctype
from datetime import datetime


class Employee(DocTypeBase, Base):
    """직원 마스터"""
    
    __tablename__ = 'tabEmployee'
    
    # 기본 정보
    employee_name = Column(String(100), nullable=False)
    first_name = Column(String(50), nullable=False)
    middle_name = Column(String(50))
    last_name = Column(String(50))
    
    # 개인 정보
    gender = Column(String(10))
    date_of_birth = Column(Date)
    blood_group = Column(String(5))
    marital_status = Column(String(20))
    
    # 연락처 정보
    cell_number = Column(String(20))
    personal_email = Column(String(140))
    current_address = Column(Text)
    permanent_address = Column(Text)
    
    # 회사 정보
    company = Column(String(140), nullable=False)
    employee_number = Column(String(50))
    employment_type = Column(String(50))
    status = Column(String(50), default='Active')
    
    # 부서 및 직급
    department = Column(String(140))
    designation = Column(String(140))
    branch = Column(String(140))
    reports_to = Column(String(140))  # 상급자
    
    # 입사 정보
    date_of_joining = Column(Date, nullable=False)
    final_confirmation_date = Column(Date)
    contract_end_date = Column(Date)
    notice_number_of_days = Column(Integer, default=30)
    
    # 퇴사 정보
    relieving_date = Column(Date)
    reason_for_leaving = Column(String(140))
    leave_encashed = Column(Boolean, default=False)
    encashment_date = Column(Date)
    
    # 급여 정보
    salary_mode = Column(String(50), default='Bank')
    payroll_cost_center = Column(String(140))
    
    # 은행 정보
    bank_name = Column(String(140))
    bank_ac_no = Column(String(50))
    
    # 세금 정보
    pan_number = Column(String(20))
    
    # 사용자 권한
    user_id = Column(String(140))  # User 계정과 연결
    
    # 상태
    disabled = Column(Boolean, default=False)
    
    def get_required_fields(self):
        return ['employee_name', 'first_name', 'company', 'date_of_joining']
    
    def validate(self):
        errors = super().validate()
        
        # 생년월일 검증
        if self.date_of_birth:
            if self.date_of_birth >= datetime.now().date():
                errors.append("생년월일은 현재 날짜보다 이전이어야 합니다.")
        
        # 입사일과 퇴사일 검증
        if self.relieving_date and self.date_of_joining:
            if self.relieving_date <= self.date_of_joining:
                errors.append("퇴사일은 입사일보다 이후여야 합니다.")
        
        # 이메일 유효성 검사
        if self.personal_email:
            import re
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, self.personal_email):
                errors.append("올바른 이메일 주소를 입력하세요.")
        
        return errors


class Attendance(DocTypeBase, Base):
    """출근 기록"""
    
    __tablename__ = 'tabAttendance'
    
    # 기본 정보
    employee = Column(String(140), nullable=False)
    employee_name = Column(String(140))
    attendance_date = Column(Date, nullable=False)
    
    # 출근 정보
    status = Column(String(20), nullable=False)  # Present, Absent, Half Day
    in_time = Column(DateTime)
    out_time = Column(DateTime)
    
    # 근무 시간
    working_hours = Column(Float, default=0)
    late_entry = Column(Boolean, default=False)
    early_exit = Column(Boolean, default=False)
    
    # 회사 정보
    company = Column(String(140))
    department = Column(String(140))
    
    # 승인 정보
    leave_type = Column(String(140))
    leave_application = Column(String(140))
    
    def get_required_fields(self):
        return ['employee', 'attendance_date', 'status']
    
    def validate(self):
        errors = super().validate()
        
        # 퇴근 시간이 출근 시간보다 이른지 확인
        if self.in_time and self.out_time:
            if self.out_time <= self.in_time:
                errors.append("퇴근 시간은 출근 시간보다 늦어야 합니다.")
        
        return errors


class SalaryStructure(DocTypeBase, Base):
    """급여 구조"""
    
    __tablename__ = 'tabSalaryStructure'
    
    # 기본 정보
    name = Column(String(140), primary_key=True, nullable=False)
    employee = Column(String(140), nullable=False)
    employee_name = Column(String(140))
    
    # 급여 정보
    from_date = Column(Date, nullable=False)
    to_date = Column(Date)
    base = Column(Float, default=0)
    variable = Column(Float, default=0)
    total_earning = Column(Float, default=0)
    total_deduction = Column(Float, default=0)
    net_pay = Column(Float, default=0)
    
    # 회사 정보
    company = Column(String(140))
    department = Column(String(140))
    designation = Column(String(140))
    
    # 상태
    is_active = Column(String(10), default='Yes')
    
    def get_required_fields(self):
        return ['employee', 'from_date']


# Employee DocType 메타데이터
employee_meta = DocTypeMeta({
    "name": "Employee",
    "module": "HR",
    "autoname": "naming_series:",
    "title_field": "employee_name",
    "search_fields": ["employee_name", "employee_number", "department"],
    "sort_field": "employee_name",
    "sort_order": "ASC",
    "fields": [
        {
            "fieldname": "employee_name",
            "fieldtype": "Data",
            "label": "직원명",
            "reqd": 1,
            "length": 100
        },
        {
            "fieldname": "first_name",
            "fieldtype": "Data",
            "label": "성",
            "reqd": 1,
            "length": 50
        },
        {
            "fieldname": "middle_name",
            "fieldtype": "Data",
            "label": "중간명",
            "length": 50
        },
        {
            "fieldname": "last_name",
            "fieldtype": "Data",
            "label": "이름",
            "length": 50
        },
        {
            "fieldname": "gender",
            "fieldtype": "Select",
            "label": "성별",
            "options": "Male\nFemale\nOther"
        },
        {
            "fieldname": "date_of_birth",
            "fieldtype": "Date",
            "label": "생년월일"
        },
        {
            "fieldname": "blood_group",
            "fieldtype": "Select",
            "label": "혈액형",
            "options": "A+\nA-\nB+\nB-\nAB+\nAB-\nO+\nO-"
        },
        {
            "fieldname": "marital_status",
            "fieldtype": "Select",
            "label": "결혼상태",
            "options": "Single\nMarried\nDivorced\nWidowed"
        },
        {
            "fieldname": "cell_number",
            "fieldtype": "Data",
            "label": "휴대폰",
            "length": 20
        },
        {
            "fieldname": "personal_email",
            "fieldtype": "Data",
            "label": "개인 이메일",
            "length": 140
        },
        {
            "fieldname": "current_address",
            "fieldtype": "Text",
            "label": "현재 주소"
        },
        {
            "fieldname": "company",
            "fieldtype": "Link",
            "label": "회사",
            "options": "Company",
            "reqd": 1
        },
        {
            "fieldname": "employee_number",
            "fieldtype": "Data",
            "label": "사번",
            "length": 50
        },
        {
            "fieldname": "employment_type",
            "fieldtype": "Link",
            "label": "고용 형태",
            "options": "Employment Type"
        },
        {
            "fieldname": "status",
            "fieldtype": "Select",
            "label": "상태",
            "options": "Active\nInactive\nSuspended\nLeft",
            "default": "Active"
        },
        {
            "fieldname": "department",
            "fieldtype": "Link",
            "label": "부서",
            "options": "Department"
        },
        {
            "fieldname": "designation",
            "fieldtype": "Link",
            "label": "직급",
            "options": "Designation"
        },
        {
            "fieldname": "reports_to",
            "fieldtype": "Link",
            "label": "상급자",
            "options": "Employee"
        },
        {
            "fieldname": "date_of_joining",
            "fieldtype": "Date",
            "label": "입사일",
            "reqd": 1
        },
        {
            "fieldname": "final_confirmation_date",
            "fieldtype": "Date",
            "label": "정규직 전환일"
        },
        {
            "fieldname": "contract_end_date",
            "fieldtype": "Date",
            "label": "계약 만료일"
        },
        {
            "fieldname": "relieving_date",
            "fieldtype": "Date",
            "label": "퇴사일"
        },
        {
            "fieldname": "reason_for_leaving",
            "fieldtype": "Select",
            "label": "퇴사 사유",
            "options": "Better Prospects\nHealth Concerns\nHigher Studies\nImmigration\nMarriage\nNot Applicable\nOther\nRetirement\nTerminated\nUndisclosed\nWork Location"
        },
        {
            "fieldname": "salary_mode",
            "fieldtype": "Select",
            "label": "급여 지급 방식",
            "options": "Bank\nCash\nCheque",
            "default": "Bank"
        },
        {
            "fieldname": "bank_name",
            "fieldtype": "Data",
            "label": "은행명",
            "length": 140
        },
        {
            "fieldname": "bank_ac_no",
            "fieldtype": "Data",
            "label": "계좌번호",
            "length": 50
        },
        {
            "fieldname": "pan_number",
            "fieldtype": "Data",
            "label": "주민등록번호",
            "length": 20
        },
        {
            "fieldname": "user_id",
            "fieldtype": "Link",
            "label": "사용자 ID",
            "options": "User"
        },
        {
            "fieldname": "disabled",
            "fieldtype": "Check",
            "label": "비활성화",
            "default": 0
        }
    ],
    "permissions": [
        {
            "role": "HR User",
            "read": 1,
            "write": 1,
            "create": 1,
            "delete": 1
        },
        {
            "role": "HR Manager",
            "read": 1,
            "write": 1,
            "create": 1,
            "delete": 1,
            "cancel": 1
        },
        {
            "role": "Employee",
            "read": 1,
            "write": 0,
            "create": 0
        }
    ]
})

# Attendance DocType 메타데이터
attendance_meta = DocTypeMeta({
    "name": "Attendance",
    "module": "HR",
    "autoname": "naming_series:",
    "search_fields": ["employee", "employee_name", "attendance_date"],
    "sort_field": "attendance_date",
    "sort_order": "DESC",
    "is_submittable": 1,
    "fields": [
        {
            "fieldname": "employee",
            "fieldtype": "Link",
            "label": "직원",
            "options": "Employee",
            "reqd": 1
        },
        {
            "fieldname": "employee_name",
            "fieldtype": "Data",
            "label": "직원명",
            "read_only": 1,
            "length": 140
        },
        {
            "fieldname": "attendance_date",
            "fieldtype": "Date",
            "label": "출근일",
            "reqd": 1
        },
        {
            "fieldname": "status",
            "fieldtype": "Select",
            "label": "상태",
            "options": "Present\nAbsent\nHalf Day\nOn Leave\nWork From Home",
            "reqd": 1
        },
        {
            "fieldname": "in_time",
            "fieldtype": "Datetime",
            "label": "출근 시간"
        },
        {
            "fieldname": "out_time",
            "fieldtype": "Datetime",
            "label": "퇴근 시간"
        },
        {
            "fieldname": "working_hours",
            "fieldtype": "Float",
            "label": "근무 시간",
            "precision": 2
        },
        {
            "fieldname": "late_entry",
            "fieldtype": "Check",
            "label": "지각",
            "default": 0
        },
        {
            "fieldname": "early_exit",
            "fieldtype": "Check",
            "label": "조퇴",
            "default": 0
        },
        {
            "fieldname": "company",
            "fieldtype": "Link",
            "label": "회사",
            "options": "Company"
        }
    ],
    "permissions": [
        {
            "role": "HR User",
            "read": 1,
            "write": 1,
            "create": 1,
            "submit": 1,
            "cancel": 1
        },
        {
            "role": "Employee",
            "read": 1,
            "write": 1,
            "create": 1
        }
    ]
})

# DocType 등록
register_doctype("Employee", employee_meta, Employee)
register_doctype("Attendance", attendance_meta, Attendance)
register_doctype("Salary Structure", None, SalaryStructure)  # 간소화된 등록