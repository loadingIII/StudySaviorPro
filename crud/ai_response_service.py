from datetime import datetime

from sqlalchemy import select

from agent.smart_question.ai_response import get_questions
from model.Question import UserGeneratedQuestion
from schemas.quesion_schemas import UserGeneratedQuestionVO
from utils.threadUtils import get_user_id


async def crud_intelligent_question_generation(data, db):
    """智能出题的CRUD函数，负责调用LLM生成题目，并将生成的题目存储到数据库中"""
    # 调用llm生成题目
    questions = get_questions(data)

    # 讲题目数据存入数据库
    ug_questions = UserGeneratedQuestion(
        question_type=data.question_type,
        user_id=get_user_id(),
        original_question=data.question,
        generated_question_text=questions.json(),
        created_at=datetime.now()
    )
    db.add(ug_questions)

    return questions


async def crud_get_user_generated_questions(db):
    """获取当前用户生成的所有题目记录"""
    user_id = get_user_id()
    res = await db.execute(select(UserGeneratedQuestion).where(UserGeneratedQuestion.user_id == user_id))
    questions = res.scalars().all()

    list_ques = []
    for q in questions:
        temp = UserGeneratedQuestionVO(
            id=q.id,
            original_question=q.original_question,
            generated_question_text=q.generated_question_text,
            question_type=q.question_type,
            created_at=q.created_at.isoformat() if q.created_at else None
        )
        list_ques.append(temp)

    return list_ques
