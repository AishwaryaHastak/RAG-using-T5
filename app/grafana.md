# Grafana Queries for Dashboard Creation

This document outlines the SQL queries used to create the Grafana dashboards for analyzing data from the application.

## 1. Feedback by Topic
```sql
SELECT sum(feedback) as feedback, topic
FROM conversations c
JOIN feedback f ON f.conversation_id = c.id
GROUP BY topic
ORDER BY feedback;
```

## 2. Question Distribution Across Topics

```sql
SELECT COUNT(*) as count, topic
FROM conversations
GROUP BY topic
ORDER BY count;
```

## 3. Relevance Score by Topic
```sql
SELECT avg(relevance_score) as avg_relevance_score, topic
FROM conversations 
WHERE search_type = 'Text'
GROUP BY topic
ORDER BY avg_relevance_score;
```

## 4. Average Time Taken by Search Type 
```sql
SELECT avg(time_taken) as avg_time_taken, search_type
FROM conversations 
GROUP BY search_type;
```

## 5. Average Time Taken (in ms) for Retrieval Across Topics
```sql
SELECT avg(time_taken) as avg_time_taken, topic 
FROM conversations
WHERE search_type='Text'
GROUP BY topic
ORDER BY avg_time_taken;
```