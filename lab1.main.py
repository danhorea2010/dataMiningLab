from APIs.chesscom import ChessAPI


def main():
    test = ChessAPI()
    result = test.get_games({"player_name": "Raugan"})
    print(result)



if __name__ == "__main__" :
    main()