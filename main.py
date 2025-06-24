import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, scrolledtext
import sqlite3
import hashlib
import datetime
import os
import re
from PIL import Image, ImageTk
import sv_ttk

class ModernCustomerManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("凯川矿客户管理系统 V1.0")
        self.root.geometry("1200x700")
        self.root.minsize(1000, 600)
        
        # 应用现代主题
        sv_ttk.set_theme("light")
        
        # 自定义样式
        self.setup_styles()
        
        # 确保数据目录存在
        if not os.path.exists("data"):
            os.makedirs("data")
            
        # 初始化数据库
        self.conn = sqlite3.connect("data/customer_data.db")
        self.create_tables()
        
        # 检查是否有管理员账户，没有则创建
        self.check_admin_account()
        
        # 初始显示登录界面
        self.show_login_page()
    
    def setup_styles(self):
        """设置自定义样式"""
        style = ttk.Style()
        
        # 标题样式
        style.configure("Title.TLabel", font=("Arial", 24, "bold"), foreground="#2c3e50")
        
        # 卡片样式
        style.configure("Card.TFrame", background="white", borderwidth=1, relief="solid")
        style.configure("CardHeader.TLabel", font=("Arial", 14, "bold"), foreground="#2c3e50", background="white")
        style.configure("CardValue.TLabel", font=("Arial", 24, "bold"), background="white")
        
        # 按钮样式
        style.configure("Accent.TButton", font=("Arial", 10), foreground="white", background="#3498db")
        style.map("Accent.TButton", background=[("active", "#2980b9")])
        
        # 表格样式
        style.configure("Treeview", font=("Arial", 10), rowheight=25)
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
        
        # 导航按钮样式
        style.configure("Nav.TButton", font=("Arial", 10), padding=10)
        style.map("Nav.TButton", background=[("active", "#ecf0f1")])
    
    def create_tables(self):
        """创建数据库表"""
        cursor = self.conn.cursor()
        
        # 用户表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
        ''')
        
        # 客户表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY,
            company_name TEXT NOT NULL,
            contact_name TEXT NOT NULL,
            phone TEXT NOT NULL,
            customer_type TEXT NOT NULL,
            notes TEXT,
            registration_date TEXT NOT NULL
        )
        ''')
        
        self.conn.commit()
    
    def check_admin_account(self):
        """检查并创建管理员账户"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", ("jirowang",))
        if cursor.fetchone() is None:
            # 创建管理员账户
            password_hash = self.hash_password("123456")
            cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", 
                          ("jirowang", password_hash))
            self.conn.commit()
    
    def hash_password(self, password):
        """哈希密码"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password, hashed_password):
        """验证密码"""
        return self.hash_password(password) == hashed_password
    
    def show_login_page(self):
        """显示登录页面"""
        # 清除当前窗口
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # 创建主框架
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # 左侧装饰面板
        left_panel = ttk.Frame(main_frame, width=300)
        left_panel.pack(side="left", fill="y", padx=(0, 20))
        
        # 装饰性标题
        title_label = ttk.Label(left_panel, text="凯川矿客户管理系统", style="Title.TLabel")
        title_label.pack(pady=20)
        
        # 装饰性图像
        try:
            # 这里使用一个简单的颜色块代替图像
            color_block = tk.Canvas(left_panel, bg="#3498db", width=250, height=150)
            color_block.create_text(125, 75, text="凯川矿客户管理系统", font=("Arial", 14, "bold"), fill="white")
            color_block.pack(pady=20)
        except:
            pass
        
        # 系统信息
        info_text = "高效管理煤炭行业客户信息\n\n- 客户分类管理\n- 客户统计分析\n- 系统安全管理"
        info_label = ttk.Label(left_panel, text=info_text, justify="left")
        info_label.pack(pady=20, fill="x")
        
        # 右侧登录表单
        login_frame = ttk.LabelFrame(main_frame, text="用户登录", width=400)
        login_frame.pack(side="right", fill="both", expand=True)
        
        # 表单内容
        form_frame = ttk.Frame(login_frame)
        form_frame.pack(padx=40, pady=40, fill="x")
        
        ttk.Label(form_frame, text="用户名:", font=("Arial", 11)).grid(row=0, column=0, sticky="w", pady=10)
        username_entry = ttk.Entry(form_frame, width=30)
        username_entry.grid(row=0, column=1, sticky="ew", pady=10, padx=(10, 0))
        
        ttk.Label(form_frame, text="密码:", font=("Arial", 11)).grid(row=1, column=0, sticky="w", pady=10)
        password_entry = ttk.Entry(form_frame, width=30, show="*")
        password_entry.grid(row=1, column=1, sticky="ew", pady=10, padx=(10, 0))
        
        # 登录按钮
        def login():
            username = username_entry.get()
            password = password_entry.get()
            
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            user = cursor.fetchone()
            
            if user and self.verify_password(password, user[2]):
                messagebox.showinfo("登录成功", f"欢迎回来，{username}！")
                self.show_main_page()
            else:
                messagebox.showerror("登录失败", "用户名或密码错误")
        
        login_button = ttk.Button(form_frame, text="登录", command=login, style="Accent.TButton", width=15)
        login_button.grid(row=2, column=0, columnspan=2, pady=20)
        
        # 设置焦点到用户名输入框
        username_entry.focus()
        
        # 绑定回车键到登录函数
        self.root.bind('<Return>', lambda event: login())
    
    def show_main_page(self):
        """显示主页面"""
        # 清除当前窗口
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # 创建主布局
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True)
        
        # 顶部导航栏
        navbar = ttk.Frame(main_frame, height=50, style="Card.TFrame")
        navbar.pack(fill="x", padx=20, pady=(20, 10))
        
        # 系统标题
        title_label = ttk.Label(navbar, text="凯川矿客户管理系统", font=("Arial", 14, "bold"))
        title_label.pack(side="left", padx=20)
        
        # 导航按钮
        buttons = [
            ("首页", self.show_dashboard),
            ("客户管理", self.show_customer_management),
            ("系统设置", self.show_system_settings)
        ]
        
        button_frame = ttk.Frame(navbar)
        button_frame.pack(side="right", padx=20)
        
        for text, command in buttons:
            btn = ttk.Button(button_frame, text=text, command=command, style="Nav.TButton")
            btn.pack(side="left", padx=5)
        
        # 搜索栏
        search_frame = ttk.Frame(main_frame, height=40)
        search_frame.pack(fill="x", padx=20, pady=10)
        
        ttk.Label(search_frame, text="搜索:").pack(side="left", padx=5)
        
        self.search_entry = ttk.Entry(search_frame, width=30)
        self.search_entry.pack(side="left", padx=5)
        
        # 添加客户类型筛选
        ttk.Label(search_frame, text="客户类型:").pack(side="left", padx=5)
        
        self.customer_type_var = tk.StringVar()
        customer_type_combobox = ttk.Combobox(
            search_frame, 
            textvariable=self.customer_type_var, 
            values=["所有", "精煤", "中煤"],
            state="readonly",
            width=10
        )
        customer_type_combobox.pack(side="left", padx=5)
        customer_type_combobox.current(0)  # 默认选择"所有"
        
        search_button = ttk.Button(search_frame, text="搜索", command=self.perform_search, width=10)
        search_button.pack(side="left", padx=5)
        
        reset_button = ttk.Button(search_frame, text="重置", command=self.reset_search, width=10)
        reset_button.pack(side="left", padx=5)
        
        # 创建主内容区域
        self.content_frame = ttk.Frame(main_frame)
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # 默认显示首页
        self.show_dashboard()
    
    def show_dashboard(self):
        """显示首页仪表盘"""
        # 清除当前内容
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # 创建标题
        ttk.Label(self.content_frame, text="数据概览", style="Title.TLabel").pack(pady=(0, 20), anchor="w")
        
        # 创建统计卡片框架
        stats_frame = ttk.Frame(self.content_frame)
        stats_frame.pack(fill="x", pady=10)
        
        # 客户总数
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM customers")
        total_customers = cursor.fetchone()[0]
        
        # 精煤客户数
        cursor.execute("SELECT COUNT(*) FROM customers WHERE customer_type = ?", ("精煤",))
        jingmei_count = cursor.fetchone()[0]
        
        # 中煤客户数
        cursor.execute("SELECT COUNT(*) FROM customers WHERE customer_type = ?", ("中煤",))
        zhongmei_count = cursor.fetchone()[0]
        
        # 创建统计卡片
        stats = [
            {"title": "总客户数", "value": total_customers, "color": "#3498db"},
            {"title": "精煤客户", "value": jingmei_count, "color": "#e74c3c"},
            {"title": "中煤客户", "value": zhongmei_count, "color": "#2ecc71"}
        ]
        
        for stat in stats:
            card = ttk.Frame(stats_frame, style="Card.TFrame")
            card.pack(side="left", fill="both", expand=True, padx=10, ipady=10)
            
            ttk.Label(card, text=stat["title"], style="CardHeader.TLabel").pack(pady=5)
            ttk.Label(card, text=str(stat["value"]), style="CardValue.TLabel", 
                     foreground=stat["color"]).pack(pady=10)
        
        # 最近添加的客户
        recent_frame = ttk.LabelFrame(self.content_frame, text="最近添加的客户")
        recent_frame.pack(fill="both", expand=True, pady=20)
        
        # 创建表格
        columns = ("id", "公司名称", "客户名称", "联系电话", "客户类型", "登记日期")
        self.recent_tree = ttk.Treeview(recent_frame, columns=columns, show="headings", selectmode="browse")
        
        for col in columns:
            self.recent_tree.heading(col, text=col)
            self.recent_tree.column(col, width=120, anchor="center")
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(recent_frame, orient="vertical", command=self.recent_tree.yview)
        self.recent_tree.configure(yscroll=scrollbar.set)
        
        self.recent_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # 加载最近5个客户
        cursor.execute("SELECT id, company_name, contact_name, phone, customer_type, registration_date FROM customers ORDER BY id DESC LIMIT 5")
        for row in cursor.fetchall():
            self.recent_tree.insert("", "end", values=row)
    
    def show_customer_management(self):
        """显示客户管理页面"""
        # 清除当前内容
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # 创建标题和按钮
        header_frame = ttk.Frame(self.content_frame)
        header_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(header_frame, text="客户管理", style="Title.TLabel").pack(side="left")
        
        button_frame = ttk.Frame(header_frame)
        button_frame.pack(side="right")
        
        ttk.Button(button_frame, text="添加客户", command=self.add_customer, 
                  style="Accent.TButton").pack(side="left", padx=5)
        ttk.Button(button_frame, text="编辑客户", command=self.edit_customer, 
                  style="Accent.TButton").pack(side="left", padx=5)
        ttk.Button(button_frame, text="删除客户", command=self.delete_customer, 
                  style="Accent.TButton").pack(side="left", padx=5)
        
        # 创建表格
        table_frame = ttk.Frame(self.content_frame)
        table_frame.pack(fill="both", expand=True)
        
        # 修改列名：备注替换注册日期
        columns = ("id", "公司名称", "客户名称", "联系电话", "客户类型", "备注")
        self.customer_tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")
        
        for col in columns:
            self.customer_tree.heading(col, text=col)
            self.customer_tree.column(col, width=120, anchor="center")
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.customer_tree.yview)
        self.customer_tree.configure(yscroll=scrollbar.set)
        
        self.customer_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # 加载客户数据
        self.load_customer_data()
    
    def load_customer_data(self):
        """加载客户数据到表格"""
        # 清空表格
        for item in self.customer_tree.get_children():
            self.customer_tree.delete(item)
        
        # 获取搜索条件
        search_text = self.search_entry.get().strip().lower()
        customer_type = self.customer_type_var.get()
        
        cursor = self.conn.cursor()
        
        # 构建SQL查询，显示 notes 而非 registration_date
        query = "SELECT id, company_name, contact_name, phone, customer_type, notes FROM customers"
        conditions = []
        params = []
        
        if search_text:
            conditions.append("(LOWER(company_name) LIKE ? OR LOWER(contact_name) LIKE ?)")
            params.extend([f"%{search_text}%", f"%{search_text}%"])
        
        if customer_type != "所有":
            conditions.append("customer_type = ?")
            params.append(customer_type)
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        query += " ORDER BY id DESC"
        
        cursor.execute(query, params)
        
        # 客户类型颜色映射
        type_colors = {
            "精煤": "#e74c3c",  # 红色
            "中煤": "#2ecc71"   # 绿色
        }
        
        for row in cursor.fetchall():
            item = self.customer_tree.insert("", "end", values=row)
            ctype = row[4]
            if ctype in type_colors:
                self.customer_tree.tag_configure(ctype, foreground=type_colors[ctype])
                self.customer_tree.item(item, tags=(ctype,))
    
    def add_customer(self):
        """添加新客户"""
        dialog = tk.Toplevel(self.root)
        dialog.title("添加新客户")
        dialog.geometry("500x500")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        form_frame = ttk.Frame(dialog)
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        fields = []
        
        # 公司名称
        company_frame = ttk.Frame(form_frame)
        company_frame.pack(fill="x", pady=5)
        ttk.Label(company_frame, text="公司名称*:").pack(side="left", padx=5)
        company_var = tk.StringVar()
        company_entry = ttk.Entry(company_frame, textvariable=company_var, width=30)
        company_entry.pack(side="right", fill="x", expand=True)
        fields.append(("company_name", company_var))
        
        # 客户名称
        contact_frame = ttk.Frame(form_frame)
        contact_frame.pack(fill="x", pady=5)
        ttk.Label(contact_frame, text="客户名称*:").pack(side="left", padx=5)
        contact_var = tk.StringVar()
        contact_entry = ttk.Entry(contact_frame, textvariable=contact_var, width=30)
        contact_entry.pack(side="right", fill="x", expand=True)
        fields.append(("contact_name", contact_var))
        
        # 联系电话
        phone_frame = ttk.Frame(form_frame)
        phone_frame.pack(fill="x", pady=5)
        ttk.Label(phone_frame, text="联系电话*:").pack(side="left", padx=5)
        phone_var = tk.StringVar()
        phone_entry = ttk.Entry(phone_frame, textvariable=phone_var, width=30)
        phone_entry.pack(side="right", fill="x", expand=True)
        fields.append(("phone", phone_var))
        
        # 客户类型
        type_frame = ttk.Frame(form_frame)
        type_frame.pack(fill="x", pady=5)
        ttk.Label(type_frame, text="客户类型*:").pack(side="left", padx=5)
        type_var = tk.StringVar()
        type_combobox = ttk.Combobox(type_frame, textvariable=type_var, 
                                    values=["精煤", "中煤"], state="readonly", width=28)
        type_combobox.current(0)
        type_combobox.pack(side="right", fill="x", expand=True)
        fields.append(("customer_type", type_var))
        
        # 备注
        notes_frame = ttk.Frame(form_frame)
        notes_frame.pack(fill="x", pady=5)
        ttk.Label(notes_frame, text="备注:").pack(side="left", padx=5, anchor="n")
        notes_text = scrolledtext.ScrolledText(notes_frame, width=30, height=5)
        notes_text.pack(side="right", fill="x", expand=True)
        fields.append(("notes", notes_text))
        
        button_frame = ttk.Frame(form_frame)
        button_frame.pack(fill="x", pady=20)
        
        def save_customer():
            data = {}
            for name, field in fields:
                if name == "notes":
                    data[name] = field.get("1.0", tk.END).strip()
                else:
                    data[name] = field.get().strip()
            
            if not data["company_name"] or not data["contact_name"] or not data["phone"]:
                messagebox.showerror("错误", "公司名称、客户名称和联系电话不能为空")
                return
            
            if not re.match(r'^1[3-9]\d{9}$', data["phone"]):
                messagebox.showerror("错误", "请输入有效的手机号码")
                return
            
            reg_date = datetime.datetime.now().strftime("%Y-%m-%d")
            
            cursor = self.conn.cursor()
            cursor.execute("""
            INSERT INTO customers (company_name, contact_name, phone, customer_type, notes, registration_date)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (data["company_name"], data["contact_name"], data["phone"], 
                 data["customer_type"], data["notes"], reg_date))
            self.conn.commit()
            
            messagebox.showinfo("成功", "客户添加成功")
            dialog.destroy()
            self.load_customer_data()
        
        save_button = ttk.Button(button_frame, text="保存", command=save_customer, style="Accent.TButton")
        save_button.pack(side="right", padx=5)
        cancel_button = ttk.Button(button_frame, text="取消", command=dialog.destroy)
        cancel_button.pack(side="right", padx=5)
    
    def edit_customer(self):
        """编辑选中的客户"""
        selected_item = self.customer_tree.selection()
        if not selected_item:
            messagebox.showinfo("提示", "请先选择要编辑的客户")
            return
        
        item = selected_item[0]
        customer_id = self.customer_tree.item(item, "values")[0]
        
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM customers WHERE id = ?", (customer_id,))
        customer_data = cursor.fetchone()
        
        dialog = tk.Toplevel(self.root)
        dialog.title("编辑客户信息")
        dialog.geometry("500x500")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        form_frame = ttk.Frame(dialog)
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        fields = []
        
        company_frame = ttk.Frame(form_frame)
        company_frame.pack(fill="x", pady=5)
        ttk.Label(company_frame, text="公司名称*:").pack(side="left", padx=5)
        company_var = tk.StringVar(value=customer_data[1])
        company_entry = ttk.Entry(company_frame, textvariable=company_var, width=30)
        company_entry.pack(side="right", fill="x", expand=True)
        fields.append(("company_name", company_var))
        
        contact_frame = ttk.Frame(form_frame)
        contact_frame.pack(fill="x", pady=5)
        ttk.Label(contact_frame, text="客户名称*:").pack(side="left", padx=5)
        contact_var = tk.StringVar(value=customer_data[2])
        contact_entry = ttk.Entry(contact_frame, textvariable=contact_var, width=30)
        contact_entry.pack(side="right", fill="x", expand=True)
        fields.append(("contact_name", contact_var))
        
        phone_frame = ttk.Frame(form_frame)
        phone_frame.pack(fill="x", pady=5)
        ttk.Label(phone_frame, text="联系电话*:").pack(side="left", padx=5)
        phone_var = tk.StringVar(value=customer_data[3])
        phone_entry = ttk.Entry(phone_frame, textvariable=phone_var, width=30)
        phone_entry.pack(side="right", fill="x", expand=True)
        fields.append(("phone", phone_var))
        
        type_frame = ttk.Frame(form_frame)
        type_frame.pack(fill="x", pady=5)
        ttk.Label(type_frame, text="客户类型*:").pack(side="left", padx=5)
        type_var = tk.StringVar(value=customer_data[4])
        type_combobox = ttk.Combobox(type_frame, textvariable=type_var, 
                                    values=["精煤", "中煤"], state="readonly", width=28)
        type_combobox.pack(side="right", fill="x", expand=True)
        fields.append(("customer_type", type_var))
        
        date_frame = ttk.Frame(form_frame)
        date_frame.pack(fill="x", pady=5)
        ttk.Label(date_frame, text="登记日期:").pack(side="left", padx=5)
        date_var = tk.StringVar(value=customer_data[5])
        date_entry = ttk.Entry(date_frame, textvariable=date_var, state="readonly", width=30)
        date_entry.pack(side="right", fill="x", expand=True)
        
        notes_frame = ttk.Frame(form_frame)
        notes_frame.pack(fill="x", pady=5)
        ttk.Label(notes_frame, text="备注:").pack(side="left", padx=5, anchor="n")
        notes_text = scrolledtext.ScrolledText(notes_frame, width=30, height=5)
        notes_text.insert("1.0", customer_data[6] or "")
        notes_text.pack(side="right", fill="x", expand=True)
        fields.append(("notes", notes_text))
        
        button_frame = ttk.Frame(form_frame)
        button_frame.pack(fill="x", pady=20)
        
        def update_customer():
            data = {}
            for name, field in fields:
                if name == "notes":
                    data[name] = field.get("1.0", tk.END).strip()
                else:
                    data[name] = field.get().strip()
            
            if not data["company_name"] or not data["contact_name"] or not data["phone"]:
                messagebox.showerror("错误", "公司名称、客户名称和联系电话不能为空")
                return
            
            if not re.match(r'^1[3-9]\d{9}$', data["phone"]):
                messagebox.showerror("错误", "请输入有效的手机号码")
                return
            
            cursor = self.conn.cursor()
            cursor.execute("""
            UPDATE customers 
            SET company_name = ?, contact_name = ?, phone = ?, customer_type = ?, notes = ?
            WHERE id = ?
            """, (data["company_name"], data["contact_name"], data["phone"], 
                 data["customer_type"], data["notes"], customer_id))
            self.conn.commit()
            
            messagebox.showinfo("成功", "客户信息更新成功")
            dialog.destroy()
            self.load_customer_data()
        
        save_button = ttk.Button(button_frame, text="保存", command=update_customer, style="Accent.TButton")
        save_button.pack(side="right", padx=5)
        cancel_button = ttk.Button(button_frame, text="取消", command=dialog.destroy)
        cancel_button.pack(side="right", padx=5)
    
    def delete_customer(self):
        """删除选中的客户"""
        selected_item = self.customer_tree.selection()
        if not selected_item:
            messagebox.showinfo("提示", "请先选择要删除的客户")
            return
        
        item = selected_item[0]
        customer_id = self.customer_tree.item(item, "values")[0]
        company_name = self.customer_tree.item(item, "values")[1]
        
        if messagebox.askyesno("确认删除", f"确定要删除客户 '{company_name}' 吗？"):
            try:
                cursor = self.conn.cursor()
                cursor.execute("DELETE FROM customers WHERE id = ?", (customer_id,))
                self.conn.commit()
                
                messagebox.showinfo("成功", "客户已删除")
                self.load_customer_data()
            except Exception as e:
                messagebox.showerror("错误", f"删除失败: {str(e)}")
    
    def show_system_settings(self):
        """显示系统设置页面"""
        # 清除当前内容
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        ttk.Label(self.content_frame, text="系统设置", style="Title.TLabel").pack(anchor="w", pady=(0, 20))
        
        settings_frame = ttk.LabelFrame(self.content_frame, text="系统管理")
        settings_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ttk.Button(settings_frame, text="更改管理员密码", command=self.change_admin_password, 
                  width=20).pack(anchor="w", padx=20, pady=10)
        ttk.Button(settings_frame, text="备份数据库", command=self.backup_database, 
                  width=20).pack(anchor="w", padx=20, pady=10)
        ttk.Button(settings_frame, text="恢复数据库", command=self.restore_database, 
                  width=20).pack(anchor="w", padx=20, pady=10)
        
        info_frame = ttk.LabelFrame(self.content_frame, text="系统信息")
        info_frame.pack(fill="x", padx=10, pady=10)
        
        info_text = (
            "凯川矿客户管理系统 v1.0\n\n"
            "开发人员: 王杰\n"
            "开发日期: 2025-06-24\n"
            "数据库位置: data/customer_data.db"
        )
        
        ttk.Label(info_frame, text=info_text, justify="left").pack(padx=20, pady=20)
    
    def change_admin_password(self):
        """更改管理员密码"""
        current_password = simpledialog.askstring("密码验证", "请输入当前密码:", show='*', parent=self.root)
        if current_password is None:
            return
        
        cursor = self.conn.cursor()
        cursor.execute("SELECT password_hash FROM users WHERE username = ?", ("jirowang",))
        result = cursor.fetchone()
        if not result or not self.verify_password(current_password, result[0]):
            messagebox.showerror("错误", "当前密码不正确")
            return
        
        new_password = simpledialog.askstring("更改密码", "请输入新密码:", show='*', parent=self.root)
        if new_password is None:
            return
        confirm_password = simpledialog.askstring("更改密码", "请再次输入新密码:", show='*', parent=self.root)
        if confirm_password is None:
            return
        if new_password != confirm_password:
            messagebox.showerror("错误", "两次输入的新密码不一致")
            return
        
        password_hash = self.hash_password(new_password)
        cursor.execute("UPDATE users SET password_hash = ? WHERE username = ?", (password_hash, "jirowang"))
        self.conn.commit()
        messagebox.showinfo("成功", "密码已更新")
    
    def backup_database(self):
        """备份数据库"""
        try:
            if not os.path.exists("data/backups"):
                os.makedirs("data/backups")
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = f"data/backups/customer_data_backup_{timestamp}.db"
            backup_conn = sqlite3.connect(backup_file)
            with backup_conn:
                self.conn.backup(backup_conn)
            messagebox.showinfo("成功", f"数据库备份成功，备份文件位于: {backup_file}")
        except Exception as e:
            messagebox.showerror("错误", f"备份失败: {str(e)}")
    
    def restore_database(self):
        """恢复数据库"""
        if not messagebox.askyesno("确认恢复", "恢复数据库将覆盖当前数据，是否继续？"):
            return
        try:
            backup_dir = "data/backups"
            if not os.path.exists(backup_dir) or not os.listdir(backup_dir):
                messagebox.showinfo("提示", "没有找到备份文件")
                return
            backup_files = [f for f in os.listdir(backup_dir) if f.endswith(".db")]
            backup_file = simpledialog.askstring("恢复数据库", "请输入要恢复的备份文件名:\n" + "\n".join(backup_files), parent=self.root)
            if not backup_file:
                return
            backup_path = os.path.join(backup_dir, backup_file)
            if not os.path.exists(backup_path):
                messagebox.showerror("错误", "指定的备份文件不存在")
                return
            self.conn.close()
            if os.path.exists("data/customer_data.db"):
                os.remove("data/customer_data.db")
            import shutil
            shutil.copy2(backup_path, "data/customer_data.db")
            messagebox.showinfo("成功", "数据库恢复成功")
        except Exception as e:
            messagebox.showerror("错误", f"恢复失败: {str(e)}")
        finally:
            self.conn = sqlite3.connect("data/customer_data.db")
            if hasattr(self, 'customer_tree'):
                self.load_customer_data()
            self.show_dashboard()
    
    def perform_search(self):
        """执行搜索"""
        # 直接刷新客户列表，无需跳转页面
        self.load_customer_data()
    
    def reset_search(self):
        """重置搜索"""
        self.search_entry.delete(0, tk.END)
        self.customer_type_var.set("所有")
        self.perform_search()

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernCustomerManagementSystem(root)
    root.mainloop()
