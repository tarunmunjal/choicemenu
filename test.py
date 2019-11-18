from unittest.mock import patch
import unittest

from choicemenu import ChoiceMenu


class ChoiceMenuTestClass(unittest.TestCase):
    list_test = ["Apple", "Orange", "Banana", "Mango"]
    dict_test = {
        "Apple": 1,
        "Orange": 2,
        "Banana": 3,
        "Mango": 4,
        "Second Level": {"Inner Dict": {"Third Level": "l3"}},
    }

    def test_select_all_from_list(self):
        user_input = "0"
        with patch("builtins.input", side_effect=user_input):
            dm = ChoiceMenu(self.__class__.list_test).get_choice()
        self.assertEqual(dm, self.__class__.list_test)

    def test_select_two_from_the_list(self):
        user_input = ["1, 2"]
        expected_output = ["Apple", "Orange"]
        with patch("builtins.input", side_effect=user_input):
            dm = ChoiceMenu(self.__class__.list_test, maxtries=1).get_choice()
        self.assertEqual(dm, expected_output)

    def test_select_one_from_the_list(self):
        user_input = "2"
        expected_output = ["Orange"]
        with patch("builtins.input", side_effect=user_input):
            dm = ChoiceMenu(
                self.__class__.list_test, maxtries=1, multichoice=False
            ).get_choice()
        self.assertEqual(dm, expected_output)

    def test_select_two_from_the_dict(self):
        user_input = ["1, 2"]
        expected_output = {"Apple": 1, "Orange": 2}
        with patch("builtins.input", side_effect=user_input):
            dm = ChoiceMenu(self.__class__.dict_test, maxtries=1).get_choice()
        self.assertEqual(dm, expected_output)

    def test_select_all_from_the_dict(self):
        user_input = ["0,1,2"]
        with patch("builtins.input", side_effect=user_input):
            dm = ChoiceMenu(self.__class__.dict_test, maxtries=1).get_choice()
        self.assertEqual(dm, self.__class__.dict_test)

    def test_select_one_from_the_dict(self):
        user_input = ["5"]
        expected_output = {"Second Level": {"Inner Dict": {"Third Level": "l3"}}}
        with patch("builtins.input", side_effect=user_input):
            dm = ChoiceMenu(
                self.__class__.dict_test, maxtries=1, multichoice=False
            ).get_choice()
        self.assertEqual(dm, expected_output)


if __name__ == "__main__":
    unittest.main()
