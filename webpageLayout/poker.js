
var cardsPath = "";
//var playerNumber = //Get JSON for User player
var gameOver = false;
var isPlayerTurn = false;
var bet = 0;
var folded = false;
var funds = 0;
var cardsShown = 0;


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

if (gameOver) {
    //var playerOneHand = //Get JSON for player one's hand.;
    //var playerTwoHand = //Get JSON for player two's hand.;
    //var playerThreeHand = //Get JSON for player three's hand.;
    //var playerFourHand = //Get JSON for player four's hand.;
    //var getWinner = //Get JSON for winner

    $(".p1c1").attr('src',cardsPath + playerOneHand.cards[0].suit  
              + "-" + playerOneHand.cards[0].value + ".png");

    $(".p1c2").attr('src',cardsPath + playerOneHand.cards[1].suit  
              + "-" + playerOneHand.cards[1].value + ".png");

    $(".p2c1").attr('src',cardsPath + playerTwoHand.cards[0].suit  
                  + "-" + playerTwoHand.cards[0].value + ".png");

    $(".p2c2").attr('src',cardsPath + playerTwoHand.cards[1].suit  
                  + "-" + playerTwoHand.cards[1].value + ".png");

    $(".p3c1").attr('src',cardsPath + playerThreeHand.cards[0].suit  
              + "-" + playerThreeHand.cards[0].value + ".png");

    $(".p3c2").attr('src',cardsPath + playerThreeHand.cards[1].suit
              + "-" + playerThreeHand.cards[1].value + ".png");

    $(".p4c1").attr('src',cardsPath + playerFourHand.cards[0].suit  
              + "-" + playerFourHand.cards[0].value + ".png");

    $(".p4c2").attr('src',cardsPath + playerFourHand.cards[1].suit  
              + "-" + playerFourHand.cards[1].value + ".png");
}