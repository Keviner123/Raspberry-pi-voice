from BLL.question_answering_service import QuestionAnsweringService

questionansweringservice = QuestionAnsweringService()

aaaa = questionansweringservice.get_answer("hi")


print(aaaa)