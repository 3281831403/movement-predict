# 角色移动预测：积分、回滚与滑墙

联机角色位置来回跳、贴墙时速度被吃掉：积分没有算加速度半项，航位推演没按延迟外推，回滚没有插值，滑墙没有去掉法线分量，跳跃高度除零，空输入崩，批量预测只成功一半。

## 目录结构

```
README.md
conftest.py
.gitignore
gameplay/__init__.py
gameplay/movement.py
tests/test_movement.py
```

## 当前状态

`gameplay/movement.py` 中所有函数只保留签名与文档字符串，函数体统一
`raise NotImplementedError`。`tests/test_movement.py` 有 15 个参数化用例，
初始全部失败。

## 需要修复的 10 个问题

1. 积分含加速度半项
2. 按延迟外推
3. 回滚插值
4. 滑墙去法线分量
5. 跳跃高度除零
6. 空输入兜底

## 验收

```bash
python -m pytest -q
```

初始应得到 `15 failed`，且没有 collection error。实现 `gameplay/movement.py`
后 15 条用例应全部通过。
