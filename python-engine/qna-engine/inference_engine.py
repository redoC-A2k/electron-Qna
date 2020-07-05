from models.albert import Albert
from collections import OrderedDict

class QnAModel:
    def __init__(self, model_name: str):
        """A direct class to be used to draw inference from a model by just passing its name

        Parameters
        ----------
        model_name : str
            The name of the model you want to use for inference
        """

        self.models = {"Albert": Albert}
        self.model_class = self.models.get(model_name, None)

    def get_answer(self, para: str, query: list) -> OrderedDict:
        """A function that is to be used for drawing inference from 
        the selected model

        Parameters
        ----------
        para : str
            The context from which the query is asked
        query : list
            The list of queries of the user

        Returns
        -------
        answer : OrderedDict
            The OrderedDict of answers of the queries returned by the model
        """

        assert self.model_class is not None, "The model name you passed is invalid."
        model = self.model_class()
        answer = model.infer(para, query)

        return answer


if __name__ == '__main__':
    model = QnAModel("Albert")
    context = "New Zealand (Māori: Aotearoa) is a sovereign island country in the southwestern Pacific Ocean. It has a total land area of 268,000 square kilometres (103,500 sq mi), and a population of 4.9 million. New Zealand's capital city is Wellington, and its most populous city is Auckland."
    questions = ["How many people live in New Zealand?", "What's the largest city?"]

    predictions = model.get_answer(context, questions)

    for key in predictions.keys():
        print(predictions[key])