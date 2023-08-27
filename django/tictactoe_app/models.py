from django.db import models
from users_app.models import User
from django.contrib.postgres.fields import ArrayField


    
class Match(models.Model):
    player1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='match_player1')
    player2 = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='match_player2')
    finish = models.BooleanField(default=False)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='match_winner')
    turn = models.IntegerField(default=1)
    row0column0 = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='match_row0column0')
    row0column1 = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='match_row0column1')
    row0column2 = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='match_row0column2')
    row1column0 = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='match_row1column0')
    row1column1 = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='match_row1column1')
    row1column2 = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='match_row1column2')
    row2column0 = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='match_row2column0')
    row2column1 = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='match_row2column1')
    row2column2 = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='match_row2column2')

    def check_horizontal(self, row, column):
        object_dict = self.__dict__
        return object_dict['row'+str(row)+'column0_id'] == object_dict['row'+str(row)+'column1_id'] and object_dict['row'+str(row)+'column0_id'] == object_dict['row'+str(row)+'column2_id']

    def check_vertical(self, row, column):
        object_dict = self.__dict__
        return object_dict['row0column'+str(column)+'_id'] == object_dict['row1column'+str(column)+'_id'] and object_dict['row0column'+str(column)+'_id'] == object_dict['row2column'+str(column)+'_id']

    def check_diagonal_1(self):
        object_dict = self.__dict__
        return object_dict['row0column0_id'] == object_dict['row1column1_id'] and object_dict['row0column0_id'] == object_dict['row2column2_id']

    def check_diagonal_2(self):
        object_dict = self.__dict__
        return object_dict['row0column2_id'] == object_dict['row1column1_id'] and object_dict['row0column2_id'] == object_dict['row2column0_id']

    def check_diagonal(self, row, column):
        if abs(row-column)!=1: 
            if row==1 and column==1:
                return self.check_diagonal_1() or self.check_diagonal_2()
            elif row-column==0:
                return self.check_diagonal_1()
            else:
                return self.check_diagonal_2()
        return False


    def get_board(self):
        row0 = [self.row0column0,self.row0column1, self.row0column2]
        row1 = [self.row1column0,self.row1column1, self.row1column2]
        row2 = [self.row2column0,self.row2column1, self.row2column2]
        board = [row0,row1,row2]
        return board

    def get_row_column_parse(self, row, column):
        object_dict = self.__dict__
        if object_dict['row'+str(row)+'column'+str(column)+'_id'] is None:
            return '-'
        elif object_dict['row'+str(row)+'column'+str(column)+'_id']==self.player1.id:
            return 'X'
        else:
            return 'O'

    def get_row_parse(self, row):
        return self.get_row_column_parse(row,0)+' | '+self.get_row_column_parse(row,1)+ ' | '+self.get_row_column_parse(row,2)


    def set_value_row_column(self, row, column, user):
        setattr(self,'row'+str(row)+'column'+str(column),user)
        
        if self.check_horizontal(row, column) or self.check_vertical(row, column) or self.check_diagonal(row, column):
            self.finish = True
            self.winner = user
        
        self.turn = self.turn+1
        if self.turn>=10:
            self.finish=True
        
        self.save()






