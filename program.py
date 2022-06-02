from typing import Sequence
def lower_join(seq: Sequence[str]) -> str:
    """Принимает на вход последовательность и создаёт из неё  
    строку в нижнем регистре."""
    return ''.join(seq).lower()
test_list = ['Влад','Ксюша','Олег']
test_set = {'Влад','Ксюша','Олег'}
print(lower_join(test_list))
print(lower_join(test_set))