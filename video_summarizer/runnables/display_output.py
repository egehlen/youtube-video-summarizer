from langchain.schema.runnable import Runnable

class DisplayOutputRunnable(Runnable):

    def invoke(self, input, *args) -> None:
        print(input)