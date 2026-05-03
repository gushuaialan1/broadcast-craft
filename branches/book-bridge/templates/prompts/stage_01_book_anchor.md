# Stage 01 | Book Anchor（书籍锚定）

## 输入

- 书名：{{book_title}}
- 备选主题（若网上检索不到该书）：{{fallback_theme}}

## 任务

1. 提取该书的核心论点（用 1 句话概括）
2. 检索该书是否引用了历史案例（如有，列出案例名称）
3. 确定这本书能解决的最深层心理需求（非表层功能，而是情绪/认知层面的需求）
4. 如使用了 fallback_theme，在输出中注明"基于用户提供的主题展开"

## 输出格式（JSON）

```json
{
  "book_title": "书名",
  "core_thesis": "用一句话概括书的核心论点",
  "historical_cases": ["案例1", "案例2"],
  "deep_need": "这本书能解决的最深层心理需求",
  "fallback_used": false
}
```
