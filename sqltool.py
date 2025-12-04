#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SQL工具 - 用于执行MySQL查询并返回结果
使用方法：python sqltool.py "SELECT * FROM table_name LIMIT 10"
"""

import sys
import json
import mysql.connector
from mysql.connector import Error
from tabulate import tabulate
import os

def load_config():
    """从config.json加载数据库配置"""
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"错误: 找不到配置文件 {config_path}")
        sys.exit(1)
    except json.JSONDecodeError:
        print("错误: 配置文件格式不正确")
        sys.exit(1)

def is_safe_query(sql):
    """
    检查SQL语句是否为安全的只读查询
    严格限制：只允许SELECT、SHOW、DESCRIBE、DESC、EXPLAIN等查询语句
    禁止：INSERT、UPDATE、DELETE、DROP、CREATE、ALTER、TRUNCATE等所有修改操作
    """
    sql_upper = sql.strip().upper()
    
    # 允许的只读操作
    allowed_keywords = ('SELECT', 'SHOW', 'DESCRIBE', 'DESC', 'EXPLAIN', 'USE')
    
    # 明确禁止的危险操作
    forbidden_keywords = (
        'INSERT', 'UPDATE', 'DELETE', 'DROP', 'CREATE', 'ALTER', 
        'TRUNCATE', 'RENAME', 'REPLACE', 'GRANT', 'REVOKE',
        'LOCK', 'UNLOCK', 'SET', 'COMMIT', 'ROLLBACK', 'START',
        'LOAD', 'IMPORT', 'CALL', 'EXECUTE', 'PREPARE'
    )
    
    # 检查是否以允许的关键字开头
    if not sql_upper.startswith(allowed_keywords):
        return False, "只允许执行查询语句 (SELECT, SHOW, DESCRIBE, DESC, EXPLAIN, USE)"
    
    # 检查是否包含禁止的关键字
    for keyword in forbidden_keywords:
        if keyword in sql_upper:
            return False, f"禁止执行包含 {keyword} 的语句！本工具仅供只读查询使用"
    
    return True, "OK"

def execute_sql(sql, config):
    """执行SQL语句并返回结果"""
    connection = None
    try:
        # 首先检查SQL是否安全
        is_safe, error_msg = is_safe_query(sql)
        if not is_safe:
            print(f"\n❌ 安全检查失败: {error_msg}")
            print("=" * 60)
            print("⚠️  安全规范:")
            print("   本工具仅允许执行只读查询操作")
            print("   允许: SELECT, SHOW, DESCRIBE, DESC, EXPLAIN, USE")
            print("   禁止: INSERT, UPDATE, DELETE, DROP, CREATE, ALTER 等")
            print("=" * 60)
            return None
        
        # 连接到MySQL数据库
        connection = mysql.connector.connect(
            host=config['host'],
            port=config['port'],
            user=config['user'],
            password=config['password'],
            database=config.get('database', ''),  # 可选的默认数据库
            charset='utf8mb4'
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # 执行SQL语句
            cursor.execute(sql)
            
            # 查询语句，获取结果
            rows = cursor.fetchall()
            
            if cursor.description:
                columns = [desc[0] for desc in cursor.description]
                
                if rows:
                    print(f"\n✅ 查询成功! 共返回 {len(rows)} 条记录:\n")
                    print(tabulate(rows, headers=columns, tablefmt='grid'))
                else:
                    print("\n✅ 查询成功! 但没有返回任何记录。")
            else:
                print("\n✅ 命令执行成功!")
            
            return rows
                
    except Error as e:
        print(f"\n数据库错误: {e}")
        return None
    except Exception as e:
        print(f"\n发生错误: {e}")
        return None
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def interactive_mode(config):
    """交互式模式 - 持续输入SQL并执行"""
    print("=" * 80)
    print("SQL工具 - 交互式模式 (只读查询)")
    print("=" * 80)
    print(f"已连接到: {config['host']}:{config['port']}")
    print()
    print("⚠️  安全限制: 本工具仅允许执行只读查询操作")
    print("   ✅ 允许: SELECT, SHOW, DESCRIBE, DESC, EXPLAIN, USE")
    print("   ❌ 禁止: INSERT, UPDATE, DELETE, DROP, CREATE, ALTER 等所有修改操作")
    print()
    print("输入 'exit' 或 'quit' 退出程序")
    print("输入 'help' 查看帮助")
    print("=" * 80)
    print()
    
    while True:
        try:
            sql = input("SQL> ").strip()
            
            if not sql:
                continue
                
            if sql.lower() in ['exit', 'quit']:
                print("再见!")
                break
                
            if sql.lower() == 'help':
                print_help()
                continue
            
            # 执行SQL
            execute_sql(sql, config)
            print()
            
        except KeyboardInterrupt:
            print("\n\n再见!")
            break
        except EOFError:
            print("\n再见!")
            break

def print_help():
    """打印帮助信息"""
    help_text = """
帮助信息:
---------
1. 输入SQL查询语句并按回车即可执行
2. 本工具仅支持只读查询操作（安全限制）
3. 输入 'exit' 或 'quit' 退出程序
4. 输入 'help' 查看本帮助信息

✅ 允许的操作:
--------------
- SELECT   : 查询数据
- SHOW     : 显示数据库/表/字段信息
- DESCRIBE : 查看表结构
- DESC     : 查看表结构（简写）
- EXPLAIN  : 查看SQL执行计划
- USE      : 切换数据库

❌ 禁止的操作:
--------------
- INSERT, UPDATE, DELETE : 数据修改操作
- DROP, CREATE, ALTER    : 结构修改操作
- TRUNCATE, RENAME       : 表操作
- GRANT, REVOKE          : 权限操作
- 以及其他所有可能修改数据的操作

示例:
-----
SELECT * FROM table_name LIMIT 10;
SHOW TABLES;
SHOW DATABASES;
DESCRIBE table_name;
SELECT COUNT(*) FROM table_name WHERE status = 'active';
USE database_name;
"""
    print(help_text)

def main():
    """主函数"""
    # 加载配置
    config = load_config()
    
    # 判断是单次执行模式还是交互式模式
    if len(sys.argv) > 1:
        # 单次执行模式 - 从命令行参数获取SQL
        sql = ' '.join(sys.argv[1:])
        execute_sql(sql, config)
    else:
        # 交互式模式
        interactive_mode(config)

if __name__ == "__main__":
    main()

