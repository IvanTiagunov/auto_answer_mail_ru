

class TextProcessingException(Exception):
    pass

class ParseException(Exception):
    pass


class LimitAnswerException(Exception):
    message = """Ответ не опубликован. За сегодняшний день вы дали максимальное количество ответов, доступное на вашем уровне."""