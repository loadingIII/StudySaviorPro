"""将分块的段落输入后,会生成几个相关问题,将问题存入数组或者一个字符串中返回"""
from langchain_core.output_parsers import StrOutputParser

from agent.llms.llms import question_llm
from langchain_core.prompts import PromptTemplate

qa_prompt = PromptTemplate.from_template(
    """
   你是一位善于提问的专家,请根据以下文档内容,生成3个用户可能提出的、高度相关的问题。
   只返回问题list列表不要有其他的前缀或者符号。
   【样例回答】:
   ["AI是什么?"||"AI是如何发展的"||"AI应该怎么去发展?"]
   
   【文档内容】：
   ######(在下一个“######”出现前，都为文档内容)
   {content}
   ######
   """
)

qa_chain = qa_prompt | question_llm | StrOutputParser()


def get_questions(texts: str) -> list[str]:
    """获取texts文本内容,返回相关问题"""
    res = qa_chain.invoke({"content": texts})
    lt = res.replace("[", "").replace("]", "").split("||")
    return lt













if __name__ == '__main__':
    texts = """
    一、春季服装（纯棉、薄牛仔、针织棉、轻薄化纤）
    
    1. 纯棉材质（春季衬衫、T恤、休闲裤）
    
    洗涤：可机洗或手洗，水温≤30℃，中性洗涤剂；浅色与深色分开洗，首次洗加少许盐固色；机洗用洗衣袋+轻柔模式，避免摩擦起球。
    
    养护：阴凉通风处阴干，避免暴晒褪色；收纳前完全干燥，折叠或宽肩悬挂；潮湿天放干燥剂防发霉。
    
    2. 薄牛仔材质（春季牛仔裤、牛仔外套）
    
    洗涤：水温≤30℃，中性洗涤剂；翻面清洗减少褪色，机洗选轻柔模式；避免频繁清洗，1-2周一次即可。
    
    养护：翻面阴干，避免阳光直射；收纳时折叠平放或悬挂，宽肩衣架防止裤腰变形；裤兜内放防潮纸保持版型。
    
    3. 针织棉材质（春季针织衫、薄开衫）
    
    洗涤：手洗优先，水温≤25℃，中性洗涤剂轻轻按压；机洗需用洗衣袋，选针织专用模式；禁止用力搓揉、拧绞。
    
    养护：平铺阴干，避免悬挂拉伸领口；收纳时折叠，可放樟脑丸防蛀；轻微起球用毛球修剪器处理。
    
    4. 轻薄化纤材质（春季风衣、防晒衣）
    
    洗涤：可机洗，水温30-40℃，中性或碱性洗涤剂；轻柔揉搓，顽固污渍轻轻刷洗；清洗时加柔顺剂减少静电。
    
    养护：可阳光下晾晒，及时翻面确保干燥；收纳折叠或悬挂均可，避免重压产生永久性褶皱。
    """
    lt = get_questions()
    for i in lt:
        print(i)
