import wx
import wx.grid as gridlib
import random

SNAKES = {16: 6, 47: 26, 49: 11, 56: 53, 62: 19, 64: 60, 87: 24, 93: 73, 95: 75, 98: 78}
LADDERS = {1: 38, 4: 14, 9: 31, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 100}

def fill_snake_ladder_numbers(grid):
    n = 10
    for row_from_bottom in range(n):
        board_row = n - 1 - row_from_bottom
        start_num = row_from_bottom * n + 1
        end_num = start_num + n - 1
        if row_from_bottom % 2 == 0:
            nums = list(range(start_num, end_num + 1))
        else:
            nums = list(range(start_num, end_num + 1))[::-1]
        for col in range(n):
            grid.SetCellValue(board_row, col, str(nums[col]))

class GridFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Snake Ladder Grid - 2 Players", size=(580, 720))
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.grid = gridlib.Grid(panel)
        self.grid.CreateGrid(10, 10)
        self.grid.DisableDragColSize()
        self.grid.DisableDragRowSize()
        self.grid.EnableEditing(False)
        self.grid.SetRowLabelSize(0)
        self.grid.SetColLabelSize(0)
        for i in range(10):
            self.grid.SetColSize(i, 45)
            self.grid.SetRowSize(i, 45)
        fill_snake_ladder_numbers(self.grid)
        self.colour_snakes_ladders()
        self.add_snake_ladder_symbols()
        self.player_pos = [1, 1]
        self.prev_player_pos = [None, None]
        self.current_player = 0
        self.highlight_players()
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.roll_btn = wx.Button(panel, label="Roll Dice")
        hbox.Add(self.roll_btn, 0, wx.ALL, 5)
        self.new_game_btn = wx.Button(panel, label="New Game")
        hbox.Add(self.new_game_btn, 0, wx.ALL, 5)
        self.status = wx.StaticText(panel, label="Player 1's turn. Click Roll Dice.")
        font = self.status.GetFont()
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        self.status.SetFont(font)
        hbox.Add(self.status, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        vbox.Add(self.grid, 1, wx.EXPAND | wx.ALL, 5)
        vbox.Add(hbox, 0, wx.EXPAND | wx.ALL, 5)
        panel.SetSizer(vbox)
        self.roll_btn.Bind(wx.EVT_BUTTON, self.on_roll)
        self.new_game_btn.Bind(wx.EVT_BUTTON, self.on_new_game)

    def find_cell_for_number(self, num):
        target = str(num)
        for r in range(self.grid.GetNumberRows()):
            for c in range(self.grid.GetNumberCols()):
                val = self.grid.GetCellValue(r, c)
                num_part = ""
                for ch in val:
                    if ch.isdigit():
                        num_part += ch
                    else:
                        break
                if num_part == target:
                    return r, c
        return None, None

    def colour_snakes_ladders(self):
        snake_colors = [wx.Colour(255, 180, 180), wx.Colour(255, 150, 150), wx.Colour(255, 200, 200),
                        wx.Colour(255, 160, 190), wx.Colour(255, 210, 170), wx.Colour(255, 140, 140),
                        wx.Colour(230, 120, 150), wx.Colour(240, 170, 170), wx.Colour(220, 110, 110),
                        wx.Colour(250, 190, 190)]
        ladder_colors = [wx.Colour(180, 255, 180), wx.Colour(200, 255, 200), wx.Colour(150, 220, 255),
                         wx.Colour(190, 230, 190), wx.Colour(160, 255, 220), wx.Colour(190, 120, 180),
                         wx.Colour(200, 178, 160), wx.Colour(100, 150, 200), wx.Colour(225, 250, 150)]
        for r in range(self.grid.GetNumberRows()):
            for c in range(self.grid.GetNumberCols()):
                self.grid.SetCellBackgroundColour(r, c, wx.WHITE)
        for i, (head, tail) in enumerate(SNAKES.items()):
            color = snake_colors[i % len(snake_colors)]
            r1, c1 = self.find_cell_for_number(head)
            r2, c2 = self.find_cell_for_number(tail)
            if r1 is not None: self.grid.SetCellBackgroundColour(r1, c1, color)
            if r2 is not None: self.grid.SetCellBackgroundColour(r2, c2, color)
        for i, (bottom, top) in enumerate(LADDERS.items()):
            color = ladder_colors[i % len(ladder_colors)]
            r1, c1 = self.find_cell_for_number(bottom)
            r2, c2 = self.find_cell_for_number(top)
            if r1 is not None: self.grid.SetCellBackgroundColour(r1, c1, color)
            if r2 is not None: self.grid.SetCellBackgroundColour(r2, c2, color)

    def add_snake_ladder_symbols(self):
        snake_emoji = " 🐍"
        ladder_emoji = " 🪜"
        for head, tail in SNAKES.items():
            for pos in (head, tail):
                r, c = self.find_cell_for_number(pos)
                if r is None: continue
                val = self.grid.GetCellValue(r, c)
                if snake_emoji not in val:
                    self.grid.SetCellValue(r, c, val + snake_emoji)
        for bottom, top in LADDERS.items():
            for pos in (bottom, top):
                r, c = self.find_cell_for_number(pos)
                if r is None: continue
                val = self.grid.GetCellValue(r, c)
                if ladder_emoji not in val:
                    self.grid.SetCellValue(r, c, val + ladder_emoji)

    def clear_player_backgrounds(self):
        snake_colors = [wx.Colour(255, 180, 180), wx.Colour(255, 150, 150), wx.Colour(255, 200, 200),
                        wx.Colour(255, 160, 190), wx.Colour(255, 210, 170), wx.Colour(255, 140, 140),
                        wx.Colour(230, 120, 150), wx.Colour(240, 170, 170), wx.Colour(220, 110, 110),
                        wx.Colour(250, 190, 190)]
        ladder_colors = [wx.Colour(180, 255, 180), wx.Colour(200, 255, 200), wx.Colour(150, 220, 255),
                         wx.Colour(190, 230, 190), wx.Colour(160, 255, 220), wx.Colour(190, 120, 180),
                         wx.Colour(200, 178, 160), wx.Colour(100, 150, 200), wx.Colour(225, 250, 150)]
        for idx in range(2):
            if self.prev_player_pos[idx] is not None:
                num = self.prev_player_pos[idx]
                pr, pc = self.find_cell_for_number(num)
                if pr is None: continue
                base_colour = wx.WHITE
                for i, (h, t) in enumerate(SNAKES.items()):
                    if num == h or num == t:
                        base_colour = snake_colors[i % len(snake_colors)]
                        break
                for i, (b, t) in enumerate(LADDERS.items()):
                    if num == b or num == t:
                        base_colour = ladder_colors[i % len(ladder_colors)]
                        break
                self.grid.SetCellBackgroundColour(pr, pc, base_colour)
                self.grid.SetCellTextColour(pr, pc, wx.BLACK)

    def highlight_players(self):
        self.clear_player_backgrounds()
        bg_colors = [wx.Colour(255, 0, 0), wx.Colour(0, 0, 255)]
        text_colors = [wx.WHITE, wx.WHITE]
        for idx in range(2):
            r, c = self.find_cell_for_number(self.player_pos[idx])
            if r is not None:
                self.grid.SetCellBackgroundColour(r, c, bg_colors[idx])
                self.grid.SetCellTextColour(r, c, text_colors[idx])
                self.prev_player_pos[idx] = self.player_pos[idx]
        self.grid.ForceRefresh()

    def apply_snakes_ladders(self, pos):
        if pos in SNAKES: return SNAKES[pos]
        if pos in LADDERS: return LADDERS[pos]
        return pos

    def on_roll(self, event):
        p = self.current_player
        other = 1 - p
        roll = random.randint(1, 6)
        old = self.player_pos[p]
        tentative = old + roll
        if tentative > 100:
            tentative = old
        jumped = self.apply_snakes_ladders(tentative)
        self.player_pos[p] = jumped
        self.highlight_players()
        msg = f"Player {p+1} rolled {roll}. "
        if jumped != tentative:
            if tentative in SNAKES:
                msg += "Bitten by SNAKE! Slid down."
            else:
                msg += "Climbed LADDER! Moved up."
        if self.player_pos[p] == 100:
            msg = f"Player {p+1} wins!"
            self.roll_btn.Disable()
            wx.MessageBox(f"Player {p+1} wins!", "Game Over")
        else:
            if roll != 6:
                self.current_player = other
        self.status.SetLabel(msg)

    def on_new_game(self, event):
        self.player_pos = [1, 1]
        self.prev_player_pos = [None, None]
        self.current_player = 0
        fill_snake_ladder_numbers(self.grid)
        self.colour_snakes_ladders()
        self.add_snake_ladder_symbols()
        self.highlight_players()
        self.roll_btn.Enable()
        self.status.SetLabel("Player 1's turn. Click Roll Dice.")

if __name__ == "__main__":
    app = wx.App(False)
    frame = GridFrame()
    frame.Show()
    app.MainLoop()
