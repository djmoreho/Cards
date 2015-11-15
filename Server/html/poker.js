src="jquery-1.11.3.min.js";
//url the ajax stuff posts to
var url ="";
//All the other stuff
var cardsPath = "card_pics/";
var playerHand = playerData["playerHand"];
var playerNumber = playerData["playerNumber"];
var gameOver = false;
var currentPlayerTurn = 0;
var bet = 0;
var folded = false;
var river1 = "BJ";
var river2 = "BJ";
var river3 = "BJ";
var river4 = "BJ";
var river5 = "BJ";
var pot = 0;
var loggedIn = false;
var ready = false;

function login(){
        var dataOut = {action:"signup"};
        var redJSON=$.post(url, dataOut, function(){},"json");     
        return redJSON["SignUpWorked"];
}

function isReady(){
        var dataOut = {action:"IsItReady"};
        var redJSON=$.post(url, dataOut, function(){},"json");
        return redJSON["Ready"];
}

function fold(){
        if (currentPlayerTurn === playerNumber && !folded){
            var dataOut = {action:"Fold"};
            var caller=$.post(url, dataOut, function(){},"json");
            if(caller["success"]){
                folded = true;
            }
            refresh();
        }
}

function call(){
        var dataOut={action:"Call"};
        $.post(url, dataOut, function(){},"json");
        refresh();
}

function raise(raiseAmount){
        var dataOut={action:"Raise",value:raiseAmount};
        $.post(url, dataOut, function(){},"json");
        refresh();
}

function getPlayerData(){
        var dataOut={action:"GetPlayerData"};
        return $.post(url, dataOut, function(){},"json");
}

function theGame(){
        while(!loggedIn){
            loggedIn = login();
        }
        
        while(!ready){
            ready = isReady();
        }
        
        playerData = getPlayerData();
        playerHand = playerData["playerHand"];
        playerNumber = playerData["playerNumber"];
        while(!gameOver){
            refresh();
        }
}
/*
function reset(){
    var river1 = "BJ";
    var river2 = "BJ";
    var river3 = "BJ";
    var river4 = "BJ";
    var river5 = "BJ";
    var playerData = $.post(url, {"datatype":"json", "headers":header});
    var playerHand = playerData["hand"];
    var pot = 0;
    $(".p1c1").attr('src',"playing-card-back.jpg");

    $(".p1c2").attr('src',"playing-card-back.jpg");

    $(".p2c1").attr('src',"playing-card-back.jpg");

    $(".p2c2").attr('src',"playing-card-back.jpg");

    $(".p3c1").attr('src',"playing-card-back.jpg");

    $(".p3c2").attr('src',"playing-card-back.jpg");

    $(".p4c1").attr('src',"playing-card-back.jpg");

    $(".p4c2").attr('src',"playing-card-back.jpg");
}
*/
function refresh(){
    var dataOut = {action:"Update"};
    scoresJSON = $.post(url, dataOut, function(){},"json");;
    playerScores = scoresJSON["Scores"];
    reveal = scoresJSON["allHands"];
    pot = scoresJSON["Pot"];
    gameOver = scoresJSON["GameOver"];
    river = scoresJSON["river"];
    CardsShown = scoresJSON["RiverCount"];
    
    //Data for player's scores/Turn
    $("#p1-money").html("Player 1: " + playerScores[0].toString());
    $("#p2-money").html("Player 2: " + playerScores[1].toString());
    $("#p3-money").html("Player 3: " + playerScores[2].toString());
    $("#p4-money").html("Player 4: " + playerScores[3].toString());
    $("#playerMoney").html("Money Left: " + scoresJSON["playerScores"[playerNumber]].toString());
    $("#playerTurn").html("Player" + (scoresJSON["CurrentPlayerTurn"] + 1).toString() + "'s Turn" );
    
    //These ifs are for the river.
    if(cardsShown = 1){
        river1 = river.substr(0,2)
        $(".center1").attr('src',cardsPath + river1 + ".png");
    }
    
    if(cardsShown = 2){
        river2 = river.substr(2,2);
        $(".center2").attr('src',cardsPath + river2 + ".png");
    }
    
    if(cardsShown = 3){
        river3 = river.substr(4,2);
        $(".center3").attr('src',cardsPath + river3 + ".png");
    }
    
    if(cardsShown = 4){
        river4 = river.substr(6,2);
        $(".center4").attr('src',cardsPath + river4 + ".png");
    }
    
    if(cardsShown = 5){
        river5 = river.substr(8,2);
        $(".center5").attr('src',cardsPath + river5 + ".png");
    }
    
    
    //If the game is over, reveal all players hands
    if (gameOver) {
        Hands = ScoresJSON["AllHands"];
        PlayerOneHand=[Hands.substr(0,2), Hands.substr(2,2)];
        PlayerTwoHand=[Hands.substr(4,2), Hands.substr(6,2)];
        PlayerThreeHand=[Hands.substr(8,2), Hands.substr(10,2)];
        PlayerFourHand=[Hands.substr(12,2), Hands.substr(14,2)]
        $(".p1c1").attr('src',cardsPath + playerOneHand[0] + ".png");

        $(".p1c2").attr('src',cardsPath + playerOneHand[1] + ".png");

        $(".p2c1").attr('src',cardsPath + playerTwoHand[0] + ".png");

        $(".p2c2").attr('src',cardsPath + playerTwoHand[1] + ".png");

        $(".p3c1").attr('src',cardsPath + playerThreeHand[0] + ".png");

        $(".p3c2").attr('src',cardsPath + playerThreeHand[1] + ".png");

        $(".p4c1").attr('src',cardsPath + playerFourHand[0] + ".png");

        $(".p4c2").attr('src',cardsPath + playerFourHand[1] + ".png");
        
        
    }
}

/*
if(playerNumber == 0){
    //var playerOneHand = //Get JSON for player one's hand.;
    $(".p1c1").attr('src',cardsPath + playerOne.cards[0] + ".png");
  
    $(".p1c2").attr('src',cardsPath + playerOne.cards[1] + ".png");
}

if(playerNumber == 1){
    //var playerTwoHand = //Get JSON for player two's hand.;
    $(".p2c1").attr('src',cardsPath + playerTwo.cards[0] + ".png");

    $(".p2c2").attr('src',cardsPath + playerTwo.cards[1] + ".png");
}

if(playerNumber == 2){
    //var playerThreeHand = //Get JSON for player three's hand.;
    $(".p3c1").attr('src',cardsPath + playerThree.cards[0] + ".png");

    $(".p3c2").attr('src',cardsPath + playerThree.cards[1] + ".png");
}

if(playerNumber == 3){
    //var playerFourHand = //Get JSON for player four's hand.;
    $(".p4c1").attr('src',cardsPath + playerFour.cards[0] + ".png");

    $(".p4c2").attr('src',cardsPath + playerFour.cards[1] + ".png");
}
*/