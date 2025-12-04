# SQL查询工具 (只读版本)

一个**严格限制为只读查询**的MySQL命令行工具，用于安全地执行SQL查询并查看结果。

## ⚠️ 重要安全规范 - 必读！

### 🚫 严格禁止的操作

**本工具已强制限制为只读查询，以下操作将被拒绝执行：**

- ❌ **INSERT** - 禁止插入数据
- ❌ **UPDATE** - 禁止更新数据
- ❌ **DELETE** - 禁止删除数据
- ❌ **DROP** - 禁止删除表/数据库
- ❌ **CREATE** - 禁止创建表/数据库
- ❌ **ALTER** - 禁止修改表结构
- ❌ **TRUNCATE** - 禁止清空表
- ❌ **RENAME** - 禁止重命名
- ❌ **REPLACE** - 禁止替换数据
- ❌ **GRANT/REVOKE** - 禁止权限操作
- ❌ **LOCK/UNLOCK** - 禁止锁表
- ❌ **SET** - 禁止设置变量
- ❌ **LOAD/IMPORT** - 禁止导入数据
- ❌ **CALL/EXECUTE** - 禁止执行存储过程

### ✅ 允许的操作

**只允许以下安全的只读查询操作：**

- ✅ **SELECT** - 查询数据
- ✅ **SHOW** - 显示数据库/表/字段信息
- ✅ **DESCRIBE** / **DESC** - 查看表结构
- ✅ **EXPLAIN** - 查看SQL执行计划
- ✅ **USE** - 切换数据库

## 🛡️ 安全机制

1. **代码级别强制检查**：所有SQL语句在执行前都会经过安全检查
2. **关键字黑名单**：自动拦截所有危险操作关键字
3. **白名单机制**：只允许明确列出的安全查询操作
4. **实时提示**：尝试执行禁止操作时会给出清晰的错误提示

## 功能特性

- ✅ 支持单次执行模式和交互式模式
- ✅ 自动格式化查询结果为表格
- ✅ 支持所有标准SELECT查询语法
- ✅ 安全的配置文件管理
- ✅ 中文友好的提示信息
- ✅ 严格的安全限制保护数据安全

## 安装依赖

```bash
pip install -r requirements.txt
```

或者手动安装：

```bash
pip install mysql-connector-python tabulate
```

## 配置

数据库连接信息已配置在 `config.json` 文件中：

```json
{
  "host": "master.shopee_ssc_lfs.mysql.cloud.test.shopee.io",
  "port": 6606,
  "user": "sz_sc_test2",
  "password": "6vJaoy5HHiPP0ms_sUnO",
  "database": ""
}
```

你可以修改 `database` 字段来设置默认数据库。

## 使用方法

### 方式一：交互式模式（推荐）

直接运行脚本进入交互式模式：

```bash
python3 sqltool.py
```

然后就可以持续输入SQL查询语句：

```
SQL> SHOW DATABASES;
SQL> USE your_database;
SQL> SELECT * FROM users LIMIT 10;
SQL> exit
```

### 方式二：单次执行模式

直接在命令行传入SQL语句：

```bash
python3 sqltool.py "SELECT * FROM table_name LIMIT 10"
python3 sqltool.py "SHOW TABLES"
python3 sqltool.py "SHOW DATABASES"
```

## 使用示例

### ✅ 正确示例（允许执行）

```sql
-- 查看所有数据库
SHOW DATABASES;

-- 使用某个数据库
USE database_name;

-- 查看当前数据库的所有表
SHOW TABLES;

-- 查看表结构
DESCRIBE table_name;
DESC table_name;

-- 查询数据
SELECT * FROM table_name LIMIT 10;

-- 条件查询
SELECT * FROM table_name WHERE id = 123;

-- 统计查询
SELECT COUNT(*) FROM table_name;

-- 复杂查询
SELECT 
    user_id, 
    COUNT(*) as order_count,
    SUM(amount) as total_amount
FROM orders 
WHERE status = 'completed'
GROUP BY user_id
ORDER BY total_amount DESC
LIMIT 100;

-- 多表关联查询
SELECT u.name, o.order_id, o.amount
FROM users u
INNER JOIN orders o ON u.id = o.user_id
WHERE o.created_at >= '2025-01-01'
LIMIT 50;

-- 查看执行计划
EXPLAIN SELECT * FROM table_name WHERE id = 123;
```

### ❌ 错误示例（将被拒绝）

```sql
-- 以下操作都会被拒绝执行：

UPDATE users SET status = 'active';        -- ❌ 禁止UPDATE
DELETE FROM orders WHERE id = 123;         -- ❌ 禁止DELETE
INSERT INTO users VALUES (1, 'test');      -- ❌ 禁止INSERT
DROP TABLE old_table;                      -- ❌ 禁止DROP
CREATE TABLE new_table (id INT);           -- ❌ 禁止CREATE
ALTER TABLE users ADD COLUMN age INT;      -- ❌ 禁止ALTER
TRUNCATE TABLE logs;                       -- ❌ 禁止TRUNCATE
```

### 🛑 安全拦截示例

当尝试执行禁止的操作时，会看到如下提示：

```
SQL> UPDATE users SET status = 'active';

❌ 安全检查失败: 禁止执行包含 UPDATE 的语句！本工具仅供只读查询使用
============================================================
⚠️  安全规范:
   本工具仅允许执行只读查询操作
   允许: SELECT, SHOW, DESCRIBE, DESC, EXPLAIN, USE
   禁止: INSERT, UPDATE, DELETE, DROP, CREATE, ALTER 等
============================================================
```

## 常用查询命令

```sql
-- 查看所有数据库
SHOW DATABASES;

-- 查看当前数据库
SELECT DATABASE();

-- 查看所有表
SHOW TABLES;

-- 查看表结构
DESCRIBE table_name;
SHOW CREATE TABLE table_name;

-- 查看表索引
SHOW INDEX FROM table_name;

-- 查看表状态
SHOW TABLE STATUS LIKE 'table_name';

-- 查看字段信息
SHOW COLUMNS FROM table_name;

-- 查询前N条记录
SELECT * FROM table_name LIMIT 10;

-- 条件筛选
SELECT * FROM table_name WHERE column_name = 'value';

-- 排序查询
SELECT * FROM table_name ORDER BY column_name DESC LIMIT 10;

-- 分组统计
SELECT status, COUNT(*) as count 
FROM table_name 
GROUP BY status;

-- 时间范围查询
SELECT * FROM table_name 
WHERE created_at >= '2025-11-01' 
  AND created_at < '2025-12-01';
```

## 示例输出

```
SQL> SELECT * FROM users LIMIT 3;

✅ 查询成功! 共返回 3 条记录:

+----+----------+------------------+---------------------+
| id | username | email            | created_at          |
+====+==========+==================+=====================+
| 1  | alice    | alice@email.com  | 2024-01-01 10:00:00 |
+----+----------+------------------+---------------------+
| 2  | bob      | bob@email.com    | 2024-01-02 11:30:00 |
+----+----------+------------------+---------------------+
| 3  | charlie  | charlie@email.com| 2024-01-03 09:15:00 |
+----+----------+------------------+---------------------+
```

## 注意事项

### 🔒 安全性

1. **只读限制**：工具已强制限制为只读，无法执行任何修改操作
2. **配置文件安全**：`config.json` 包含敏感信息，已添加到 `.gitignore`，请勿提交到Git仓库
3. **权限控制**：即使数据库账号有写权限，本工具也会拒绝执行修改操作
4. **生产环境**：虽然工具是只读的，但在生产环境查询时仍需谨慎，避免执行过于复杂或慢查询

### 📊 查询优化建议

1. **使用LIMIT**：查询大表时建议加上 `LIMIT` 限制返回行数
2. **添加索引条件**：WHERE子句尽量使用有索引的字段
3. **避免SELECT ***：生产环境建议明确指定需要的字段
4. **使用EXPLAIN**：对慢查询使用 `EXPLAIN` 查看执行计划

### 🎯 使用场景

本工具适用于：
- ✅ 数据查询和分析
- ✅ 问题排查和调试
- ✅ 数据验证
- ✅ 表结构查看
- ✅ 性能分析（EXPLAIN）

本工具不适用于：
- ❌ 数据修改操作
- ❌ 表结构变更
- ❌ 数据导入导出
- ❌ 批量数据处理

## 故障排除

### 无法连接到数据库

1. 检查网络连接
2. 确认数据库服务器地址和端口正确
3. 验证用户名和密码
4. 检查防火墙设置

### 依赖安装失败

如果安装 `mysql-connector-python` 失败，可以尝试：

```bash
pip install --upgrade pip
pip install mysql-connector-python --no-cache-dir
```

### SQL被拒绝执行

如果你的查询语句被拒绝，请检查：
1. 是否使用了禁止的关键字（UPDATE、DELETE等）
2. 确保语句是纯查询操作
3. 查看错误提示了解具体原因

## 开发信息

- **语言**: Python 3
- **依赖**: mysql-connector-python, tabulate
- **模式**: 只读查询
- **安全级别**: 高（强制只读限制）

## 常见问题

**Q: 为什么不能执行UPDATE/DELETE操作？**  
A: 这是故意设计的安全限制。本工具专门用于只读查询，防止误操作导致数据被修改或删除。

**Q: 如果我确实需要修改数据怎么办？**  
A: 请使用其他数据库管理工具（如MySQL Workbench、DBeaver等），或直接使用mysql命令行客户端。本工具定位就是安全的只读查询。

**Q: USE database_name 算是修改操作吗？**  
A: 不算。USE只是切换当前数据库上下文，不会修改任何数据，因此是允许的。

**Q: 能否查询系统表？**  
A: 可以，只要是SELECT查询操作都是允许的，包括查询information_schema等系统表。

## 技术支持

遇到问题请检查：
1. README中的故障排除章节
2. 错误提示信息
3. MySQL官方文档

---

**最后提醒：本工具是只读的，请放心使用，不会造成任何数据修改或损坏！** ✅
