# import，导入所需要的包，库
import curses
from random import randrange, choice # generate and place new tile
from collections import defaultdict

# 获得有效键值列表
letter_codes = [ord(ch) for ch in 'WASDRQwasdrq']

# 定义用户动作
actions = ['Up', 'Left', 'Down', 'Right', 'Restart', 'Exit']
# 将输入与行为进行关联
actions_dict = dict(zip(letter_codes, actions * 2))


# 用户输入处理，这里直到获得用户有效输入才返回对应行为。
def get_user_action(keyboard):    
    char = "N"
    while char not in actions_dict:
        char = keyboard.getch()
    return actions_dict[char]

# 矩阵转置
def transpose(field):
    return [list(row) for row in zip(*field)]
# 矩阵逆转
def invert(field):
    return [row[::-1] for row in field]


# 创建棋盘，初始化棋盘参数，
# 这里指定了棋盘的高和宽以及游戏胜利条件
# 在这里我们制定的是最经典的4x4的模式。
class GameField(object):
    def __init__(self, height=4, width=4, win=2048):
        self.height = height
        self.width = width
        self.win_value = win	# 过关分数
        self.score = 0	        # 当前分数
        self.highscore = 0	# 最高分
        self.reset()    	# 重置棋盘

    # 重置棋盘
    def reset(self):
        
# highscore为程序初始化过程中定义的一个变量。记录你赢得游戏的最高分数记录。
        if self.score > self.highscore:
            self.highscore = self.score
        self.score = 0

        # 生成一个二维数组。
        # 其中，第一维长度是self.width。第二维长度为self.height。
        # 相当于把棋盘上每一个下棋的地方(横纵线交叉产生的方格)赋值为0。
        self.field = [[0 for i in range(self.width)] for j in range(self.height)]
        self.spawn()
        self.spawn()


    #按键后数字合并操作，棋盘走一步。
    #通过对矩阵进行转置与逆转，可以直接从左移得到其余三个方向的移动操作。
    def move(self, direction):
        def move_row_left(row):
            def tighten(row): # squeese non-zero elements together
                new_row = [i for i in row if i != 0]
                new_row += [0 for i in range(len(row) - len(new_row))]
                return new_row

            # 定义合并函数
            def merge(row):
                pair = False
                new_row = []
                for i in range(len(row)):
                    if pair:
                        new_row.append(2 * row[i])
                        self.score += 2 * row[i]
                        pair = False
                    else:
                        if i + 1 < len(row) and row[i] == row[i + 1]:
                            pair = True
                            new_row.append(0)
                        else:
                            new_row.append(row[i])
                assert len(new_row) == len(row)
                return new_row
            return tighten(merge(tighten(row)))

        moves = {}
        moves['Left']  = lambda field:                              \
                [move_row_left(row) for row in field]
        moves['Right'] = lambda field:                              \
                invert(moves['Left'](invert(field)))
        moves['Up']    = lambda field:                              \
                transpose(moves['Left'](transpose(field)))
        moves['Down']  = lambda field:                              \
                transpose(moves['Right'](transpose(field)))

        if direction in moves:
            if self.move_is_possible(direction):
                self.field = moves[direction](self.field)
                self.spawn()
                return True
            else:
                return False

    # 判断输赢
    def is_win(self):
        return any(any(i >= self.win_value for i in row) for row in self.field)

    # 游戏界面的绘制
    def is_gameover(self):
        return not any(self.move_is_possible(move) for move in actions)

    def draw(self, screen):
        help_string1 = '(W)Up (S)Down (A)Left (D)Right'
        help_string2 = '     (R)Restart (Q)Exit'
        gameover_string = '           GAME OVER'
        win_string = '          YOU WIN!'
        def cast(string):
            screen.addstr(string + '\n')

        # 绘制水平分割线
        def draw_hor_separator():
            line = '+' + ('+------' * self.width + '+')[1:]
            separator = defaultdict(lambda: line)
            if not hasattr(draw_hor_separator, "counter"):
                draw_hor_separator.counter = 0
            cast(separator[draw_hor_separator.counter])
            draw_hor_separator.counter += 1

        def draw_row(row):
            cast(''.join('|{: ^5} '.format(num) if num > 0 else '|      ' for num in row) + '|')

        screen.clear()
        cast('SCORE: ' + str(self.score))
        if 0 != self.highscore:
            cast('HIGHSCORE: ' + str(self.highscore))
        for row in self.field:
            draw_hor_separator()
            draw_row(row)
        draw_hor_separator()
        if self.is_win():
            cast(win_string)
        else:
            if self.is_gameover():
                cast(gameover_string)
            else:
                cast(help_string1)
        cast(help_string2)

    # 棋盘数字生成，随机生成一个2或者4
    def spawn(self):
        new_element = 4 if randrange(100) > 89 else 2
        (i,j) = choice([(i,j) for i in range(self.width) for j in range(self.height) if self.field[i][j] == 0])
        self.field[i][j] = new_element

    # 判断能否移动
    def move_is_possible(self, direction):
        def row_is_left_movable(row): 
            def change(i): # true if there'll be change in i-th tile
                if row[i] == 0 and row[i + 1] != 0: # Move
                    return True
                if row[i] != 0 and row[i + 1] == row[i]: # Merge
                    return True
                return False
            return any(change(i) for i in range(len(row) - 1))

        check = {}
        check['Left']  = lambda field:                              \
                any(row_is_left_movable(row) for row in field)

        check['Right'] = lambda field:                              \
                 check['Left'](invert(field))

        check['Up']    = lambda field:                              \
                check['Left'](transpose(field))

        check['Down']  = lambda field:                              \
                check['Right'](transpose(field))

        if direction in check:
            return check[direction](self.field)
        else:
            return False


# 下面是主逻辑代码，游戏会不断循环，直到达到Exit终结状态结束程序
def main(stdscr):
    def init():
        #重置游戏棋盘
        game_field.reset()
        return 'Game'

    def not_game(state):
        #画出 GameOver 或者 Win 的界面
        game_field.draw(stdscr)
        #读取用户输入得到action，判断是重启游戏还是结束游戏
        action = get_user_action(stdscr)
        responses = defaultdict(lambda: state) #默认是当前状态，没有行为就会一直在当前界面循环
        responses['Restart'], responses['Exit'] = 'Init', 'Exit' #对应不同的行为转换到不同的状态
        return responses[action]

    def game():
        #画出当前棋盘状态
        game_field.draw(stdscr)
        #读取用户输入得到action
        action = get_user_action(stdscr)

        if action == 'Restart':
            return 'Init'
        if action == 'Exit':
            return 'Exit'
        if game_field.move(action): # move successful
            if game_field.is_win():
                return 'Win'
            if game_field.is_gameover():
                return 'Gameover'
        return 'Game'

    # state存储当前状态，state_actions这个词典变量作为状态转换的规则，它的key是状态，value是返回下一个状态的函数。
    state_actions = {
            'Init': init,
            'Win': lambda: not_game('Win'),
            'Gameover': lambda: not_game('Gameover'),
            'Game': game
        }

    # 使用默认颜色作为背景
    curses.use_default_colors()

    # 设置终结状态最大数值为 2048q
    game_field = GameField(win=2048)

    state = 'Init'

    #状态机开始循环
    while state != 'Exit':
        state = state_actions[state]()
        
        # 此处的意思是: state=init()或者
        # state=not_game(‘Win')或者
        # 是另外的not_game(‘Gameover')/game()

curses.wrapper(main) # 包装函数，初始化curses并调用函数 main
