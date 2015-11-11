
var cardsPath = "card_pics/";
//var playerNumber = //Get JSON for User player
var gameOver = false;
var currentPlayerTurn = 0;
var bet = 0;
var folded = false;
var cardsShown = 0;
var player1Score = 0 ;
var player2Score = 0;
var player3Score = 0;
var player4Score= 0;
var playerNumber = 0;
var river1 = "BJ";
var river2 = "BJ";
var river3 = "BJ";
var river4 = "BJ";
var river5 = "BJ";
var pot = 0;

function refresh(scoresJSON){
    //I should request the scores here.
    //scoresJSON= score method
    
    player1Score = scoresJSON[0];
    player2Score = scoresJSON[1];
    player3Score = scoresJSON[2];
    player4Score = scoresJSON[3];
    pot = scoresJSON[4];
    gameOver = scoresJSON[5];
    nextPlayer = scoresJSON[6];
    
    //Data for player's scores/Turn
    $("#p1-money").html("Player 1: " + player1Score.toString());
    $("#p2-money").html("Player 2: " + player2Score.toString());
    $("#p3-money").html("Player 3: " + player3Score.toString());
    $("#p4-money").html("Player 4: " + player4Score.toString());
    $("#playerMoney").html("Money Left: " + scoresJSON[playerNumber].toString());
    $("#playerTurn").html("Player" + (currentPlayerTurn + 1).toString() + "'s Turn" );
    
    //These ifs are for the river.
    if(cardsShown = 1){
        //get river first card put into river1
        $("center1").attr('src',cardsPath + river1 + ".png");
    }
    
    if(cardsShown = 2){
        //get river second card put into river2
        $("center2").attr('src',cardsPath + river2 + ".png");
    }
    
    if(cardsShown = 3){
        //get river first card put into river3
        $("center3").attr('src',cardsPath + river3 + ".png");
    }
    
    if(cardsShown = 4){
        //get river first card put into river1
        $("center4").attr('src',cardsPath + river4 + ".png");
    }
    
    if(cardsShown = 5){
        //get river first card put into river1
        $("center5").attr('src',cardsPath + river5 + ".png");
    }
    
    
    //If the game is over, reveal all players hands
    if (gameOver) {
        //var playerOneHand = //Get JSON for player one's hand.;
        //var playerTwoHand = //Get JSON for player two's hand.;
        //var playerThreeHand = //Get JSON for player three's hand.;
        //var playerFourHand = //Get JSON for player four's hand.;
        //var getWinner = //Get JSON for winner

        $(".p1c1").attr('src',cardsPath + playerOneHand.cards[0] + ".png");

        $(".p1c2").attr('src',cardsPath + playerOneHand.cards[1] + ".png");

        $(".p2c1").attr('src',cardsPath + playerTwoHand.cards[0] + ".png");

        $(".p2c2").attr('src',cardsPath + playerTwoHand.cards[1] + ".png");

        $(".p3c1").attr('src',cardsPath + playerThreeHand.cards[0] + ".png");

        $(".p3c2").attr('src',cardsPath + playerThreeHand.cards[1] + ".png");

        $(".p4c1").attr('src',cardsPath + playerFourHand.cards[0] + ".png");

        $(".p4c2").attr('src',cardsPath + playerFourHand.cards[1] + ".png");
        }
}


if(playerNumber == 0){
    //var playerOneHand = //Get JSON for player one's hand.;
    $(".p1c1").attr('src',cardsPath + playerOne.cards[0].suit  
          + "-" + playerOne.cards[0].value + ".png");
  
    $(".p1c2").attr('src',cardsPath + playerOne.cards[1].suit  
          + "-" + playerOne.cards[1].value + ".png");
}

if(playerNumber == 1){
    //var playerTwoHand = //Get JSON for player two's hand.;
    $(".p2c1").attr('src',cardsPath + playerTwo.cards[0].suit  
              + "-" + playerTwo.cards[0].value + ".png");

    $(".p2c2").attr('src',cardsPath + playerTwo.cards[1].suit  
              + "-" + playerTwo.cards[1].value + ".png");
}

if(playerNumber == 2){
    //var playerThreeHand = //Get JSON for player three's hand.;
    $(".p3c1").attr('src',cardsPath + playerThree.cards[0].suit  
              + "-" + playerThree.cards[0].value + ".png");

    $(".p3c2").attr('src',cardsPath + playerThree.cards[1].suit  
              + "-" + playerThree.cards[1].value + ".png");
}

if(playerNumber == 3){
    //var playerFourHand = //Get JSON for player four's hand.;
    $(".p4c1").attr('src',cardsPath + playerFour.cards[0].suit  
              + "-" + playerFour.cards[0].value + ".png");

    $(".p4c2").attr('src',cardsPath + playerFour.cards[1].suit  
              + "-" + playerFour.cards[1].value + ".png");
}