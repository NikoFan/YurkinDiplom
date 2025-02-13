# Стек действий пользователя
class ActionStack:
    stack: list = []

    @staticmethod
    def push(action: str):
        ''' Добавить элемент '''
        ActionStack.stack.append(action)

    @staticmethod
    def pop():
        ''' Удаление последнего добавленного пути '''
        if len(ActionStack.stack) == 1:
            return ActionStack.stack[0]
        ActionStack.stack.pop()
        return ActionStack.stack[-1]

    @staticmethod
    def get_last():
        print(ActionStack.stack)
        return ActionStack.stack[-1]

    @staticmethod
    def change_step(step: str):
        """
        Функция для заменты шага
        :param step: Новый шаг
        :return: Ничего
        """

        if step == "Шаг 0":
            ActionStack.pop()
            return
        print("new step", step)
        print("new step", ActionStack.stack)
        ActionStack.stack[-1] = step
        print("new step", ActionStack.stack)

    @staticmethod
    def clear_stack():
        """
        Очищение стека от информации
        :return: Ничего
        """
        ActionStack.stack = []
    @staticmethod
    def get_full_stack():
        print("Полный стек:", ActionStack.stack)
        return ActionStack.stack  # -> [Регистрация, Изобретение, Информация]

    @staticmethod
    def get_element_by_index(index_of_element: int):
        print(ActionStack.stack)
        return ActionStack.stack[index_of_element]
# [Регистрация, Изделие, Информация]
