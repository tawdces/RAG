# Retrieval-Augmented Generation (RAG)

## Overview

Retrieval-Augmented Generation (RAG) เป็นแนวทางการพัฒนาระบบ AI ที่ผสมผสานระหว่างการค้นหาข้อมูล (Retrieval) และการสร้างคำตอบด้วย Large Language Model (LLM) เพื่อให้สามารถตอบคำถามโดยอ้างอิงจากข้อมูลขององค์กรหรือเอกสารที่กำหนดได้อย่างถูกต้องและลดปัญหา Hallucination

ระบบแบ่งการทำงานออกเป็น 2 ส่วนหลัก ได้แก่

* Retrieval
* Generate

---

# Part 1 : Retrieval

## File Processing

### 1. Extract Text

ดึงข้อความ (Text) จากไฟล์ เช่น PDF หรือเอกสารต่าง ๆ โดยไม่ประมวลผลรูปภาพ

ข้อมูลจะถูกแยกตามหน้าเอกสารเพื่อจัดเก็บ Metadata สำหรับอ้างอิงแหล่งที่มาในภายหลัง เช่น

* File Name
* Page Number

### 2. Chunking

แบ่งข้อความออกเป็นหลาย Chunks โดยกำหนดให้แต่ละ Chunk มีข้อความทับซ้อนกัน (Overlap)

ตัวอย่าง

```text
Chunk 1 : 0 - 500
Chunk 2 : 400 - 900
Chunk 3 : 800 - 1300
```

การทำ Overlap ช่วยลดปัญหาข้อมูลขาดหายระหว่างการแบ่งข้อความ

### 3. Embedding

นำข้อความของแต่ละ Chunk ไปแปลงเป็น Embedding Vector

ตัวอย่าง

```text
MongoDB is a NoSQL database
```

↓

```text
[0.123, -0.551, 0.882, ...]
```

Embedding Vector ใช้สำหรับเปรียบเทียบความหมายของข้อความในการค้นหาข้อมูล

### 4. Data Storage

จัดเก็บข้อมูลที่เกี่ยวข้องลงในฐานข้อมูล

ตัวอย่างข้อมูลที่จัดเก็บ

```json
{
  "source": "Test.PDF",
  "page": 1,
  "chunk_id": 1,
  "text": "...",
  "embedding": [...]
}
```

ข้อมูลที่จัดเก็บประกอบด้วย

* Source(File Name)
* Page
* Chunk_ID
* Text
* Embedding

---

## Database

ข้อมูลเชิงโครงสร้าง (Structured Data) ที่มีอยู่แล้วในฐานข้อมูลสามารถนำมาใช้ตอบคำถามได้โดยตรงผ่านการ Query

ตัวอย่าง

* Product Data
* Transaction Data

ข้อมูลประเภทนี้ไม่จำเป็นต้องทำ Embedding หากสามารถค้นหาด้วย SQL ได้โดยตรง

---

# Part 2 : Generate

## Question Classification

เมื่อผู้ใช้ส่งคำถามเข้ามา ระบบจะวิเคราะห์ประเภทของคำถาม (Query Routing)

เพื่อเลือกวิธีค้นหาข้อมูลที่เหมาะสมระหว่าง

* Embedding Search
* SQL Query

---

## Embedding Search

### 1. Question Embedding

นำคำถามของผู้ใช้ไปแปลงเป็น Embedding Vector

โดยใช้ Embedding Model เดียวกับที่ใช้สร้าง Embedding ของเอกสาร

### 2. Vector Search

นำ Vector ของคำถามไปเปรียบเทียบกับ Vector ของเอกสารที่จัดเก็บไว้ในฐานข้อมูล

เพื่อค้นหา Chunks ที่มีความหมายใกล้เคียงกันมากที่สุด

### 3. Retrieve Top K

เลือกผลลัพธ์ที่มีความใกล้เคียงมากที่สุด เช่น

```text
Top K = 5
```

จากนั้นดึง

* Text
* Metadata

ของ Chunks ที่เกี่ยวข้อง

### 4. Generate Answer

นำ Text ที่ค้นพบไปใช้เป็น Context สำหรับ LLM

ตัวอย่าง Flow

```text
Question
    ↓
Vector Search
    ↓
Top 5 Chunks
    ↓
Context
    ↓
LLM
    ↓
Answer
```

หมายเหตุ:

LLM ไม่ได้รับ Embedding Vector โดยตรง

LLM จะได้รับเฉพาะ Text ที่ถูกดึงมาจาก Retrieval เพื่อใช้สร้างคำตอบ

---

## SQL Query

สำหรับคำถามที่เกี่ยวข้องกับข้อมูลเชิงโครงสร้าง

ตัวอย่าง

* จำนวนเอกสารทั้งหมด
* รายชื่อเอกสาร

ระบบจะ Query ข้อมูลจากฐานข้อมูลโดยตรง

ตัวอย่าง Flow

```text
Question
    ↓
SQL Query
    ↓
Database
    ↓
Result
    ↓
LLM (Optional)
    ↓
Answer
```

---

# System Flow

```text
User Question
       │
       ▼
Question Classification
       │
 ┌─────┴─────┐
 │           │
 ▼           ▼
SQL      Embedding Search
 │           │
 ▼           ▼
Database  Vector Search
 │           │
 ▼           ▼
Result    Top K Chunks
 └─────┬─────┘
       ▼
      LLM
       ▼
    Answer
```

---

# Future Improvements

## FAQ Cache

บันทึกคำถามและคำตอบที่เกิดขึ้นบ่อยลงในฐานข้อมูล

ตัวอย่าง

```text
Question:
เวลาทำการกี่โมง

Answer:
08:30 - 17:30
```

หากมีคำถามเดิมหรือใกล้เคียงกัน ระบบสามารถตอบกลับได้ทันทีโดยไม่ต้องเรียกใช้งาน LLM

---

## Benefits

* ลดการใช้ Token
* ลดต้นทุนการประมวลผล
* เพิ่มความเร็วในการตอบคำถาม
* ลดจำนวนการเรียกใช้งาน LLM
* รองรับการสร้าง FAQ และระบบแนะนำคำถาม
* เพิ่มความแม่นยำของคำตอบจากข้อมูลภายในองค์กร
* ลดปัญหา Hallucination ของ LLM
