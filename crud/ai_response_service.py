import asyncio
from datetime import datetime

from langchain_core.output_parsers import StrOutputParser
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from agent.llms.llms import think_llm
from agent.sub_agents.question_agent import api_question_agent
from model.Question import UserGeneratedQuestion
from schemas.agent_schemas import AgentQuestion, ChatHistoryVO, ChatSessionVO
from schemas.quesion_schemas import UserGeneratedQuestionVO
from utils.logger_handler import logger
from utils.threadUtils import get_user_id
from model.ChatHistory import ChatHistory, ChatSession


async def crud_intelligent_question_generation(data, db):
    """智能出题的CRUD函数，负责调用QuestionAgent生成题目，并将生成的题目存储到数据库中"""
    # 调用 QuestionAgent 生成题目
    questions_json = await api_question_agent(
        query=data.question,
        question_type=data.question_type,
        question_count=data.question_count
    )

    # 将题目数据存入数据库
    ug_questions = UserGeneratedQuestion(
        question_type=data.question_type,
        user_id=get_user_id(),
        original_question=data.question,
        generated_question_text=questions_json,
        created_at=datetime.now()
    )
    db.add(ug_questions)

    return questions_json


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


async def crud_add_chat_history(db, data: AgentQuestion, full_response: str = None):
    """添加用户(0)和AI(1)聊天记录到数据库"""
    user_role, ai_role = 0, 1

    content = data.question
    session_id = data.session_id
    # 检查session_id是否存在, 如果不存在则创建
    res = await db.execute(select(ChatSession).where(ChatSession.id == session_id))
    session_exists = res.scalars().first()

    if not session_exists:
        chain = think_llm | StrOutputParser()
        theme = chain.invoke(f"""
        请用极短的语言提炼出下列用户的问题与AI的问答之间的主题,作为会话的主题
        [用户提问]: {content}
        [AI回答]:{full_response}
        """)

        new_session = ChatSession(
            id=session_id,
            user_id=get_user_id(),
            title=theme
        )
        db.add(new_session)
        await db.commit()

    try:
        # 添加用户消息
        user_chat_history = ChatHistory(
            session_id=session_id,
            role=user_role,
            content=content,
            created_at=datetime.now(),
            status=0
        )
        db.add(user_chat_history)
        # 添加AI消息
        ai_chat_history = ChatHistory(
            session_id=session_id,
            role=ai_role,
            content=full_response,
            created_at=datetime.now(),
            status=0
        )
        db.add(ai_chat_history)
        await db.commit()
    except:
        await db.rollback()


async def crud_get_new_session_id(db: AsyncSession):
    """获取当前用户的session_id"""
    try:
        user_id = get_user_id()
        res = await db.execute(select(ChatSession).where(ChatSession.user_id == user_id).order_by(ChatSession.id.desc()))
        session = res.scalars().first()
        # 如果session_id不存在，则创建一个
        if session:
            session_id = session.id + 1
            logger.info(f"获取新session_id成功：{session.id}")
        else:
            session_id = 1
            logger.info("获取新session_id成功：用户无会话，使用默认id=1")

        return session_id
    except:
        logger.error("获取session_id失败")

async def crud_get_sessions(db: AsyncSession):
    """获取当前用户的所有会话"""
    user_id = get_user_id()
    res = await db.execute(select(ChatSession).where(ChatSession.user_id == user_id).order_by(ChatSession.id.desc()))
    sessions = res.scalars().all()
    list_sessions = []
    for s in sessions:
        temp = ChatSessionVO(
            id=s.id,
            title=s.title,
            created_at=s.created_at.isoformat() if s.created_at else None,
        )
        list_sessions.append(temp)
    logger.info(f"获取用户会话成功!")
    return list_sessions

async def crud_get_chat_history(db: AsyncSession, session_id):
    """获取当前用户的聊天记录"""
    chat_history_res = await db.execute(select(ChatHistory)
                                        .where(ChatHistory.session_id == session_id,ChatHistory.status==0)
                                        .order_by(ChatHistory.id.asc()))
    chat_history = chat_history_res.scalars().all()
    list_chat = []
    for c in chat_history:
        temp = ChatHistoryVO(
            id=c.id,
            session_id=c.session_id,
            role=c.role,
            content=c.content,
            created_at=c.created_at.isoformat() if c.created_at else None,
            status=c.status
        )
        list_chat.append(temp)
    logger.info(f"获取用户聊天记录成功!")
    return list_chat


async def crud_delete_chat_history(db: AsyncSession, chat_history_ids):
    """删除当前用户的聊天记录"""
    try:
        await db.execute(update(ChatHistory).where(ChatHistory.id.in_(chat_history_ids)).values(status=1))
        await db.commit()
        logger.info(f"删除用户聊天记录成功!")
        return True
    except:
        await db.rollback()
        logger.error(f"删除用户聊天记录失败!")
        return False

async def crud_delete_chat_session(db: AsyncSession, session_id):
    """删除当前用户的聊天会话"""
    try:
        # 先删除会话下的聊天记录
        await db.execute(delete(ChatHistory).where(ChatHistory.session_id == session_id))
        # 再删除会话本身
        await db.execute(delete(ChatSession).where(ChatSession.id == session_id))
        await db.commit()
        logger.info(f"删除用户聊天会话成功!")
        return True
    except:
        await db.rollback()
        logger.error(f"删除用户聊天会话失败!")
        return False


