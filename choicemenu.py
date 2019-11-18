"""
Takes a list, tuple or dict object and presents users with \
all items in the object to choose one or more or all items.

User Cases:
Useful in a situations where scripts need to be invoked manually and by \
wide range of users. It becomes a challenge to give them arguments they \
need to pass and or provide them with an easier way to determine available \
arguments and correct value for those arguments. Instead, I found it \
easier to create this class and use it to provide a menu driven script \
that wrappers around the original script and will ask user to choose \
item(s) from a list/tuple/dictionary and then use the selection to call \
a the original script with correct arguments.
One of my many user cases:
Managing hundreds of servers in different environments with different \
services and behind different kind of load balancers was a challange. \
I use this class so that no one has to remember arguments of all \
the scripts we have. This can be used as a multi level argument \
alternative.
    Multi level argument
    - Get a list of load balancers to choose from:
      - Get the list of instances/servers in the lb to choose from:
        - Action to perform on the server:
          - toggle offline/online
          - patch
"""

from termcolor import colored


class ChoiceMenu(object):
    """
    Parameters:
        input_object:
            list: A list object for user to choose from.
            dict: A dictionary object for user to choose from.
        multichoice: True would allow multiple items to be selected.
        maxtries: How many times user is allowed to submit a bad choice.

    Returns:
        dict:
        list:
    """

    def __init__(self, input_object, multichoice=True, maxtries=10):
        """
        Initialize the class with basic information and verify values.
        """
        self._my_list = input_object
        self._user_input = []
        self._multi_choice = multichoice
        self._object_type = type(input_object)
        #### TODO:
        ## fix bug in max_key_len count
        ## numeric elements in a list will break
        if isinstance(self._my_list, dict):
            self._max_key_len = max(map(len, self._my_list))
            self._choice = {}
        elif isinstance(self._my_list, (list, tuple)):
            self._choice = []
            self._max_key_len = len(max(self._my_list, key=len))
            # self._max_key_len = max(k for k, v in self._my_list.items())
        else:
            raise Exception("Object can only be of type List, Tuple or Dictionary.")
        self.object_length = len(self._my_list)
        if maxtries < 0 or not isinstance(maxtries, int):
            raise Exception("1 Try is minimum the number has to be an integer.")
        else:
            self._max_tries = maxtries

    def _get_user_input(self):
        """
            Internal function to get user choice.
        """
        return input(
            colored("Please make your selection: ", color="green", attrs=["bold"],)
        )

    def _print_choice_message(self):
        """
            Print a message telling user the available choices based
            upon class parameters.
        """
        print(
            colored(
                "{} {}. {}".format(
                    "Choose from 0 to",
                    self.object_length,
                    "Multiple choice needs to be comma separated e.g. 1,2",
                ),
                color="green",
            )
            if self._multi_choice
            else colored(
                "Choose from 1 to {}.".format(self.object_length), color="green",
            )
        )

    def _check_user_input(self, user_input):
        """
            Input has to be integer. If input is not integer then
            returns False.
        """
        try:
            self._user_input = [int(i) for i in user_input.split(",")]
        except Exception as integer_exception:
            print(
                colored(
                    "Only integers are allowed: {}".format(integer_exception),
                    color="red",
                    attrs=["bold", "reverse"],
                )
            )
            return False
        return True

    def _check_multi_choice_in_input(self):
        """
            Check if multiple items were choosen. If yes and multichoice
            was not set to true then return False
        """
        if not self._multi_choice and len(self._user_input) > 1:
            print(
                colored(
                    "Multiple values are not allowed unless multichoice is set to true",
                    color="red",
                    attrs=["bold", "reverse"],
                )
            )
            return False
        return True

    def _check_select_all_option(self):
        """
            Returns False if the user entered 0 in the input but
            multichoice was set to False
        """
        if 0 in self._user_input and not self._multi_choice:
            print(colored("INVALID CHOICE: {}.".format(0), color="red",))
            return False
        return True

    def _check_each_value(self):
        """
            Check if the value provided is between the available range.
            If the value is out of range then return False.
        """
        for user_choice in self._user_input:
            if user_choice > self.object_length or user_choice < 0:
                print(colored("INVALID CHOICE: {}.".format(user_choice), color="red",))
                return False
        return True

    def __check_input(self):
        """
            This function is to check the input from the user to make sure the input is correct.
            If the input is incorrect or invalid we loop back for maxtries default(10). This is
            configurable when initalizing the class object
        """

        fail_counter = 0
        while fail_counter <= self._max_tries:
            ## Let's start assuming all choices will be good and not bad.
            if fail_counter >= self._max_tries:
                raise Exception(
                    "No valid selection made in {} tries.".format(self._max_tries)
                )
            if fail_counter > 0 and fail_counter < self._max_tries:
                print(colored("Please make a valid selection: ", color="yellow",))
            self._print_choice_message()
            user_choice = self._get_user_input()
            if (
                not self._check_user_input(user_choice)
                or not self._check_multi_choice_in_input()
                or not self._check_each_value()
                or not self._check_select_all_option()
            ):
                fail_counter = fail_counter + 1
            else:
                break
        return self._user_input

    def _print_items_to_choose_from(self):
        """
        Creates a pretty output for selection.
        """

        space_after_choice = len(str(self.object_length)) + 3
        item_number = 0
        for i in self._my_list:
            if isinstance(self._my_list, dict):
                if item_number == 0:
                    print(
                        " " * (space_after_choice - 1),
                        colored("KEY", color="yellow", attrs=["underline"],),
                        "".ljust(self._max_key_len),
                        colored(
                            "{}".format("VALUE",), color="yellow", attrs=["underline"],
                        ),
                    )
                    if self._multi_choice:
                        print(
                            colored(
                                "{}{}{}".format(
                                    "0",
                                    "".ljust(
                                        space_after_choice
                                        - (len(str((item_number + 1))))
                                    ),
                                    "Select ALL key value pairs",
                                ),
                                color="cyan",
                            )
                        )
                print(
                    colored(
                        "{}{}{}{}{}".format(
                            item_number + 1,
                            "".ljust(
                                space_after_choice - (len(str((item_number + 1))))
                            ),
                            i.ljust(self._max_key_len),
                            "".ljust(4),
                            self._my_list[i],
                        ),
                        color="yellow",
                    )
                )
            if isinstance(self._my_list, (list, tuple)):
                if item_number == 0 and self._multi_choice:
                    print(
                        colored(
                            "{}{}{}".format(
                                "0",
                                "".ljust(
                                    space_after_choice - (len(str((item_number + 1))))
                                ),
                                "Select ALL Values",
                            ),
                            color="cyan",
                            attrs=["bold"],
                        )
                    )
                print(
                    colored(
                        "{}{}{}".format(
                            item_number + 1,
                            "".ljust(
                                space_after_choice - (len(str((item_number + 1))))
                            ),
                            self._my_list[item_number],
                        ),
                        color="yellow",
                    )
                )
            item_number = item_number + 1

    def get_choice(self):
        """
        Main function that get the values and provides the choice to the user.
        If a dictionary object is sent the choice will show key and value pair
        to choose from.
        """
        self._print_items_to_choose_from()
        for user_choice in self.__check_input():
            if user_choice == None:
                continue
            elif user_choice == 0:
                return self._my_list
            if isinstance(self._my_list, dict):
                working_key = list(self._my_list)[user_choice - 1]
                self._choice[working_key] = self._my_list[working_key]
            else:
                self._choice.append(self._my_list[user_choice - 1])
        if self._choice:
            return self._choice
        return None


if __name__ == "__main__":
    # from choicemenu import ChoiceMenu

    list_servers = [
        "server1",
        "server2",
        "server3",
        "server4",
        "server5",
        "server6",
    ]
    list_tasks = [
        "current status in load balancer",
        "take offline in load balancer",
        "bring back online in load balancer",
        "delete from load balancer",
    ]
    files_menu = {
        "file1": {"created": "Monday"},
        "file2": {"created": "Tuesday"},
        "file3": {"created": "Wednesday"},
    }
    ## setting multiple choice to false and maxtries to 1
    action_choice = ChoiceMenu(list_tasks, multichoice=False, maxtries=1).get_choice()
    ## keeping everything else except input_object to default.
    server_choice = ChoiceMenu(list_servers).get_choice()
    ## output here
    print("performing {} on servers : {}".format(action_choice, server_choice))

    ## Dictionary testing.
    print(ChoiceMenu(files_menu, multichoice=False, maxtries=1).get_choice())
