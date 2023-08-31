from rest_framework import serializers

from tictactoe_app.models import Match


class MatchCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Match
        fields = ['id']
        read_only_fields = ['id']
        

    def create(self, validated_data):
        validated_data['player1'] = self.context['request'].user
        return super(MatchCreateSerializer, self).create(validated_data)


class MatchJoinSerializer(serializers.ModelSerializer):
    player1_username = serializers.SerializerMethodField('get_player1_username')
    player2_username = serializers.SerializerMethodField('get_player2_username')


    class Meta:
        model = Match
        fields = ['id','player1_username','player2_username']
        read_only_fields = ['id','player1_username','player2_username']


    def get_player1_username(self, obj):
        return obj.player1.username

    def get_player2_username(self, obj):
        return obj.player2.username

    def validate(self, data):
        if (self.instance.player2 is not None) or (self.instance.player1==self.context['request'].user):
            raise serializers.ValidationError('Can not Join to this Match')
        return data

    def update(self, instance, validated_data):
        instance.player2 = self.context['request'].user
        instance.save()
        return instance


class MatchDetailSerializer(serializers.ModelSerializer):
    winner = serializers.SerializerMethodField('get_winner')
    X = serializers.SerializerMethodField('get_X')
    O = serializers.SerializerMethodField('get_O')
    board_row0 = serializers.SerializerMethodField('get_board_row0') 
    board_row1 = serializers.SerializerMethodField('get_board_row1') 
    board_row2 = serializers.SerializerMethodField('get_board_row2') 
    
    class Meta:
        model = Match
        fields = ['id','X','O','turn','finish','winner','board_row0','board_row1','board_row2']
        read_only_fields = ['id','X','O','turn','finish','winner','board_row0','board_row1','board_row2']

    def get_X(self, obj):
        return obj.player1.username

    def get_O(self, obj):
        return obj.player2.username

    def get_winner(self, obj):
        if obj.winner is None:
            return 'Draw'
        return obj.winner.username

    def get_board_row0(self, obj):
        return obj.get_row_parse(0)
    
    def get_board_row1(self, obj):
        return obj.get_row_parse(1)
    
    def get_board_row2(self, obj):
        return obj.get_row_parse(2)


class MatchPlaySerializer(serializers.ModelSerializer):
    row = serializers.IntegerField(min_value=0, max_value=2, write_only=True)
    column = serializers.IntegerField(min_value=0, max_value=2, write_only=True)


    class Meta:
        model = Match
        fields = ['id','row','column']
        read_only_fields = ['id']


    def validate(self, data):
        if self.instance.finish:
            raise serializers.ValidationError('Can not move, the match is over')

        if not(self.instance.player1==self.context['request'].user or self.instance.player2==self.context['request'].user):
            raise serializers.ValidationError('Can not play')


        if not((self.instance.turn%2==1 and self.instance.player1==self.context['request'].user) or (self.instance.turn%2==0 and self.instance.player2==self.context['request'].user)):
            raise serializers.ValidationError('Can not move, it´s not your turn')

        if self.instance.__dict__['row'+str(data['row'])+'column'+str(data['column'])+'_id'] is not None:
            raise serializers.ValidationError('Can not move, the position is occupied')

        return data

    def update(self, instance, validated_data):
        instance.set_value_row_column(validated_data.get('row'),validated_data.get('column'),self.context['request'].user)
        return instance