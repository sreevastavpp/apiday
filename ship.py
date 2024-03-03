from time import sleep


class TreasureHunt:
    def __init__(self):
        # soon will be deleted if i read the code again no worries
        self.x = 60
        self.y = 15
        self.maximum_distance = 5
        self.board = []
        self.chests_location = []
        self.used_moves = []
        self.placeholder = ""
        self.screen = ""
        self.user_x = 0
        self.user_y = 0
        self.sonar_devices = int(self.x / 3)
        self.chest_number = round(self.x / 7)

    def getBoard(
        self, width=60, height=15
    ):  # this is to calculate the 'waves' on the board
        from random import randint

        if width > 100 or height > 100:
            print("Width or height too big.")
            return False
        if width < 10 or height < 10:
            print("Width or height too small.")
            return False
        self.y, self.x = height, width
        for y in range(height):
            self.board.append([])  # append a list inside a list
            for x in range(width):
                if randint(0, 1) == 0:
                    self.board[y].append(
                        "`"
                    )  # append the list inside the list with these randoms to create waves
                else:
                    self.board[y].append("~")
        return self.board

    def drawBoard(self):  # this is for visualizing purposes
        def first():
            # first line
            self.placeholder += (
                " " * 3
            )  # for the furthest left part, reserved for the left numbers
            for i in range(
                1, int(self.x / 10) + 1
            ):  # adds the top part multiplied by 10, 1 2 3 4
                self.placeholder += " " * 9 + str(i)
            if (self.x % 10) == 0:  # for the whitespaces if it's not a 10th number
                self.placeholder += " " * 9
            else:
                self.placeholder += " " * (self.x % 10)
            self.placeholder += (
                " " * 3 + "\n"
            )  # for the furthest right part, reserved for the right numbers

        def second():
            # second line
            self.placeholder += " " * 3  # for the left numbers
            for i in range(
                int(self.x / 10)
            ):  # this is initializing the 1234567890 numbers
                for o in range(1, 10):
                    self.placeholder += str(o)
                self.placeholder += "0"
            if (self.x % 10) > 0:  # if it doesnt end in a 10th number
                for m in range(1, self.x % 10 + 1):
                    self.placeholder += str(m)
            self.placeholder += "\n"

        first(), second()
        #  the waves according to numbers
        for p in range(self.y):
            self.placeholder += (str(p + 1)).ljust(3)
            for characters in range(self.x):
                self.placeholder += self.board[p][
                    characters
                ]  # put the list of waves from self.board
            self.placeholder += (str(p + 1)).rjust(
                3
            ) + "\n"  # put the numbers to the right screen
        second(), first()
        self.screen = self.placeholder  # captures the board
        self.placeholder = ""  # deletes the board to make space for a new one
        return print(self.screen)

    def randomChestPlace(self):
        from random import randint

        self.chest_number = round(self.x / 7)
        self.sonar_devices = int(self.x / 3)
        for i in range(self.chest_number):
            chests = [randint(1, self.x), randint(1, self.y)]
            if chests not in self.chests_location:
                self.chests_location.append(chests)
            elif len(chests) != 3 and chests in self.chests_location:
                chests.append([randint(1, self.x), randint(1, self.y)])
        return self.chests_location

    def valid_move(self, playermove):
        placeholder_list = [playermove]
        for x, y in placeholder_list:
            if (self.x - 1) <= int(x) >= 1:
                return True
            elif (self.y - 1) <= int(y) >= y:
                return True

    def move(self):
        from math import sqrt

        smallest_distance = 100
        for (
            cx,
            cy,
        ) in (
            self.chests_location
        ):  # finding the distance between user inputted and chest's
            # sqrt((chest x - user x)^2 + (chest y - user y)^2)
            calculated_distance = sqrt(
                pow((cx - self.user_x), 2) + pow((cy - self.user_y), 2)
            )
            if calculated_distance < smallest_distance:
                smallest_distance = round(calculated_distance)
        # naming and commenting soon but just know it's pretty much the end result/output
        self.sonar_devices -= 1
        self.user_x -= 1
        self.user_y -= 1
        print("Sonar device left: %s" % self.sonar_devices)
        if smallest_distance == 0:
            print(self.user_x, self.user_y)
            self.chests_location.remove([self.user_x + 1, self.user_y + 1])
            self.board[self.user_y][self.user_x] = "C"
            print(
                "You found a sunken chest! %s more to go!" % len(self.chests_location)
            )
        elif smallest_distance <= self.maximum_distance:
            self.board[self.user_y][self.user_x] = str(smallest_distance)
            print("You found a chest %s distance away!" % smallest_distance)
        elif smallest_distance >= self.maximum_distance:
            self.board[self.user_y][self.user_x] = "X"
            print("You didn't find anything.")

    def user_chest_move_calculation(
        self,
    ):  # basically handles with user error and inputs kkk
        from time import sleep

        self.user_x = 0
        self.user_y = 0
        try:
            user_input = input(
                "Where do you want to put the sonar device, cap?\n> "
            ).split(",")
            exqu = ""
            for a in user_input:
                exqu += a
            if exqu == "exit" or exqu == "quit":  # if user wants to leave
                for t in range(5, 0, -1):
                    clear_screen()
                    print("Goodbye!")
                    print("Program quitting in " + str(t) + "...")
                    sleep(1)
                quit()
            if user_input in self.used_moves:
                raise ZeroDivisionError
            if not len(user_input) == 2 or self.valid_move(
                user_input
            ):  # if len of user_input != 2 or not valid move
                raise TypeError
            self.user_x += int(user_input[0])  # logs the x and y
            self.user_y += int(user_input[1])
            self.used_moves.append(user_input)  # logs every moves
        except TypeError:
            clear_screen()
            print("Please only enter integers with commas, and input 2 arguments.")
            sleep(3)
            clear_screen()
        except ValueError:
            clear_screen()
            print("Please only enter integers.")
            sleep(3)
            clear_screen()
        except ZeroDivisionError:
            clear_screen()
            print("You have put that position before.")
            sleep(3)
            clear_screen()

    def introduction(self):  # introduction with a txt
        file = open("introduction.txt", "rt")
        for lines in file:
            a = lines.rstrip().splitlines()  # splitlines() automatically splits \n
            print(lines.rstrip())
            if not a:  # if list is empty
                input("Press enter to continue. ")
                clear_screen()


def clear_screen():  # clears the screen
    from os import system

    _ = system("cls")


def check_int(user_input):  # checks if is an integer
    try:
        int(user_input)
        return True
    except ValueError:
        return print("I only take numbers.")


# initializing the game
TH = TreasureHunt()
while True:
    TH.introduction()  # introduction starts
    while True:
        game_start_input = input(
            "So what do you think, cap? Ready to get the treasures?\n> "
        ).lower()
        if game_start_input == "help":
            TH.introduction()
        if game_start_input == "start" or game_start_input.startswith("yes"):
            print("OK")
            break
        while game_start_input.startswith("commands"):  # changes some game aspects
            print("This is where we change stuffs up, cap. What do you want to change?")
            print(
                "1. Sonar device amount\n2. Chests amount\n3. Board size\n4. Maximum distance\n5. Back"
            )
            amount_change = input("> ")
            check_int(amount_change)
            if amount_change == "1":
                sonar_change = input(
                    "Change sonar device amount to..? (Default is 1/3 board size)\n> "
                )
                check_int(sonar_change)
                TH.sonar_devices = sonar_change
            if amount_change == "2":
                chest_change = input(
                    "Change chests amounts to..? (Default is 1/7 board size)\n> "
                )
                check_int(chest_change)
                TH.chest_number = chest_change
            if amount_change == "3":
                board_size_change = input(
                    "Change board size to..? (Default is 60x15)(Example: 30,10)\n> "
                ).split(",")
                check_int(board_size_change)
                if len(board_size_change) != 2:
                    board_size_change = input(
                        "Enter 2 arguments, else the game will quit."
                    )
                try:
                    for bx, by in board_size_change:
                        TH.x, TH.y = int(bx), int(by)
                except TypeError:
                    print("No integers detected.")
                    quit()
            if amount_change == "4":
                distance_change = input(
                    "Change maximum distance to..? (Default is 10)\n> "
                )
                check_int(distance_change)
                TH.maximum_distance = distance_change
            if amount_change == "5":
                print("OK!")
                break
    clear_screen()
    TH.getBoard()  # gets the board
    TH.randomChestPlace()  # initializes the chests
    TH.drawBoard()  # adds the board to the screen
    while len(TH.chests_location) > 0 and int(TH.sonar_devices) > 0:
        TH.user_chest_move_calculation()
        TH.move()
        TH.drawBoard()
    end_message = ""
    if len(TH.chests_location) == 0:
        end_message = "Way to go, cap! We found every chests. Another ride?"
    elif int(TH.sonar_devices) == 0:
        end_message = "Tough luck, cap. We ran out of sonars. We'll get 'em next time. Another ride?"
    play_again = input("{}\n> ").format(end_message).lower()
    if play_again.startswith("yes"):
        print("Sweet!\nLoading...")
        sleep(3)
        continue
    elif play_again.startswith("no"):
        print("Well, I'll see you next time, cap.\nQuitting...")
        sleep(3)
        quit()
    else:
        print("I don't understand, cap. Are you drunk? I'm leaving you.\nQuitting...")
        sleep(3)
        quit()