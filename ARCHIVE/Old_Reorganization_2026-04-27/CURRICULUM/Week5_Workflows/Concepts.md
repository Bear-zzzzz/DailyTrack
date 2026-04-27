# 📘 Text-to-SQL 完整学习指南

> **学习日期**：2026-04-27（第 5 周第 1 天）
> **目标**：掌握 Text-to-SQL 的核心概念、技术难点、工程实践
> **预计用时**：2-3 小时

---

## 🎯 学习目标

By 本次学习结束，你应该能够：
- [ ] 清楚理解 Text-to-SQL 的 3 个关键难点
- [ ] 设计高质量的数据库 Schema 文档
- [ ] 构造有效的 Few-shot 示例
- [ ] 实现 SQL 验证和纠错机制
- [ ] 理解 Query 改写处理歧义
- [ ] 设计成本优化方案

---

## 📚 第 1 部分：核心概念（30-45 分钟）

### 什么是 Text-to-SQL？

**定义**：自然语言问题 → SQL 查询的自动转换

```
用户提问：
  "过去 30 天内，销售额最高的产品是什么？"

目标 SQL：
  SELECT product_name, SUM(amount) as total_sales
  FROM orders o
  JOIN products p ON o.product_id = p.id
  WHERE o.order_date >= DATE_SUB(NOW(), INTERVAL 30 DAY)
  GROUP BY o.product_id
  ORDER BY total_sales DESC
  LIMIT 1;
```

**为什么重要？**
- 🎯 让非技术用户能查询数据
- ⚡ 减少编写 SQL 的工作量
- 🤖 是数据库 Agent 的核心能力
- 💰 企业级应用（数据分析、BI）

---

## 🔥 Text-to-SQL 的 3 个关键难点

### 难点 1️⃣：**Schema 理解障碍**

**问题描述**
```
用户：找出上个月销售额最高的客户

LLM 可能犯的错误：
❌ 不知道哪个表存储销售数据（orders 还是 sales？）
❌ 不知道日期字段的名称（order_date、created_at、sale_date？）
❌ 不知道产品和订单的关系（product_id 在哪个表？）
❌ 误解字段含义（amount 是总价还是单价？）
```

**为什么难？**
- 数据库有 10+ 个表，100+ 个字段
- 字段命名规则不统一（驼峰、下划线、缩写）
- 关系复杂（多个 JOIN、自关联）
- Schema 文档不完整或不准确

**影响**：
- 📊 **准确率下降 30-40%**
- 特别是复杂查询（JOIN 3+ 个表）

---

### 难点 2️⃣：**语义-SQL 转换困难**

**问题描述**
```
用户：帮我找出经常购买的客户

这个"经常"有多种理解：
1. 购买次数多？ → WHERE COUNT(*) > threshold
2. 最近购买频繁？ → WHERE recent_count > threshold
3. 高消费客户？ → WHERE total_spend > threshold
4. 所有三种都算？

LLM 可能产生的 SQL：
❌ 歧义问题：不知道"经常"的精确定义
❌ 逻辑错误：用了错误的聚合函数（AVG vs SUM）
❌ 性能问题：没有使用索引字段
```

**为什么难？**
- 自然语言本身就有歧义
- 需要业务逻辑理解
- 同一个问题有多个有效 SQL
- 需要权衡精度、性能、成本

**影响**：
- 📊 **准确率下降 20-30%**
- 需要 SQL 验证和纠错

---

### 难点 3️⃣：**复杂逻辑编程**

**问题描述**
```
用户：
  对于每个产品类别，计算过去 12 个月的销售趋势，
  找出销售额下降超过 20% 的产品，
  并按下降幅度排序。

这需要：
1. ✅ 时间窗口（12 个月）
2. ✅ 分组聚合（按类别）
3. ✅ 计算同比变化（YoY）
4. ✅ 过滤条件（> 20%）
5. ✅ 排序

对应复杂 SQL：
  WITH monthly_sales AS (
    SELECT
      category_id,
      DATE_TRUNC('month', order_date) as month,
      SUM(amount) as monthly_total
    FROM orders
    GROUP BY category_id, DATE_TRUNC('month', order_date)
  ),
  with_trend AS (
    SELECT
      category_id,
      month,
      monthly_total,
      LAG(monthly_total) OVER (PARTITION BY category_id ORDER BY month) as prev_total,
      ((monthly_total - LAG(monthly_total) OVER (...)) / LAG(...)) * 100 as decline_pct
    FROM monthly_sales
  )
  SELECT category_id, decline_pct
  FROM with_trend
  WHERE decline_pct < -20
  ORDER BY decline_pct;
```

**为什么难？**
- 需要多个 CTE (WITH 子句)
- 需要窗口函数 (WINDOW FUNCTIONS)
- 需要子查询和嵌套
- 容易出现逻辑错误

**影响**：
- 📊 **准确率下降 40-60%**（复杂查询）
- 特别是需要窗口函数、CTE 的问题

---

## 🏗️ Schema 设计的 5 个最佳实践

### 实践 1️⃣：**清晰的 Schema 文档**

**优秀示例**
```sql
-- ============================================
-- 表名：orders
-- 说明：订单表，记录所有客户订单信息
-- 重要：order_date 是关键过滤字段，需要索引
-- ============================================

字段说明：
- order_id (INT, PRIMARY KEY)：订单唯一标识
- customer_id (INT, FOREIGN KEY → customers.id)：所属客户
- product_id (INT, FOREIGN KEY → products.id)：订单产品
- quantity (INT)：购买数量
- unit_price (DECIMAL)：单位价格
- total_amount (DECIMAL)：总金额 = quantity × unit_price
- order_date (DATETIME)：订单日期 [关键日期字段]
- status (VARCHAR)：订单状态 (pending, shipped, delivered, cancelled)
- created_at (DATETIME)：创建时间
- updated_at (DATETIME)：更新时间

常用查询：
1. 按日期范围查询：WHERE order_date BETWEEN ? AND ?
2. 按客户查询：WHERE customer_id = ?
3. 按状态统计：GROUP BY status

注意事项：
⚠️ total_amount 可能与 quantity × unit_price 不完全相等（折扣）
⚠️ status = 'cancelled' 的订单要单独处理（不计入销售额）
```

**关键点**
- ✅ 表级说明：是什么、有什么用
- ✅ 字段级说明：类型、含义、取值范围
- ✅ 关系说明：哪些表关联、如何 JOIN
- ✅ 业务规则：什么字段代表什么意思、有什么陷阱
- ✅ 常用查询示例：帮助 LLM 快速理解

---

### 实践 2️⃣：**统一的字段命名规范**

**错误示例**（混乱的命名）
```sql
表 1：orders
  - order_id, cust_id, prd_id, amt, order_dt, create_time

表 2：products
  - product_id, prod_name, price, created_timestamp

表 3：customers
  - c_id, name, email, sign_up_date

问题：
❌ cust_id vs c_id vs customer_id（同一概念不同名字）
❌ order_dt vs create_time vs created_timestamp（日期字段命名不一致）
❌ amt vs price（金额的不同表示）
```

**最佳实践**（统一规范）
```sql
字段命名规范（全库统一）：

1️⃣ ID 字段：总是用 {entity}_id
   ✅ customer_id, product_id, order_id, category_id
   ❌ cust_id, c_id, prod_id

2️⃣ 日期/时间字段：统一后缀
   ✅ order_date, created_at, updated_at
   ❌ order_dt, create_time, modified_time

3️⃣ 布尔值字段：is_ 前缀
   ✅ is_active, is_premium, is_deleted
   ❌ active, premium, deleted

4️⃣ 金额字段：amount 或 price
   ✅ total_amount, unit_price, discount_amount
   ❌ amt, price, value

5️⃣ 计数字段：count 或 _num 后缀
   ✅ order_count, item_count, purchase_num
   ❌ orders, items, num
```

**效果**
- LLM 更容易理解字段含义
- 减少误译的概率
- 准确率提升 10-15%

---

### 实践 3️⃣：**明确的关系说明**

**需要说明的关系**
```
1. 一对多关系（1:N）
   customers → orders（一个客户有多个订单）
   products → order_items（一个产品在多个订单中出现）

2. 多对多关系（N:N）
   products ↔ categories（通过 product_category 表）
   users ↔ roles（通过 user_roles 表）

3. 自关联
   employees → employees（manager_id 指向同表的 employee_id）
   categories → categories（parent_id 表示分类层级）
```

**文档示例**
```sql
-- 关系图
customers (1) ──→ (N) orders (1) ──→ (N) order_items (N) ──→ (1) products
                                                                      ↓
                                                                   (N) product_categories (N)
                                                                      ↓
                                                                   categories

-- 常用 JOIN 示例
-- 查询客户订单详情
SELECT c.name, o.order_id, p.product_name, oi.quantity
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.id;

-- 查询产品分类
SELECT p.product_name, c.category_name
FROM products p
JOIN product_categories pc ON p.id = pc.product_id
JOIN categories c ON pc.category_id = c.id;
```

---

### 实践 4️⃣：**业务规则和陷阱**

**需要说明的业务规则**
```sql
-- 订单表特殊处理
1. cancelled 订单要单独处理
   ✅ WHERE status != 'cancelled'
   ❌ 不过滤导致销售额计算错误

2. order_items 中的 unit_price 可能与 products.price 不同
   - 可能打折、促销、或历史价格变化
   - 查询总价时要用 order_items.unit_price，不是 products.price

3. 时间字段的含义
   - order_date：订单生成日期（用于销售统计）
   - shipped_date：发货日期（用于物流统计）
   - delivered_date：送达日期（用于服务统计）
   → 不同问题要用不同的时间字段！

-- 客户表特殊处理
1. 删除的客户（is_deleted = 1）通常不在当前分析范围
2. 测试账户（is_test = 1）需要过滤
3. VIP 客户可能有特殊逻辑

-- 产品表特殊处理
1. 停售产品（is_active = 0）的销售数据还存在
2. 产品分类可能有多层（需要递归查询）
```

**文档写法**
```sql
⚠️ 重要提示（写在 Schema 顶部）
- 订单统计时必须过滤：status != 'cancelled'
- 所有销售额计算使用 order_items.unit_price 而非 products.price
- 时间相关查询：
  * 销售统计 → 使用 order_date
  * 物流统计 → 使用 shipped_date
  * 收入确认 → 使用 delivered_date
```

---

### 实践 5️⃣：**示例查询集合**

**为常见问题预制 SQL 模板**
```sql
-- 模板 1：日期范围查询
SELECT * FROM orders
WHERE order_date BETWEEN '2026-01-01' AND '2026-12-31'
  AND status != 'cancelled';

-- 模板 2：按分类统计
SELECT c.category_name, SUM(oi.quantity * oi.unit_price) as total_sales
FROM order_items oi
JOIN products p ON oi.product_id = p.id
JOIN product_categories pc ON p.id = pc.product_id
JOIN categories c ON pc.category_id = c.id
GROUP BY c.category_id, c.category_name
ORDER BY total_sales DESC;

-- 模板 3：客户分析
SELECT c.customer_id, c.name, COUNT(o.order_id) as order_count,
       SUM(oi.quantity * oi.unit_price) as total_spent
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
LEFT JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.status != 'cancelled'
GROUP BY c.customer_id, c.name
ORDER BY total_spent DESC;

-- 模板 4：时间序列（按月统计）
SELECT DATE_TRUNC('month', o.order_date) as month,
       SUM(oi.quantity * oi.unit_price) as monthly_sales
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.status != 'cancelled'
GROUP BY DATE_TRUNC('month', o.order_date)
ORDER BY month DESC;
```

**效果**：Few-shot 学习的基础

---

## 🎓 Few-shot 示例的构造方法

### 什么是 Few-shot？

```
不同的教学方式：

1. Zero-shot（不教学）
   系统提示：你是 SQL 专家，把英文转成 SQL
   用户：找出过去 30 天销售额最高的产品
   LLM 可能出错率高：30-40%

2. Few-shot（给示例）
   系统提示 + 3-5 个高质量示例
   然后同样的问题
   LLM 出错率低：10-15%

   原理：in-context learning，LLM 通过示例学会对应的模式
```

### Few-shot 的 4 个关键要素

#### 要素 1️⃣：**多样性**

```
示例要覆盖不同的难度和类型：

示例 1：简单查询（单表）
  Q: 列出所有活跃的产品
  A: SELECT * FROM products WHERE is_active = 1;

示例 2：中等复杂（2-3 个表 JOIN）
  Q: 找出每个客户的订单总数和总支出
  A: SELECT c.customer_id, c.name, COUNT(o.order_id), SUM(oi.quantity * oi.unit_price)
     FROM customers c
     LEFT JOIN orders o ON c.customer_id = o.customer_id
     LEFT JOIN order_items oi ON o.order_id = oi.order_id
     GROUP BY c.customer_id;

示例 3：复杂查询（聚合、过滤、排序）
  Q: 过去 30 天销售额最高的产品是什么？
  A: SELECT p.product_name, SUM(oi.quantity * oi.unit_price) as total_sales
     FROM order_items oi
     JOIN products p ON oi.product_id = p.id
     JOIN orders o ON oi.order_id = o.order_id
     WHERE o.order_date >= DATE_SUB(NOW(), INTERVAL 30 DAY)
       AND o.status != 'cancelled'
     GROUP BY p.product_id, p.product_name
     ORDER BY total_sales DESC
     LIMIT 1;

示例 4：非常复杂（窗口函数、CTE、时间序列）
  Q: 计算过去 12 个月每个产品的销售趋势，找出销售下降的产品
  A: WITH monthly_sales AS (
       SELECT p.product_id, p.product_name,
              DATE_TRUNC('month', o.order_date) as month,
              SUM(oi.quantity * oi.unit_price) as monthly_total
       FROM products p
       JOIN order_items oi ON p.id = oi.product_id
       JOIN orders o ON oi.order_id = o.order_id
       WHERE o.status != 'cancelled'
       GROUP BY p.product_id, p.product_name, DATE_TRUNC('month', o.order_date)
     ),
     with_trend AS (
       SELECT *,
              LAG(monthly_total) OVER (PARTITION BY product_id ORDER BY month) as prev_month
       FROM monthly_sales
     )
     SELECT product_name, month, monthly_total, prev_month,
            ROUND((monthly_total - prev_month) / prev_month * 100, 2) as growth_pct
     FROM with_trend
     WHERE prev_month IS NOT NULL
     ORDER BY growth_pct ASC;
```

**效果**：示例覆盖 simple → medium → hard，LLM 能学会处理不同复杂度

---

#### 要素 2️⃣：**清晰的注释**

```
好的示例（含详细注释）：

Q: 过去 30 天销售额最高的产品是什么？

A:
SELECT p.product_name, SUM(oi.quantity * oi.unit_price) as total_sales
FROM order_items oi
JOIN products p ON oi.product_id = p.id
JOIN orders o ON oi.order_id = o.order_id
WHERE o.order_date >= DATE_SUB(NOW(), INTERVAL 30 DAY)  -- 时间过滤：过去 30 天
  AND o.status != 'cancelled'                            -- 业务规则：排除取消订单
GROUP BY p.product_id, p.product_name                    -- 按产品分组
ORDER BY total_sales DESC                                 -- 按销售额降序
LIMIT 1;                                                  -- 只取第一名

关键点说明：
1. 使用 order_items.unit_price（订单时的价格），不是 products.price
2. 必须排除 cancelled 订单
3. 时间过滤用 order_date（订单日期），不是 created_at
```

---

#### 要素 3️⃣：**涵盖业务规则**

```
示例要体现业务规则：

✅ 好的示例（涵盖业务规则）
Q: 计算本月的总销售额
A: SELECT SUM(oi.quantity * oi.unit_price) as total_sales
   FROM order_items oi
   JOIN orders o ON oi.order_id = o.order_id
   WHERE MONTH(o.order_date) = MONTH(NOW())
     AND YEAR(o.order_date) = YEAR(NOW())
     AND o.status != 'cancelled'  -- ⭐ 关键业务规则

❌ 不好的示例（遗漏业务规则）
A: SELECT SUM(oi.quantity * oi.unit_price) as total_sales
   FROM order_items oi
   WHERE MONTH(oi.created_at) = MONTH(NOW())
   -- ❌ 没有排除 cancelled
   -- ❌ 用错了时间字段
```

---

#### 要素 4️⃣：**逐步递进的难度**

```
Few-shot 的最佳结构：

在 Prompt 中的位置：
1. 系统消息：Schema 说明 + 业务规则
2. Few-shot 示例：3-5 个递进的例子
3. 用户问题：实际待解决的问题

示例顺序：
1️⃣ 最简单的（单表查询）- 建立信心
2️⃣ 中等的（2 表 JOIN + 简单过滤）- 引入复杂性
3️⃣ 较复杂的（3+ 表 JOIN + 聚合）- 展示常见模式
4️⃣ 最复杂的（CTE/窗口函数）- 处理边界情况

心理学效应：
- 前面简单的例子让 LLM "预热"
- 中间的例子建立信心
- 最复杂的例子说明系统能处理困难情况
- 然后用户的问题显得不那么难

结果：准确率提升 15-25%
```

---

## 🔧 第 2 部分：技术细节（45-60 分钟）

### SQL 验证和纠错策略

#### 策略 1️⃣：**语法验证**

```python
# 层级 1：基本语法检查（正则表达式级别）

def validate_sql_syntax(sql: str) -> Tuple[bool, str]:
    """
    第一层防守：过滤明显的语法错误
    """
    issues = []

    # 1. 检查必要关键字
    if 'SELECT' not in sql.upper():
        issues.append("❌ 缺少 SELECT 关键字")

    # 2. 检查 JOIN 一致性
    joins = sql.count('JOIN')
    ons = sql.count('ON')
    if joins != ons:
        issues.append(f"❌ JOIN 数量 ({joins}) 与 ON 条件数 ({ons}) 不匹配")

    # 3. 检查括号平衡
    if sql.count('(') != sql.count(')'):
        issues.append("❌ 括号不平衡")

    # 4. 检查引号平衡
    if sql.count("'") % 2 != 0:
        issues.append("❌ 引号不平衡")

    if issues:
        return False, "\n".join(issues)
    return True, "✅ 语法检查通过"

# 使用示例
is_valid, message = validate_sql_syntax(sql)
if not is_valid:
    print(message)
    # 要求 LLM 修复
```

#### 策略 2️⃣：**Schema 验证**

```python
# 层级 2：字段和表是否存在

from typing import Dict, List

class SchemaValidator:
    def __init__(self, schema: Dict[str, List[str]]):
        """
        schema 格式：
        {
            'orders': ['order_id', 'customer_id', 'order_date', 'status'],
            'products': ['id', 'product_name', 'price'],
            'customers': ['customer_id', 'name', 'email']
        }
        """
        self.schema = schema
        self.tables = set(schema.keys())
        self.all_fields = {}
        for table, fields in schema.items():
            for field in fields:
                self.all_fields[f"{table}.{field}"] = True

    def validate(self, sql: str) -> Tuple[bool, List[str]]:
        """验证 SQL 中引用的表和字段是否存在"""
        issues = []

        # 1. 检查表是否存在
        import re
        from_clause = re.search(r'FROM\s+(\w+)', sql, re.IGNORECASE)
        if from_clause:
            table_name = from_clause.group(1)
            if table_name not in self.tables:
                issues.append(f"❌ 表不存在：{table_name}")

        # 2. 检查 JOIN 的表
        joins = re.findall(r'JOIN\s+(\w+)', sql, re.IGNORECASE)
        for table_name in joins:
            if table_name not in self.tables:
                issues.append(f"❌ JOIN 表不存在：{table_name}")

        # 3. 检查字段是否存在
        fields = re.findall(r'(\w+\.\w+)', sql)
        for field in fields:
            if field not in self.all_fields:
                issues.append(f"❌ 字段不存在：{field}")

        return len(issues) == 0, issues

# 使用
validator = SchemaValidator(database_schema)
is_valid, issues = validator.validate(sql)
if not is_valid:
    print("\n".join(issues))
```

#### 策略 3️⃣：**逻辑验证（试运行）**

```python
# 层级 3：实际执行验证，最有效但也最贵

import sqlite3
from contextlib import contextmanager

@contextmanager
def get_db_connection(db_path: str):
    """数据库连接管理"""
    conn = sqlite3.connect(db_path)
    try:
        yield conn
    finally:
        conn.close()

def validate_sql_execution(sql: str, db_path: str, timeout: int = 5) -> Tuple[bool, str]:
    """
    实际执行 SQL 验证是否可行
    成本最高，但最准确
    """
    try:
        with get_db_connection(db_path) as conn:
            cursor = conn.cursor()
            # 添加超时保护（防止无限循环）
            cursor.execute(f"SET STATEMENT_TIMEOUT = {timeout * 1000}")

            # 执行 SQL
            cursor.execute(sql)

            # 获取结果（限制行数，防止数据过多）
            results = cursor.fetchmany(1000)

            # 获取列名
            column_names = [description[0] for description in cursor.description]

            return True, {
                "rows": len(results),
                "columns": column_names,
                "sample": results[:5] if results else []
            }

    except sqlite3.OperationalError as e:
        return False, f"❌ SQL 执行错误：{str(e)}"
    except Exception as e:
        return False, f"❌ 未知错误：{str(e)}"

# 使用
is_valid, result = validate_sql_execution(sql, 'database.db')
if is_valid:
    print(f"✅ 查询成功，返回 {result['rows']} 行")
    print(f"   列：{result['columns']}")
else:
    print(result)
```

#### 策略 4️⃣：**业务规则验证**

```python
# 层级 4：业务规则检查

class BusinessRuleValidator:
    def __init__(self):
        self.rules = {
            # 规则 1：涉及 orders 表必须过滤 cancelled
            'orders_must_filter_cancelled': {
                'tables': ['orders'],
                'pattern': r"status\s*!=\s*['\"]cancelled['\"]",
                'message': "❌ 查询 orders 必须过滤 cancelled 订单"
            },
            # 规则 2：金额计算必须用 unit_price
            'use_correct_price': {
                'tables': ['order_items'],
                'pattern': r"quantity\s*\*\s*unit_price",
                'message': "✅ 正确使用了 quantity × unit_price"
            },
        }

    def validate(self, sql: str) -> List[str]:
        """检查是否违反业务规则"""
        issues = []
        sql_upper = sql.upper()

        # 如果查询涉及 orders 表，检查是否过滤了 cancelled
        if 'FROM ORDERS' in sql_upper or 'JOIN ORDERS' in sql_upper:
            if 'CANCELLED' not in sql_upper:
                issues.append("⚠️ 警告：查询 orders 通常需要过滤 cancelled 订单")

        # 如果查询涉及金额统计，检查是否用了正确的字段
        if 'SUM' in sql_upper and 'AMOUNT' in sql_upper:
            if 'UNIT_PRICE' not in sql_upper:
                issues.append("⚠️ 警告：金额计算可能用错了字段，应该用 unit_price")

        return issues

# 使用
br_validator = BusinessRuleValidator()
warnings = br_validator.validate(sql)
for warning in warnings:
    print(warning)
```

---

### Query 改写（处理歧义）

#### 问题：用户问题的歧义

```
用户：找出经常购买的客户

这个"经常"有多种理解：

1️⃣ 解释 1：购买次数多
   SELECT c.*, COUNT(o.order_id) as purchase_count
   FROM customers c
   JOIN orders o ON c.customer_id = o.customer_id
   GROUP BY c.customer_id
   HAVING COUNT(o.order_id) > 10
   ORDER BY purchase_count DESC;

2️⃣ 解释 2：最近购买频繁
   SELECT c.*, COUNT(o.order_id) as recent_purchases
   FROM customers c
   JOIN orders o ON c.customer_id = o.customer_id
   WHERE o.order_date >= DATE_SUB(NOW(), INTERVAL 30 DAY)
   GROUP BY c.customer_id
   HAVING COUNT(o.order_id) >= 5
   ORDER BY recent_purchases DESC;

3️⃣ 解释 3：高消费客户
   SELECT c.*, SUM(oi.quantity * oi.unit_price) as total_spent
   FROM customers c
   JOIN orders o ON c.customer_id = o.customer_id
   JOIN order_items oi ON o.order_id = oi.order_id
   GROUP BY c.customer_id
   ORDER BY total_spent DESC
   LIMIT 100;
```

#### 解决方案：Query 改写

```python
class QueryRewriter:
    """
    将模糊的自然语言问题改写成明确的问题
    然后转换成 SQL
    """

    def __init__(self, llm_client):
        self.llm = llm_client

    def clarify_query(self, user_question: str) -> str:
        """
        步骤 1：让 LLM 识别歧义并改写成明确的问题
        """
        clarification_prompt = f"""
        用户问题：{user_question}

        请识别这个问题中的歧义，并改写成 3 个明确的版本：

        版本 1（关于XXX的解释）：...
        版本 2（关于YYY的解释）：...
        版本 3（关于ZZZ的解释）：...

        然后选择最可能的版本。
        """

        response = self.llm.generate(clarification_prompt)
        return response

    def execute_with_clarification(self, user_question: str) -> Dict:
        """完整流程"""
        # 1. 识别并改写
        clarified = self.clarify_query(user_question)
        print("🔍 改写后的问题：")
        print(clarified)

        # 2. 转换成 SQL
        sql_prompt = f"""
        数据库 Schema：... （省略）

        问题：{clarified}

        请生成对应的 SQL。
        """

        sql = self.llm.generate(sql_prompt)

        return {
            "original_question": user_question,
            "clarified_question": clarified,
            "generated_sql": sql
        }

# 使用
rewriter = QueryRewriter(llm_client)
result = rewriter.execute_with_clarification("找出经常购买的客户")
```

---

### 成本优化

#### 优化 1️⃣：**Prompt 缓存**

```
问题：每次查询都要重新发送完整的 Schema 文档

解决方案：Prompt 缓存（Claude API 特性）

成本对比：
- 不用缓存：每次 query 都消耗 schema tokens（假设 5000 tokens）
  100 次查询 → 100 × 5000 = 500,000 tokens

- 使用缓存：schema tokens 只计算一次，之后可以复用
  第 1 次：5000 tokens（完整）
  第 2-100 次：100 tokens（只计算 query tokens）
  总计：5000 + 100 × 100 = 15,000 tokens

成本降低：97%！
```

```python
import anthropic

client = anthropic.Anthropic()

# 准备 schema 文档
schema_doc = """
# 数据库 Schema

## 表 1：orders
...（完整的 schema）

## 表 2：products
...

## 业务规则
...
""".strip()  # 注意：要去掉多余的换行

def query_with_cache(question: str) -> str:
    """
    使用 Prompt 缓存的查询
    """
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=2048,
        system=[
            {
                "type": "text",
                "text": "你是一个 SQL 生成助手。根据用户问题和 Schema 生成 SQL。"
            },
            {
                # ⭐ 关键：这部分会被缓存
                "type": "text",
                "text": schema_doc,
                "cache_control": {"type": "ephemeral"}
            }
        ],
        messages=[
            {
                "role": "user",
                "content": question
            }
        ]
    )

    return response.content[0].text

# 使用
question_1 = "找出过去 30 天销售额最高的产品"
answer_1 = query_with_cache(question_1)

# 第 2 次查询，schema_doc 被缓存，成本大幅降低！
question_2 = "计算每个产品类别的平均销售额"
answer_2 = query_with_cache(question_2)
```

#### 优化 2️⃣：**SQL 模板库**

```python
class SQLTemplateLibrary:
    """
    常见查询的预制模板，避免重复生成
    """

    def __init__(self):
        self.templates = {
            # 模板 1：按日期范围统计
            'date_range_stats': """
            SELECT DATE_TRUNC('day', {date_field}) as date,
                   SUM({amount_field}) as total
            FROM {table}
            WHERE {date_field} BETWEEN '{start_date}' AND '{end_date}'
              AND {filter_condition}
            GROUP BY DATE_TRUNC('day', {date_field})
            ORDER BY date DESC;
            """,

            # 模板 2：Top N 统计
            'top_n': """
            SELECT {dimension}, SUM({metric}) as total
            FROM {table}
            WHERE {filter_condition}
            GROUP BY {dimension}
            ORDER BY total DESC
            LIMIT {n};
            """,

            # 模板 3：对比分析
            'comparison': """
            SELECT {dimension},
                   SUM(CASE WHEN {condition_1} THEN {metric} ELSE 0 END) as {label_1},
                   SUM(CASE WHEN {condition_2} THEN {metric} ELSE 0 END) as {label_2}
            FROM {table}
            GROUP BY {dimension};
            """
        }

    def get_template(self, template_name: str, **params) -> str:
        """获取模板并填充参数"""
        template = self.templates[template_name]
        return template.format(**params)

# 使用
library = SQLTemplateLibrary()

# 不需要调用 LLM，直接用模板！
sql = library.get_template(
    'date_range_stats',
    date_field='order_date',
    amount_field='amount',
    table='orders',
    filter_condition="status != 'cancelled'",
    start_date='2026-01-01',
    end_date='2026-03-31'
)
print(sql)

# 成本节省：Token 消耗减少 70-80%（不需要调用 LLM）
```

#### 优化 3️⃣：**分层策略**

```python
class CostOptimizedTextToSQL:
    """
    根据问题复杂度采用不同策略
    """

    def __init__(self, llm_client):
        self.llm = llm_client
        self.template_library = SQLTemplateLibrary()
        self.complexity_classifier = ComplexityClassifier()

    def generate_sql(self, question: str) -> str:
        """
        智能选择最省成本的方案
        """
        # 第 1 层：复杂度分类（很便宜，用正则表达式）
        complexity = self.complexity_classifier.classify(question)

        if complexity == 'simple':
            # 简单查询：直接用模板 ✅ 成本最低
            return self._generate_from_template(question)

        elif complexity == 'medium':
            # 中等复杂：用缓存的 LLM ✅ 成本中等
            return self._generate_with_llm(question)

        else:  # complexity == 'complex'
            # 复杂查询：用完整的 LLM + 验证 ✅ 成本最高，但必要
            sql = self._generate_with_llm(question)
            sql = self._validate_and_refine(sql)
            return sql

    def _generate_from_template(self, question: str) -> str:
        """使用模板，零 API 调用成本"""
        if '过去' in question and '销售' in question:
            return self.template_library.get_template(
                'date_range_stats',
                # 参数...
            )

    def _generate_with_llm(self, question: str) -> str:
        """调用 LLM（有缓存支持）"""
        return self.llm.generate(question)

    def _validate_and_refine(self, sql: str) -> str:
        """验证并改进（可选，用于最复杂的查询）"""
        # 验证 SQL
        # 如果有问题，让 LLM 改进
        return sql

# 成本优化结果：
# 简单问题：Token 消耗 ↓ 95%（用模板）
# 中等问题：Token 消耗 ↓ 80%（用缓存）
# 复杂问题：Token 消耗 ↓ 30%（用缓存 + 验证）
```

---

## 📝 总结：Text-to-SQL 的关键洞察

### 核心难点 + 解决方案 对应表

| 难点 | 原因 | 解决方案 |
|------|------|---------|
| Schema 理解 | 表字段众多，命名不统一 | 清晰的 Schema 文档 + 统一命名规范 |
| 语义转换 | 自然语言有歧义 | Query 改写 + Few-shot 示例 |
| 复杂逻辑 | 需要 CTE、窗口函数 | 逐步递进的 Few-shot 示例 |
| 错误恢复 | SQL 可能有语法/逻辑错误 | 多层次验证 + 自动纠错 |
| 成本控制 | LLM 调用贵 | 模板库 + 缓存 + 分层策略 |

### 最佳实践清单

- ✅ Schema 文档必须清晰（表说明 + 字段说明 + 关系说明 + 业务规则）
- ✅ 字段命名要统一（customer_id, not cust_id 或 c_id）
- ✅ Few-shot 示例需要多样性和递进难度
- ✅ 必须包含业务规则（比如 cancelled 订单要过滤）
- ✅ 多层次验证（语法 → Schema → 执行 → 业务规则）
- ✅ 使用 Prompt 缓存减少成本
- ✅ 建立 SQL 模板库处理常见查询

---

## ❓ 常见问题

**Q1：为什么我的 Text-to-SQL 准确率只有 60%？**
A：最常见的原因是 Schema 文档不够清晰，或者 Few-shot 示例不够好。检查：
   1. Schema 是否清楚说明了表关系和字段含义？
   2. Few-shot 示例是否覆盖了用户问题的复杂度？
   3. 是否有业务规则被遗漏（比如 cancelled 订单）？

**Q2：应该用多少个 Few-shot 示例？**
A：通常 3-5 个就够了。更多的示例不一定更好，反而会增加 Token 消耗。质量比数量更重要。

**Q3：执行 SQL 验证会很慢吗？**
A：不会。大多数验证（语法、Schema）都是 O(1) 或 O(n)。只有执行验证在实际数据库上才可能慢，但可以设置超时。

**Q4：如何处理跨数据库的 SQL 差异（MySQL vs PostgreSQL）？**
A：在 Prompt 中明确指定目标数据库，比如："生成 PostgreSQL 语法的 SQL"。在 Few-shot 示例中也要用正确的方言。

---

**下一步**：你准备好进入第 2 部分（技术细节）了吗？
